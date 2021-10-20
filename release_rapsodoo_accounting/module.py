#!/bin/env python3

# TODO: Approve PR using pygithub
# TODO: Aggiungere i file di log

import argparse
import logging
import os
import sys
import tempfile
import xmltodict

from github import Github

description = 'Update submodules for rapsodoo-accounting'
version = '%(prog)s 1.0'
usage = '%(prog)s -t githubToken [-f path_file_xml]'

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
    parser.add_argument(
        '-f', '--file-path', dest='path_file_xml', required=False,
        action='store', nargs='?', help="Path of settings.xml file, if you don't pass it default is 'settings.xml'" 
    )
    args = parser.parse_args()
    return args

def main():
    args = options()

    path_file_xml = 'settings.xml' if not bool(args.path_file_xml) else args.path_file_xml
    token = args.token

    with open(path_file_xml, 'r') as myfile:
        data = xmltodict.parse(myfile.read())

    for repo in data['repositories']:
        if data['repositories'][repo]['active'] == "True":
            print("----->{}<-----".format(data['repositories'][repo]['name']))
            os.chdir('{}/{}'.format(data['repositories'][repo]['organizzazione'], data['repositories'][repo]['name']))
            print(os.getcwd())
            os.system('git pull')
            os.system('git checkout {}'.format(data['repositories'][repo]['branch_update_target']))
            os.system('git submodule update')
            
            submodules_updated = []
            for submodule in data['repositories'][repo]['submodules']:
                if data['repositories'][repo]['submodules'][submodule] == "True":
                    os.chdir(submodule)
                    print(os.getcwd())
                    os.system('git fetch')
                    os.system('git merge origin/{}'.format(data['repositories'][repo]['branch_update_target']))
                    os.chdir('..')
                    print(os.getcwd())
                    os.system('git add {}'.format(submodule))
                    submodules_updated.append(submodule)
            
            os.system('git commit -m "[{}][SUB]Updated"'.format(','.join(name for name in submodules_updated)))
            os.system('git push')
            
            os.chdir('../..')
            print(os.getcwd())
            print('########################################################################')

# cosi puoi anche chamarlo da altri progs
if __name__ == '__main__':
    main()

#######
    # # setup logging
    # if not os.path.isdir(log_dir_name):
    #     os.mkdir(log_dir_name)
    # logfile = "listAWSresources_{:%Y%m%d}.log".format(date.today())
    # logfile = os.path.join(log_dir_name, logfile)
    # logger = logging.getLogger('global log')
    # logger.setLevel(logging.DEBUG)

    # log_handler = FileHandler(logfile)
    # log_handler = TimedRotatingFileHandler(logfile, when='W6')
    # # create formatter and add it to the handlers
    # log_formatter = logging.Formatter(
    #     '%(asctime)s - %(levelname)s - %(message)s'
    # )
    # log_handler.setFormatter(log_formatter)
    # log_handler.setLevel(logging.DEBUG)

    # logger.addHandler(log_handler)

# Use
#        logger.info(
#            "Writing file {} for {}".format(filename, client)
