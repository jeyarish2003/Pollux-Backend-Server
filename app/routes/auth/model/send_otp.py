import datetime
from typing import Annotated, Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field


class Data(BaseModel):
    phone: str = Field(..., max_length=10, pattern=r'^\d{10}$')

class sendOtp(BaseModel):
    requestname: Annotated[str, Field(pattern=r"^[a-zA-Z_ ]+$")]
    data: Data
     

class sendOtpResponder(BaseModel):
    name: str
    version: str
    timestamp: datetime.datetime

    
class sendOtpResponse(BaseModel):
    responder: sendOtpResponder
    status: str
    message: str



# Example request JSON
sendOtpRequestJson = {
    "requestname": "send_otp",
    "data": {
       "phone":"1234567890"
    }
}
