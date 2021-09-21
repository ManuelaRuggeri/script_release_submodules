# -*- coding: utf-8 -*-

import sys
import os
import xmltodict
import tempfile
import logging

_logger = logging.getLogger(__name__)

stop_run = False

if len(sys.argv) > 1 and sys.argv[1]:
    if len(sys.argv) != 3:
        print('Inserire questi parametri: True percorso_delle_cartelle_dei_progetti')
        stop_run = True
    path_file_xml = 'settings.xml'
    if not stop_run:
        folder_projects = sys.argv[2]
else:
    path_file_xml = os.path.join(tempfile.gettempdir(), 'settings.xml')
    folder_projects = ''

if not stop_run:
    print('path_file_xml: {}'.format(path_file_xml))
    
    with open(path_file_xml, 'r') as myfile:
        data = xmltodict.parse(myfile.read())
    print(os.getcwd())
    os.system('cd {}'.format(folder_projects))
    print(os.getcwd())
    
    for repo in data['repositories']:
        os.system('cd {}'.format(data['repositories'][repo]['name']))
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
            os.system('cd odoo-accounting')
            print(os.getcwd())
            os.system('git fetch')
            print(os.getcwd())
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            print(os.getcwd())
            os.system('cd ..')
            print(os.getcwd())
            os.system('git add odoo-accounting')
            print(os.getcwd())
            submodules_updated.append('odoo-accounting')
            print(os.getcwd())
        if data['repositories'][repo]['submodules']['odoo-accounting-enterprise']:
            os.system('cd odoo-accounting-enterprise')
            print(os.getcwd())
            os.system('git fetch')
            print(os.getcwd())
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            print(os.getcwd())
            os.system('cd ..')
            print(os.getcwd())
            os.system('git add odoo-accounting-enterprise')
            print(os.getcwd())
            submodules_updated.append('odoo-accounting-enterprise')
        if data['repositories'][repo]['submodules']['odoo-accounting-addons']:
            os.system('cd odoo-accounting-addons')
            print(os.getcwd())
            os.system('git fetch')
            print(os.getcwd())
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            print(os.getcwd())
            os.system('cd ..')
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
        os.system('cd')
        print(os.getcwd())