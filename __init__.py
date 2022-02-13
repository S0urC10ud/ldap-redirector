import click
import authBackends
from ldapRedirector.messageHandler import LdapSocketFactory

@click.command()
@click.option('--authentication-container', prompt='your base path',
              help='Path to your users - e.g.:ou=Employee,dc=practice,dc=net')
@click.option('--authentication-backend', prompt='used python backend for authentication',
              help='Module-Name of the authentication backend in auth-backends.py')
@click.option('--host', prompt='your service-ip',
              help='IP to host the server-socket - for example 0.0.0.0 for full accessibility',
              default="127.0.0.1")
@click.option('--port', prompt='your service-port',
              help='Your ldap service port - for example 689',
              default="689")
@click.option('--object-class', prompt='user object class',
              default="inetOrgPerson")
@click.option('--reply-cn', prompt='default reply Common Name',
              default="asdf")
@click.option('--reply-sn', prompt='default reply Surname for all users - should not matter as well as CN',
              default="asdf")
def main(authentication_container: str,
        authentication_backend: str,
        host:str,
        port:int,
        object_class: str,
        reply_cn: str,
        reply_sn: str):
    config = {
        "validator": authBackends.get_auth_backend(authentication_backend),
        "authentication_container": authentication_container,
        "object_class": object_class,
        "cn": reply_cn,
        "sn": reply_sn,
    }

    LdapSocketFactory(host, port, config)


if __name__ == '__main__':
    main()