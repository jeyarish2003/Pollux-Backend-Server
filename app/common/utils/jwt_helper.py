import jwt

from datetime import  timedelta

from common.utils.config import config
from common.utils.logger import Logger
from common.utils.error_handler import getPlatformException
from common.utils.date_helper import get_utc_datetime

logger=Logger()

def generate_access_token(user:dict) -> str:

    payload = {
        "userdetails": user,
        "type": "access",
        "iss":config.jwt.ISSUER,
        "iat": get_utc_datetime(),
        "exp": get_utc_datetime() + timedelta(minutes=config.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, config.jwt.SECRET_KEY,algorithm=config.jwt.ALGORITHM)
    return token


def generate_refresh_token(user: dict) -> str:
    payload = {
        "userdetails": user,
        "type": "refresh",
        "iss":config.jwt.ISSUER,
        "iat":  get_utc_datetime(),
        "exp":  get_utc_datetime() + timedelta(days=config.jwt.REFRESH_TOKEN_EXPIRE_DAYS)
    }

    token = jwt.encode(payload, config.jwt.SECRET_KEY, algorithm=config.jwt.ALGORITHM)
    logger.debug(f"Token:{token}")
    return token


def decode_token(token):
        try:
            payload = jwt.decode(
                token,
                config.jwt.SECRET_KEY,
                algorithms=config.jwt.ALGORITHM,
            )
  

            # Validate token issuer
            if payload["iss"] == config.jwt.ISSUER:
                # Return the subject (user) if valid
                return payload["userdetails"], None, None

            errordetails = getPlatformException(401, "authenticate", "Issuer for the token is invalid")
            return (None, 401, errordetails)

        # Raise HTTP exception if token has expired
        except jwt.ExpiredSignatureError:
            errordetails = getPlatformException(401, "authenticate", "Token expired")
            return (None, 401, errordetails)

        # Raise HTTP exception if token is invalid
        except jwt.InvalidTokenError:
            errordetails = getPlatformException(401, "authenticate", "Invalid token")
            return (None, 401, errordetails)

        except Exception as error:
            logger.error("Error in decode jwt token: {0}", str(error))
            errordetails = getPlatformException(401, "authenticate", "Invalid token")
            return (None, 401, errordetails)