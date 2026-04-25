import datetime
from typing import Annotated, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class Data(BaseModel):
    phone: str = Field(..., max_length=10, pattern=r'^\d{10}$')
    otp: str = Field(..., max_length=4)
   

class verifyOtp(BaseModel):
    requestname: Annotated[str, Field(pattern=r"^[a-zA-Z_ ]+$")]
    data: Data
     

class verifyOtpResponder(BaseModel):
    name: str
    version: str
    timestamp: datetime.datetime

class tokenData(BaseModel):
    accesstoken: str
    refreshtoken: str
    tokentype: str
    userid: UUID
    userrole:str
    roleid:UUID
    username:str
    
    
class verifyOtpResponse(BaseModel):
    responder: verifyOtpResponder
    status: str
    message: str
    data:tokenData


# Example request JSON
verifyOtpRequestJson = {
    "requestname": "verify_otp",
    "data": {
       "phone":"1234567890",
       "otp":"1234"
    }
}
