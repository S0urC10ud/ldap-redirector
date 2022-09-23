from calendar import c
from threading import Thread
from ldaptor.protocols import pureldap, pureber
import socket

from loguru import logger
import loguru
import ldap_redirector.ldapResponder


berdecoder = pureldap.LDAPBERDecoderContext_TopLevel(
        inherit=pureldap.LDAPBERDecoderContext_LDAPMessage(
            fallback=pureldap.LDAPBERDecoderContext(
                fallback=pureber.BERDecoderContext()
            ),
            inherit=pureldap.LDAPBERDecoderContext(
                fallback=pureber.BERDecoderContext()
            ),
        )
    )

#Debugging-Buffers from Wireshark (I haven't yet found time for automated testing):
# Userless-Login
# buffer = "300c020101600702010304008000"

# User-Search
# buffer = "3042020102633d041e6f753d456d706c6f7965652c64633d70726163746963652c64633d6e65740a01010a0101020100020119010100a30a0402636e0404617364663000"

# Login-Try
#buffer = "3043020103603e02010304277569643d617364662c6f753d456d706c6f7965652c64633d70726163746963652c64633d6e657480107465737450617373776f726461736466"

# Unbind-Request
#buffer = "30050201044200"

# buffer = bytearray.fromhex(buffer)
#decoder = asn1.Decoder()
#decoder.start(bytes(buffer))
#tag, value = decoder.read()

class LdapSocketFactory:
    def __init__(self, host, port, ldapConfig):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            logger.info(f"Listening for connections on {host}:{port}!")
            s.listen()
            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        print('Connected by', addr)
                        LdapSocket(conn, ldapConfig).start()
                except KeyboardInterrupt:
                    logger.info("Stopping because of a keyboard interrupt")
                    break
                    

class LdapSocket(Thread):
    def __init__(self, conn, ldapConfig):
        self.socket = conn
        self.config = ldapConfig
            
    def run(self):
        while True:
            data = self.conn.recv(1024)
            self.handle_packet(data)
            if not data:
                break

    def send_answer(self, messageId: int, packetData:pureldap.LDAPProtocolOp):
        self.socket.sendall(pureldap.LDAPMessage(packetData, id=messageId).toWire())

    async def handle_packet(self, buffer):
        resObject = pureber.berDecodeObject(berdecoder, buffer)[0]
        logger.debug(f"Handling a packet with the contents: {resObject}")

        if resObject is None:
            raise Exception("Packet is not parsable:" +str(buffer))
        elif isinstance(resObject.value, pureldap.LDAPUnbindRequest):
            self.socket.close()
        elif isinstance(resObject.value, pureldap.LDAPSearchRequest):
            if resObject.value.filter.attributeDesc.value == b'cn':
                user_path = resObject.value.baseObject.decode("utf-8") # TODO: Maybe use me
                user_name = resObject.value.filter.assertionValue.value.decode("utf-8")
                self.send_answer(ldapResponder.search_result_person(user_name, 
                        oc=self.config.objectClass,
                        cn=self.config.cn,
                        sn=self.config.sn,
                        base_path=self.config.authentication_container
                    ))
                self.send_answer(ldapResponder.search_result_done())
        elif isinstance(resObject.value, pureldap.LDAPBindRequest):
            if not resObject.value.auth:
                self.send_answer(ldapResponder.successful_empty_bind_response())
            elif resObject.value.dn is not None:
                username = list(filter(lambda X: "uid" in X, resObject.value.dn.decode("utf-8").split(",")))[0][4:]
                password = resObject.value.auth.decode("utf-8") 
                
                if await self.config.validator.validate(username, password):
                    self.send_answer(ldapResponder.successful_empty_bind_response())
                else:
                    self.send_answer(ldapResponder.invalid_credentials_bind_response())