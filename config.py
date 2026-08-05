from urllib.parse import quote_plus


class Config:

    SECRET_KEY = "college-timetable-secret-key"

    DB_USERNAME = "root"
    DB_PASSWORD = quote_plus("Ancy*2106")
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "college_timetable"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
