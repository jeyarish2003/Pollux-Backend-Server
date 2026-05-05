import datetime
from typing import Annotated, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class requesterDetails(BaseModel):
    name: str
    version: str
    timestamp: datetime.datetime
    requestedby: Optional[str] = None


class Data(BaseModel):
    mobile: str = Field(..., max_length=10, pattern=r'^\d{10}$')
    otp: str = Field(..., max_length=6)
   

class verifyOtp(BaseModel):
    requestname: Annotated[str, Field(pattern=r"^[a-zA-Z_ ]+$")]
    requester: requesterDetails
    data: Data
     

class verifyOtpResponder(BaseModel):
    name: str
    version: str
    timestamp: datetime.datetime


class tokenData(BaseModel):
    accesstoken: str
    refreshtokenexpires: datetime.datetime
    accesstokenexpires: datetime.datetime
    refreshtoken: str
    tokentype: str
    id: UUID
    userrole:str
    roleid:UUID
    firstname:str
    lastname:str
    title:str
    gender:str
    birthdate:datetime.date
    email:EmailStr
    preference:dict
    mobile:str

    
    
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
