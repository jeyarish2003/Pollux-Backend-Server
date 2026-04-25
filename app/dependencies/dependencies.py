import json
from typing import Any
from typing_extensions import Annotated
from fastapi import Depends, FastAPI, HTTPException, Header, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from common.utils.error_handler import getPlatformException
from common.utils.jwt_helper import decode_token
from common.utils.logger import Logger

from common.connectors.postgres_helper import PostgresHelper

postgres_helper = PostgresHelper()
security = HTTPBearer()
log = Logger()


def getAuthToken(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    # log.debug("getAuthToken:::Token from request: {0}", token)
    return token


async def verifyAuth(
    token: Annotated[Any, Depends(getAuthToken)],
):
    try:
        statuscode = None
        error_details = None

        userInToken, statuscode, error_details = decode_token(token)

        if userInToken:
            return {"user": userInToken}
        else:
            raise HTTPException(status_code=statuscode, detail=error_details)

    except Exception as error:
        if error_details:
            status_code, errordetails = str(error).split(":", 1)[0], str(error).split(":", 1)[1].strip().replace("'", '"')
            raise HTTPException(status_code=int(status_code), detail=json.loads(errordetails))
        else:
            error_details = getPlatformException(500, "verify_auth", str(error))
            raise HTTPException(status_code=500, detail=error_details)


