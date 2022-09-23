import unittest
from click.testing import CliRunner
from .command_parser import parse as command_parser_main
import socket
from loguru import logger
import threading

def run_server():
    cliRunner = CliRunner()
    params = ['--authentication-container', '"ou=Employee,dc=practice,dc=net"', '--authentication-backend', 'instagram', '--host', '127.0.0.1', '--port', 689, '--chrome-binary-path', '"C:\\Users\\marti\\AppData\\Local\\BraveSoftware\\Brave-Browser-Betae-version 98.0.4758.80\\Application\\brave.exe"', '--chrome-version', '98.0.4758.80']
    
    result = cliRunner.invoke(command_parser_main, params)
    assert result.return_value == 0

class TestSum(unittest.TestCase):
    def __init__(self):
        super().__init__()
        threading.Thread(target=run_server).start()


    def test_userless_login_response(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 689))
            s.sendall(bytearray.fromhex("300c020101600702010304008000"))
            data = s.recv(2048)
            

if __name__ == '__main__':
    unittest.main()