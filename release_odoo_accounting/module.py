# -*- coding: utf-8 -*-

import sys
import os
import xmltodict
import tempfile
import logging

_logger = logging.getLogger(__name__)

if len(sys.argv) > 1 and sys.argv[1]:
    path_file_xml = 'settings.xml'
else:
    path_file_xml = os.path.join(tempfile.gettempdir(), 'settings.xml')

print('path_file_xml: {}'.format(path_file_xml))

with open(path_file_xml, 'r') as myfile:
    data = xmltodict.parse(myfile.read())

for repo in data['repositories']:
    os.chdir('{}'.format(data['repositories'][repo]['name']))
    print(os.getcwd())
    os.system('git checkout {}'.format(data['repositories'][repo]['branch_update']))
    os.system('git pull')
    os.system('git submodule update')
    submodules_updated = []
       
    if data['repositories'][repo]['submodules']['odoo-accounting']:
        os.chdir('odoo-accounting')
        print(os.getcwd())
        os.system('git fetch')
        os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
        os.chdir('..')
        print(os.getcwd())
        os.system('git add odoo-accounting')
        submodules_updated.append('odoo-accounting')
    
    if data['repositories'][repo]['submodules']['odoo-accounting-enterprise']:
        os.chdir('odoo-accounting-enterprise')
        print(os.getcwd())
        os.system('git fetch')
        os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
        os.chdir('..')
        print(os.getcwd())
        os.system('git add odoo-accounting-enterprise')
        submodules_updated.append('odoo-accounting-enterprise')
    
    if data['repositories'][repo]['submodules']['odoo-accounting-addons']:
        os.chdir('odoo-accounting-addons')
        print(os.getcwd())
        os.system('git fetch')
        os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
        os.chdir('..')
        print(os.getcwd())
        os.system('git add odoo-accounting-addons')
        submodules_updated.append('odoo-accounting-addons')
    
    os.system('git commit -m "[{}][SUB]Updated"'.format(','.join(name for name in submodules_updated)))
    os.system('git push')
    
    if data['repositories'][repo]['pr']:
        print('START PR: {}'.format('git request-pull origin/{} origin/{}'.format(data['repositories'][repo]['branch_update_target'],data['repositories'][repo]['branch_update'])))
        os.system('git request-pull origin/{} origin/{}'.format(data['repositories'][repo]['branch_update_target'],data['repositories'][repo]['branch_update']))
        print('END PR')
    
    if data['repositories'][repo]['validation_pr']:
        print('Validation PR')
    
    os.chdir('..')
    print(os.getcwd())