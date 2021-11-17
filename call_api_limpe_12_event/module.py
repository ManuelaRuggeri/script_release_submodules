#!/bin/env python3
import xmlrpc.client

url = "http://localhost:8085"
db = "odoo12_Limpe_Master_2021-09-22"
username = 'a'
password = 'a'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

res = models.execute_kw(db, uid, password,
            'res.users', 'search',
            [[['id', '=', 2]]],
            {})

result = models.execute_kw(db, uid, password, 'event.event', 'get_sub_event_api', [], {})

print(result)