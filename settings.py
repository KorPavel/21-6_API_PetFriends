import os
from os import path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')
invalid_email = '55555@mail.ru'
invalid_password = '55555'
# ------------------------------
log_path = path.join(path.dirname(__file__), 'logs').replace('\\', '/')
log_file = f'log_{datetime.now().strftime("%Y%m%d")}.txt'