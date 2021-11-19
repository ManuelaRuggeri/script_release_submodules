#!/bin/env python3
import xmlrpc.client

url = "http://localhost:8085"
db = "odoo12_Limpe_Master_2021-09-22"
username = 'user_connector_event@example.com'
password = 'test'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

result = models.execute_kw(db, uid, password, 'syd_api_event.connector', 'test_connection', [], {})

print(result)