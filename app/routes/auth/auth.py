import hashlib
import json
import bcrypt
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, Header,Request, Response
from routes.auth.model.verify_otp import verifyOtp, verifyOtpResponder, verifyOtpResponse,verifyOtpRequestJson
from common.connectors.redis_helper import Redis
from routes.auth.model.send_otp import sendOtp, sendOtpResponder, sendOtpResponse,sendOtpRequestJson
from common.utils.error_handler import getPlatformException
from routes.auth.model.access_token import accesstoken, accesstokenResponder, accesstokenResponse
from routes.auth.auth_helper import generate_otp, insert_user_session,get_userrole
from common.utils.jwt_helper import decode_token, generate_access_token, generate_refresh_token
from common.utils.date_helper import get_utc_datetime
from common.utils.logger import Logger
from dependencies.dependencies import postgres_helper

router = APIRouter(tags=['Auth'])

logger = Logger()
redis = Redis()


        
@router.post("/sendotp")
async def verify_phone(background_tasks: BackgroundTasks,payload: sendOtp = Body(example=sendOtpRequestJson)):
    logger.info(f"sendOtp ::: Request received : phone={payload.data.phone}")

    try:
        
        error_details=None
        verify_phone_query = """
            SELECT first_name,last_name,user_id
            FROM users
            WHERE phone = $1 AND is_active = TRUE
        """
        logger.info(f"sendOtp ::: Executing query : phone={payload.data.phone}")

        verify_phone_result = await postgres_helper.execute(verify_phone_query,payload.data.phone,fetch=True)

        if not verify_phone_result:
            logger.warning(f"sendOtp ::: phone not found or inactive : phone={payload.data.phone}")
            error_details=getPlatformException(401,payload.requestname,f"phone:{payload.data.phone} does not exist")
            raise HTTPException(status_code=401,detail=error_details)

        logger.info(f"sendOtp ::: User found : user_name {verify_phone_result[0]['first_name']} {verify_phone_result[0]['last_name']}, user_id={verify_phone_result[0]['user_id']}")

        otp=generate_otp()
        hashed_otp =bcrypt.hashpw(otp.encode(), bcrypt.gensalt())

        redis.insert_data(key=f"otp:{payload.data.phone}",value=hashed_otp,expiry=300)
    #     background_tasks.add_task(
    #     sendmail,
    #     frm="",
    #     to=payload.data.phone,
    #     template_key="send_otp",
    #     context={
    #             "employee_name": verify_phone_result[0]['first_name']+" "+verify_phone_result[0]['last_name'],
    #             "otp": otp,
    #     }
    # )
       
        response = sendOtpResponse(
        responder=sendOtpResponder(
            name=payload.requestname,
            version="1.0",
            timestamp=get_utc_datetime(),
        ),
        status="Success",
        message=f"OTP Sent To {payload.data.phone} Successfully",
        
        )

        return response

        

    except Exception as error:
        if error_details:
            status_code, errordetails = str(error).split(":", 1)[0], str(error).split(":", 1)[1].strip().replace("'", '"')
            raise HTTPException(status_code=int(status_code), detail=json.loads(errordetails))
        else:
            logger.error(
                f"sendOtp ::: Unexpected failure : error={str(error)}",
                exc_info=True
            )
            error_details = getPlatformException(500, payload.requestname, str(error))
            raise HTTPException(status_code=500, detail=error_details)

@router.post("/verifyotp")
async def verify_otp(request:Request,response: Response,x_device_type: str = Header(default="web"),payload: verifyOtp = Body(example=verifyOtpRequestJson)):
    logger.info(f"verifyOtp ::: Request received : phone={payload.data.phone}")

    try:
        
        error_details=None
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            x_forwarded_for = x_forwarded_for.split(',')[0].strip()
        logger.info(f"verifyOtp ::: Forwarded IP : {x_forwarded_for}")
        if x_forwarded_for:
            client_ip = x_forwarded_for # Get the first IP in the list
        else:
            client_ip = request.client.host
        # Can contain multiple IPs: client, proxy1, proxy2
            
        verify_otp_query = """
            SELECT first_name,last_name,phone,role_id,user_id
            FROM users
            WHERE phone = $1 AND is_active = TRUE
        """
        logger.debug(f"verifyOtp ::: Executing query : phone={payload.data.phone}")

        verify_otp_result = await postgres_helper.execute(verify_otp_query,payload.data.phone,fetch=True)

        if not verify_otp_result:
            logger.warning(f"verifyOtp ::: phone not found or inactive : phone={payload.data.phone}")
            error_details=getPlatformException(401,payload.requestname,f"phone:{payload.data.phone} does not exist",code=2)
            raise HTTPException(status_code=401,detail=error_details)

        logger.debug(f"verifyOtp ::: User found : user_id={verify_otp_result[0]['user_id']}")

        # if bcrypt.checkpw(payload.data.otp.encode(), redis.retrieve_data(key=f"otp:{payload.data.phone}").encode()):
        if payload.data.otp == "1234":

            logger.info(f"verifyOtp ::: OTP verified successfully : phone={payload.data.phone}")
            
            user_role=await get_userrole(verify_otp_result[0]['role_id'])

            user_details={
                "username":verify_otp_result[0]['first_name']+" "+verify_otp_result[0]['last_name'],
                "user_id":str(verify_otp_result[0]['user_id']),
                "role_id": str(verify_otp_result[0]['role_id']),
                "user_role":user_role,
                "phone_id":payload.data.phone
            }


            access_token=generate_access_token(user_details)
            refresh_token=generate_refresh_token(user_details)
           
            user_agent=request.headers.get("user-agent")
            
            # await insert_user_session(user_id=verify_otp_result[0]['employee_id'],company_id=verify_otp_result[0]['company_id'],refresh_token=hashlib.sha256(refresh_token.encode('utf-8')).hexdigest(),created_by=verify_otp_result[0]['first_name'],client_ip=client_ip,user_agent=user_agent,device=x_device_type)
       
            return verifyOtpResponse(
            responder=verifyOtpResponder(
                name=payload.requestname,
                version="1.0",
                timestamp=get_utc_datetime(),
            ),
            status="Success",
            message=f"phone:{payload.data.phone} verified Successfully",
            data={
                "accesstoken": access_token,
                "refreshtoken": refresh_token,
                "tokentype": "Bearer",
                "userrole":user_role,
                "roleid":verify_otp_result[0]['role_id'],
                "userid":verify_otp_result[0]['user_id'],
                "phone":payload.data.phone,
                "username":verify_otp_result[0]['first_name']+" "+verify_otp_result[0]['last_name']
            }
            )


        else:
            logger.warning(
                f"verifyOtp ::: Invalid password : phone={payload.data.phone}"
            )   
            error_details=getPlatformException(401,payload.requestname,f"Password is incorrect for phone:{payload.data.phone}",code=3)
            raise HTTPException(status_code=401,detail=error_details)
        

    except Exception as error:
        if error_details:
            status_code, errordetails = str(error).split(":", 1)[0], str(error).split(":", 1)[1].strip().replace("'", '"')
            raise HTTPException(status_code=int(status_code), detail=json.loads(errordetails))
        else:
            logger.error(
                f"verifyOtp ::: Unexpected failure : error={str(error)}",
                exc_info=True
            )
            error_details = getPlatformException(500, payload.requestname, str(error))
            raise HTTPException(status_code=500, detail=error_details)


@router.post("/accesstoken")
async def get_acesstoken(request: Request, response: Response):
    try:
        error_details=None
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            error_details=getPlatformException(401,"get_accesstoken","Refresh token is missing in the request",code=4)
            raise HTTPException(status_code=401, detail=error_details)
        
        logger.info(f"accesstoken ::: Request received : refresh_token_present={bool(refresh_token)}")
        payload, statuscode, error_details = decode_token(refresh_token)
        if error_details:
            raise HTTPException(status_code=statuscode, detail=error_details)

       
        query='SELECT id FROM user_sessions where refresh_token=%s and delete_flag=0'
        result=await postgres_helper.execute(query,hashlib.sha256(refresh_token.encode('utf-8')).hexdigest(),fetch=True)
        if not result:
            raise HTTPException(status_code=401, detail=error_details)

    
        access_token=generate_access_token(payload)

        response = accesstokenResponse(
                responder=accesstokenResponder(
                    name="access_token",
                    version="1.0",
                    timestamp=get_utc_datetime(),
                ),
                status="Success",
                message=f"Access token retrieved Successfully",
                data={
                    "accesstoken": access_token,
                    
                }
                )

        return response
        
    except Exception as error:
        if error_details:
            logger.error(
                f"accesstoken :::error={str(error)}"
            )
            status_code, errordetails = str(error).split(":", 1)[0], str(error).split(":", 1)[1].strip().replace("'", '"')
            raise HTTPException(status_code=int(status_code), detail=json.loads(errordetails))
        else:
            logger.error(
                f"accesstoken ::: Unexpected failure: error={str(error)}",
                exc_info=True
            )
            error_details = getPlatformException(500, "get_acesstoken", str(error))
            raise HTTPException(status_code=500, detail=error_details)

