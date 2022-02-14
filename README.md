# LDAP Redirector

The goal of this project is to provide a basic LDAP-Server for authentication with a third-party authentication service. 

This is useful for services depending on LDAP-Authentication but the data is actually independent from your local Directory-Services.

> ⚠️ This repo is currently work in progress!

## Only for the brave
Try using it: 
`python ldap_redirector --authentication-container "ou=Employee,dc=practice,dc=net" --authentication-backend "instagram" --host "0.0.0.0" --port 689`