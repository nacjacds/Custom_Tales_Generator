DB_USERNAME = "admin"
DB_PASSWORD = "gt6fyhV$c&"
DB_HOST = "bd2405.cviiwsisi7rg.us-east-1.rds.amazonaws.com"
DB_PORT = 3306
DB_NAME = "bd2405"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"