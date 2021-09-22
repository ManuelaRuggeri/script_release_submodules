# -*- coding: utf-8 -*-

import sys
import os
import xmltodict
import tempfile
import logging
from github import Github

_logger = logging.getLogger(__name__)

if len(sys.argv) > 1 and sys.argv[1] and sys.argv[2]:
    path_file_xml = 'settings.xml'
    token = sys.argv[2]
else:
    path_file_xml = os.path.join(tempfile.gettempdir(), 'settings.xml')
    token = False

print('path_file_xml: {}'.format(path_file_xml))

with open(path_file_xml, 'r') as myfile:
    data = xmltodict.parse(myfile.read())

for repo in data['repositories']:
    if data['repositories'][repo]['active'] == "True":
        os.chdir('{}'.format(data['repositories'][repo]['name']))
        print(os.getcwd())
        os.system('git checkout {}'.format(data['repositories'][repo]['branch_update']))
        os.system('git pull')
        os.system('git submodule update')
        submodules_updated = []
           
        if data['repositories'][repo]['submodules']['odoo-accounting'] == "True":
            os.chdir('odoo-accounting')
            print(os.getcwd())
            os.system('git fetch')
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            os.chdir('..')
            print(os.getcwd())
            os.system('git add odoo-accounting')
            submodules_updated.append('odoo-accounting')
        
        if data['repositories'][repo]['submodules']['odoo-accounting-enterprise'] == "True":
            os.chdir('odoo-accounting-enterprise')
            print(os.getcwd())
            os.system('git fetch')
            os.system('git merge origin/{}'.format(data['repositories'][repo]['version']))
            os.chdir('..')
            print(os.getcwd())
            os.system('git add odoo-accounting-enterprise')
            submodules_updated.append('odoo-accounting-enterprise')
        
        if data['repositories'][repo]['submodules']['odoo-accounting-addons'] == "True":
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
        
        pr = False
        if data['repositories'][repo]['pr'] == "True" and token != False:
            print('START PR')
            gh = Github(token)
            print('Token: {}'.format(token))
            name_repo = "saydigital/{}".format(data['repositories'][repo]['name'])
            print('Name repo: {}'.format(name_repo))
            remote_repo = gh.get_repo(name_repo)
            print('Repo: {}'.format(remote_repo))
            print('Creation PR')
            pr = remote_repo.create_pull(
                title="PR odoo-accounting",
                body="PR odoo-accounting",
                head=data['repositories'][repo]['branch_update_target'],
                base=data['repositories'][repo]['branch_update'],
            )
            print('END PR')
            
        if data['repositories'][repo]['validation_pr'] == "True" and pr != False:
            print('Validation PR')
        
        os.chdir('..')
        print(os.getcwd())
        print('########################################################################')