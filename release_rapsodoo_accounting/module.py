#!/bin/env python3

# TODO: Approve PR using pygithub
# TODO: Aggiungere nel metodo create_log_and_print i vari tipi di errore [info,warning,error]

import argparse
import logging
import logging.handlers
import os
import sys
import tempfile
import xmltodict
from datetime import date

from github import Github

description = 'Update submodules for rapsodoo-accounting'
version = '%(prog)s 1.0'
usage = '%(prog)s -t githubToken [-f path_file_xml] [-l log_dir_name]'

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
    parser.add_argument(
        '-l', '--log-dir-path', dest='log_dir_name', required=False,
        action='store', nargs='?', help="Path of dir log , if you don't pass it default is 'dir_log'" 
    )
    args = parser.parse_args()
    return args

def create_log_and_print(logger, msg):
    print(msg)
    logger.info(msg)

def setup_log(log_dir_name):
    if not os.path.isdir(log_dir_name):
        os.mkdir(log_dir_name)
    logfile = "{}_{:%Y%m%d}.log".format('release_rapsodoo_accounting',date.today())
    logfile = os.path.join(log_dir_name, logfile)
    logger = logging.getLogger('global log')
    logger.setLevel(logging.DEBUG)
    log_handler = logging.FileHandler(logfile)
    log_handler = logging.handlers.TimedRotatingFileHandler(logfile, when='W6')
    # create formatter and add it to the handlers
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)
    return logger
    
def main():
    args = options()
    
    log_dir_name = 'dir_log' if not bool(args.log_dir_name) else args.log_dir_name
    path_file_xml = 'settings.xml' if not bool(args.path_file_xml) else args.path_file_xml
    token = args.token
    
    logger = setup_log(log_dir_name)
    
    with open(path_file_xml, 'r') as myfile:
        data = xmltodict.parse(myfile.read())

    for repo in data['repositories']:
        if data['repositories'][repo]['active'] == "True":
            create_log_and_print(logger, "----->{}<-----".format(data['repositories'][repo]['name']))
            os.chdir('{}/{}'.format(data['repositories'][repo]['organizzazione'], data['repositories'][repo]['name']))
            create_log_and_print(logger, os.getcwd())
            os.system('git pull')
            os.system('git checkout {}'.format(data['repositories'][repo]['branch_update_target']))
            os.system('git submodule update')
            
            submodules_updated = []
            for submodule in data['repositories'][repo]['submodules']:
                if data['repositories'][repo]['submodules'][submodule] == "True":
                    os.chdir(submodule)
                    create_log_and_print(logger, os.getcwd())
                    os.system('git fetch')
                    os.system('git merge origin/{}'.format(data['repositories'][repo]['branch_update_target']))
                    os.chdir('..')
                    create_log_and_print(logger, os.getcwd())
                    os.system('git add {}'.format(submodule))
                    submodules_updated.append(submodule)
            
            os.system('git commit -m "[{}][SUB]Updated"'.format(','.join(name for name in submodules_updated)))
            os.system('git push')
            
            os.chdir('../..')
            create_log_and_print(logger, os.getcwd())
            create_log_and_print(logger, '########################################################################')
# cosi puoi anche chamarlo da altri progs
if __name__ == '__main__':
    main()