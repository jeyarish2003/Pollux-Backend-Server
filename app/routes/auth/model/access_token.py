import datetime
from typing import Annotated, Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field


class Data(BaseModel):
    refreshtoken: str
   
class accesstoken(BaseModel):
    requestname: Annotated[str, Field(pattern=r"^[a-zA-Z_ ]+$")]
    data: Data
     

class accesstokenResponder(BaseModel):
    name: str
    version: str
    timestamp: datetime.datetime

class tokenData(BaseModel):
    accesstoken: str
 
    
class accesstokenResponse(BaseModel):
    responder: accesstokenResponder
    status: str
    message: str
    data:tokenData


