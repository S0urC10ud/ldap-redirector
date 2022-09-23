from email.policy import default
import click
from loguru import logger
import ldap_redirector.authBackendResolver
from .messageHandler import LdapSocketFactory

@click.command()
@click.option('--authentication-container', 
              prompt='your base path',
              help='Path to your users - e.g.:ou=Employee,dc=practice,dc=net')
@click.option('--authentication-backend', 
              default="instagram",
              help='Module-Name of the authentication backend in auth-backends.py')
@click.option('--host', 
              prompt='your service-ip',
              help='IP to host the server-socket - for example 0.0.0.0 for full accessibility',
              default="127.0.0.1")
@click.option('--port', 
              prompt='your service-port',
              help='Your ldap service port - for example 689',
              default=689)
@click.option('--object-class', 
              help='user object class',
              default="inetOrgPerson")
@click.option('--reply-cn', 
              help='default reply Common Name',
              default="asdf")
@click.option('--reply-sn', 
              help='default reply Surname for all users - should not matter as well as CN',
              default="asdf")
@click.option('--chrome-binary-path', 
              help='Path to the chromium binary. Needed if the authentication-manager requires selenium (like Instagram).',
              required=False)
@click.option('--chrome-version',
              help='The version of your chromium binary. Needed if the authentication-manager requires selenium (like Instagram). e.g.: 98.0.4758.80',
              required=False)
def parse(authentication_container: str,
        authentication_backend: str,
        host:str,
        port:int,
        object_class: str,
        reply_cn: str,
        reply_sn: str,
        chrome_binary_path: str = None,
        chrome_version: str = None):
    config = {
        "validator": ldap_redirector.authBackendResolver.get_auth_backend(authentication_backend, chrome_binary_path, chrome_version),
        "authentication_container": authentication_container,
        "object_class": object_class,
        "cn": reply_cn,
        "sn": reply_sn,
    }

    logger.info(f"Starting with Auth-Backend {authentication_backend}!")

    LdapSocketFactory(host, port, config)