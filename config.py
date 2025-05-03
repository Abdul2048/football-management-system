class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/football'
    SQLALCHEMY_TRACK_MODIFICATIONS = False