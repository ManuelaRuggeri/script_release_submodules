#!/bin/env python3

import argparse
import logging
import logging.handlers
import os
import tempfile
import json
from datetime import date
import xlsxwriter

from github import Github

description = 'Export name of invoice and the file name is the number of invoice'
version = '%(prog)s 1.0'
usage = '%(prog)s -f path_file_xml [-l log_dir_name]'

def options():
    parser = argparse.ArgumentParser(
        usage=usage, description=description
    )
    parser.add_argument('-v', '--version', action='version', version=version)
    parser.add_argument(
        '-f', '--file-path', dest='path_file_xml', required=True,
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
    return logger, logfile

def create_file_xlsx(data_list, count_invoice):
    workbook = xlsxwriter.Workbook('{}.xlsx'.format(count_invoice))
    worksheet = workbook.add_worksheet()
    
    worksheet.write(0, 0, 'NumDocumento')
    worksheet.write(0, 1, 'IdCliente')
    worksheet.write(0, 2, 'KTestaDoc')
    worksheet.write(0, 3, 'DataDocumento')
    
    row = 1
    
    for NumDocumento, IdCliente, KTestaDoc, DataDocumento in data_list:
        worksheet.write(row, 0, NumDocumento)
        worksheet.write(row, 1, IdCliente)
        worksheet.write(row, 2, KTestaDoc)
        worksheet.write(row, 3, DataDocumento)
        row += 1
    
    workbook.close()

def main():
    args = options()
    
    log_dir_name = 'dir_log' if not bool(args.log_dir_name) else args.log_dir_name
    path_file_xml = 'settings.xml' if not bool(args.path_file_xml) else args.path_file_xml
    
    logger, logfile = setup_log(log_dir_name)
    
    with open(path_file_xml) as json_file:
        data_json = json.load(json_file)
    
    count_invoice = 0
    data_list = []
    for invoice in data_json:
        element_list = (invoice['NumDocumento'], invoice['IdCliente'], invoice['KTestaDoc'], invoice['DataDocumento'].split('T')[0])
        data_list.append(element_list)
        create_log_and_print(logger, '{}, {}, {}, {}'.format(element_list[0], element_list[1], element_list[2], element_list[3]))
        count_invoice += 1
    
    create_log_and_print(logger, 'Numero invoice: {}'.format(count_invoice))
    create_file_xlsx(data_list, count_invoice)

# cosi puoi anche chamarlo da altri progs
if __name__ == '__main__':
    main()