from werkzeug.datastructures import FileStorage
from openpyxl.styles import Border, Side
from datetime import datetime
from pytz import timezone
import os
import csv
import uuid

#Get environment variables dependent on environment
def get_env(name):
    try: 
        return os.environ[name]
    except KeyError:        
        import config
        return config.config[name]

#Return environment type
def env_type():
    try:
        return os.environ['ENV']
    except KeyError: 
        return 'dev'

#Validate file extension
def file_validate(files, ALLOWED_EXTENSIONS):
    for file in files:
        if isinstance(file, FileStorage):
            filename = file.filename.lower()
            if filename.endswith(tuple(ALLOWED_EXTENSIONS)):
                pass
            else:
                return False
        else:
            return False
    return True

#Validate format of csv files
def csv_validate(files, allowed_size):
    error_message = 'File format not supported!'
    for file in files:
        lines = file.read().decode('UTF-8').splitlines(True)
        reader = csv.reader(lines, delimiter='\t')
        if len(next(reader)) == allowed_size:
            pass
        else:
            return error_message
    return True

#Create s3 folder name with time dependent on environment
def create_folder_name():
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

#Create cell border style function
def cell_border(left, right, top, bottom):
    border = Border(
        left=Side(border_style=left), 
        right=Side(border_style=right), 
        top=Side(border_style=top), 
        bottom=Side(border_style=bottom))
    return border

#Set border style function
def set_border(ws, border, min_row, max_row, min_col, max_col):
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            cell.border = border

#Set number format function
def set_format(ws, format, min_row, max_row, min_col, max_col):
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            cell.number_format = format  