from werkzeug.datastructures import FileStorage
from datetime import datetime
from pytz import timezone
import os
import uuid

def get_env(name):
    try: 
        return os.environ[name]
    except KeyError:        
        import config
        return config.config[name]

def env_type():
    try:
        return os.environ['ENV']
    except KeyError: 
        return 'dev'

def file_validate(files, ALLOWED_EXTENSIONS):
    for file in files:
        if isinstance(file, FileStorage):
            filename = file.filename.lower()
            if filename.endswith(tuple(ALLOWED_EXTENSIONS)):
                pass
            else:
                print('File extension not supported')
                return False
        else:
            print('No files selected')
            return False
    return True

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