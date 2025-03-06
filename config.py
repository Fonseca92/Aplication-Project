import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ac2df92a-66cf-4f47-875b-f5d027c33934')
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://cmsadmin:CMS4dmin@cmss.database.windows.net:1433/cms?'
        'driver=ODBC+Driver+17+for+SQL+Server'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/uploads'
    BLOB_ACCOUNT_NAME = os.environ.get('BLOB_ACCOUNT_NAME')
    BLOB_ACCOUNT_KEY = os.environ.get('BLOB_ACCOUNT_KEY')
    BLOB_CONTAINER_NAME = os.environ.get('BLOB_CONTAINER_NAME')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    AUTHORITY = os.environ.get('AUTHORITY')
    REDIRECT_PATH = os.environ.get('REDIRECT_PATH', '/getAToken')
    SCOPE = os.environ.get('SCOPE', ['User.Read'])
    SESSION_TYPE = 'filesystem'
    BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING')