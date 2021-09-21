# -*- coding: utf-8 -*-

import sys
import os
import xmltodict
import tempfile
import untangle

if len(sys.argv) > 1 and sys.argv[1]:
    path_file_xml = 'settings.xml'
else:
    path_file_xml = os.path.join(tempfile.gettempdir(), 'settings.xml')

with open(path_file_xml, 'r') as myfile:
    data = xmltodict.parse(myfile.read())


for repo in data['repositories']:
    os.system('cd {}'.format(data['repositories'][repo]['name']))
    os.system('git checkout {}'.format(data['repositories'][repo]['branch_update']))
    os.system('git pull')
    os.system('git submodule update')
       
    submodules_updated = []
       
    if data['repositories'][repo]['submodules']['odoo-accounting']:
        os.system('cd odoo-accounting')
        os.system('git fetch')
        os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
        os.system('cd ..')
        os.system('git add odoo-accounting')
        submodules_updated.append('odoo-accounting')
    if data['repositories'][repo]['submodules']['odoo-accounting-enterprise']:
        os.system('cd odoo-accounting-enterprise')
        os.system('git fetch')
        os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
        os.system('cd ..')
        os.system('git add odoo-accounting-enterprise')
        submodules_updated.append('odoo-accounting-enterprise')
    if data['repositories'][repo]['submodules']['odoo-accounting-addons']:
        os.system('cd odoo-accounting-addons')
        os.system('git fetch')
        os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
        os.system('cd ..')
        os.system('git add odoo-accounting-addons')
        submodules_updated.append('odoo-accounting-addons')
    os.system('git commit -m "[{}][SUB]Updated"'.format(','.join(name for name in submodules_updated)))
    os.system('git push')
    os.system('cd')