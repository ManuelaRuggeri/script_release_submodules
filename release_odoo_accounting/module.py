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
        cmd = 'cd {}'.format(data['repositories'][repo]['name'])
        print(cmd)
        os.system(cmd)
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
        if len(submodules_updated) > 0:
            os.system('git commit -m "[{}][SUB]Updated"'.format(','.join(name for name in submodules_updated)))
            os.system('git push')
        os.system('cd')