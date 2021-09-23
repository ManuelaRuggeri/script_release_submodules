#!/bin/env python3

# TODO: add file path as param
# TODO: approve PR using pygithub

import argparse
import logging
import os
import sys
import tempfile
import xmltodict

from github import Github

description = 'Update submodules for odoo-accounting'
version = '%(prog)s 1.0'
usage = '%(prog)s -t githubToken'

_logger = logging.getLogger(__name__)

def options():
    parser = argparse.ArgumentParser(
        usage=usage, description=description
    )
    parser.add_argument('-v', '--version', action='version', version=version)
    parser.add_argument(
        '-t', '--token-gh', dest='token', required=True,
        action='store', nargs='?', help='GitHub token used to create pull request'
    )
    args = parser.parse_args()
    return args

def main():
    args = options()

    path_file_xml = 'settings.xml'
    token = args.token

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
                try:
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
                        head=data['repositories'][repo]['branch_update'],
                        base=data['repositories'][repo]['branch_update_target'],
                    )
                    print('END PR')
                except Exception as error:
                    print("ERROR CREATION PR: {}".format(error)) 
                
            if data['repositories'][repo]['validation_pr'] == "True" and pr != False:
                print('Validation PR')
            
            os.chdir('..')
            print(os.getcwd())
            print('########################################################################')

# così puoi anche chamarlo da altri progs
if __name__ == '__main__':
    main()
