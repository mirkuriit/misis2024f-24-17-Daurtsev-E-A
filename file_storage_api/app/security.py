from authx import AuthX, AuthXConfig
from file_storage_api.config import config

import datetime as dt

auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = config.JWT_SECRET_KEY
auth_config.JWT_ACCESS_COOKIE_NAME = config.JWT_ACCESS_COOKIE_NAME
auth_config.JWT_TOKEN_LOCATION = ["cookies"]
auth_config.JWT_ACCESS_TOKEN_EXPIRES = dt.timedelta(minutes=30)

security = AuthX(config=auth_config)