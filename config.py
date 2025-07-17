class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:contraseña@localhost/farmedic'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'tu_clave_secreta'