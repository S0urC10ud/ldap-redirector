
import types
from ldaptor.protocols import pureldap, pureber


def rec_tuple_to_list(tuple_obj):
    res_list = []
    for el in tuple_obj:
        if isinstance(el, tuple):
            res_list.append(rec_tuple_to_list(el))
        else:
            res_list.append(el)
    return res_list

def modify_every_element(list_obj: list, modifier: types.FunctionType):
    tupleException = Exception("Invalid parameter list_obj has to be and contain only lists - not a tuple")

    if isinstance(list_obj, tuple):
        raise tupleException
    
    for idx, el in enumerate(list_obj):
        if isinstance(el, tuple):
            raise tupleException
        if isinstance(el, list):
            modify_every_element(el, modifier)
            continue

        list_obj[idx] = modifier(el)

def successful_empty_bind_response():
    return pureldap.LDAPBindResponse(resultCode=0)

def search_result_done():
    return pureldap.LDAPSearchResultDone(resultCode=0)

def invalid_credentials_bind_response():
    return pureldap.LDAPBindResponse(resultCode=49)

def search_result_person(uid, oc="inetOrgPerson", sn="as", cn="asdf", base_path="ou=Employee,dc=practice,dc=net"):
    attributes = [('objectClass', (oc,)), ('sn', (sn,)), ('cn', (cn,)), ('uid', (uid,))] 
    attributes = rec_tuple_to_list(attributes)


    modify_every_element(attributes, lambda X: bytearray(X.encode()))
    return pureldap.LDAPSearchResultEntry(
        objectName=f"uid={uid},{base_path}",
        attributes=attributes
    )


