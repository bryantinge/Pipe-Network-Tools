from werkzeug.datastructures import FileStorage
from openpyxl.styles import Border, Side
from datetime import datetime
from pytz import timezone
import os
import csv
import uuid


def get_env(name):
    '''Get environment variables dependent on environment'''
    try:
        return os.environ[name]
    except KeyError:
        import config
        return config.config[name]


def env_type():
    '''Return environment type'''
    try:
        return os.environ['ENV']
    except KeyError:
        return 'dev'


def create_folder_name():
    '''Create s3 folder name with time dependent on environment'''
    time_format = '%Y-%m-%d_%H:%M:%S'
    if env_type() == 'prod':
        now_utc = datetime.now(timezone('UTC'))
        now_est = now_utc.astimezone(timezone('US/Eastern'))
        timestamp = now_est.strftime(time_format)
    else:
        now_est = datetime.now()
        timestamp = now_est.strftime(time_format)
    folder_name = ''.join([timestamp, '_', str(uuid.uuid4().hex[:16])])
    return folder_name


def cell_border(left, right, top, bottom):
    '''Create cell border style function'''
    border = Border(
        left=Side(border_style=left),
        right=Side(border_style=right),
        top=Side(border_style=top),
        bottom=Side(border_style=bottom))
    return border


def set_border(ws, border, min_row, max_row, min_col, max_col):
    '''Set border style function'''
    for row in ws.iter_rows(
        min_row=min_row, max_row=max_row,
        min_col=min_col, max_col=max_col
    ):
        for cell in row:
            cell.border = border


def set_format(ws, format, min_row, max_row, min_col, max_col):
    '''Set number format function'''
    for row in ws.iter_rows(
        min_row=min_row, max_row=max_row,
        min_col=min_col, max_col=max_col
    ):
        for cell in row:
            cell.number_format = format


def filestorage_validate(files):
    '''Validate files are FileStorage class'''
    for file in files:
        if isinstance(file, FileStorage):
            pass
        else:
            return False
    return True


def file_nonempty_validate(files):
    '''Validate files are nonempty'''
    for file in files:
        filename = file.filename.lower()
        if filename == '':
            return False
        else:
            pass
    return True


def file_ext_validate(files):
    '''Validate file extension'''
    allowed_extensions = ['.txt']
    for file in files:
        filename = file.filename.lower()
        if filename.endswith(tuple(allowed_extensions)):
            pass
        else:
            return False
    return True


def csv_validate(files, csv_columns):
    '''Validate format of csv files'''
    for file in files:
        lines = file.read().decode('UTF-8').splitlines(True)
        reader = csv.reader(lines, delimiter='\t')
        if len(next(reader)) == csv_columns:
            pass
        else:
            return False
    return True


def form_validate(data, csv_columns):
    if not filestorage_validate(data):
        flash_message = 'File format not supported!'
        return flash_message
    if not file_nonempty_validate(data):
        flash_message = 'No files selected!'
        return flash_message
    if not file_ext_validate(data):
        flash_message = 'File format not supported!'
        return flash_message
    if not csv_validate(data, csv_columns):
        flash_message = 'File format not supported!'
        return flash_message
    return 'validated'
