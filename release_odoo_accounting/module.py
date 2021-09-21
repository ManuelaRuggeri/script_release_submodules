# -*- coding: utf-8 -*-

import sys
import os
import xmltodict
import tempfile
import logging

_logger = logging.getLogger(__name__)

stop_run = False

if len(sys.argv) > 1 and sys.argv[1]:
    path_file_xml = 'settings.xml'
else:
    path_file_xml = os.path.join(tempfile.gettempdir(), 'settings.xml')

if not stop_run:
    print('path_file_xml: {}'.format(path_file_xml))
    
    with open(path_file_xml, 'r') as myfile:
        data = xmltodict.parse(myfile.read())
    
    for repo in data['repositories']:
        os.chdir('{}'.format(data['repositories'][repo]['name']))
        print(os.getcwd())
        os.system('git checkout {}'.format(data['repositories'][repo]['branch_update']))
        print(os.getcwd())
        os.system('git pull')
        print(os.getcwd())
        os.system('git submodule update')
        print(os.getcwd())
        submodules_updated = []
           
        if data['repositories'][repo]['submodules']['odoo-accounting']:
            print(os.getcwd())
            os.chdir('odoo-accounting')
            print(os.getcwd())
            os.system('git fetch')
            print(os.getcwd())
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            print(os.getcwd())
            os.chdir('..')
            print(os.getcwd())
            os.system('git add odoo-accounting')
            print(os.getcwd())
            submodules_updated.append('odoo-accounting')
            print(os.getcwd())
        if data['repositories'][repo]['submodules']['odoo-accounting-enterprise']:
            os.chdir('odoo-accounting-enterprise')
            print(os.getcwd())
            os.system('git fetch')
            print(os.getcwd())
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            print(os.getcwd())
            os.chdir('..')
            print(os.getcwd())
            os.system('git add odoo-accounting-enterprise')
            print(os.getcwd())
            submodules_updated.append('odoo-accounting-enterprise')
        if data['repositories'][repo]['submodules']['odoo-accounting-addons']:
            os.chdir('odoo-accounting-addons')
            print(os.getcwd())
            os.system('git fetch')
            print(os.getcwd())
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            print(os.getcwd())
            os.chdir('..')
            print(os.getcwd())
            os.system('git add odoo-accounting-addons')
            print(os.getcwd())
            submodules_updated.append('odoo-accounting-addons')
        if len(submodules_updated) > 0:
            print(os.getcwd())
            os.system('git commit -m "[{}][SUB]Updated"'.format(','.join(name for name in submodules_updated)))
            print(os.getcwd())
            os.system('git push')
            print(os.getcwd())
        print(os.getcwd())