
from common.utils.date_helper import get_utc_datetime




def getPlatformException(status_code,apiname, message,code=None):
    response_data = {
        "responder": {
            "name": apiname,
            "version": "1.0",
            "timestamp": get_utc_datetime().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "message": message,
    }

    # Map status codes to appropriate messages
    status_messages = {
        200: "No Data Found",
        204: "No Content: The request was fulfilled and there is no additional content to send",
        400: "Bad Request: The request payload was invalid",
        401: "Unauthorized",
        403: "Forbidden: Permission was denied",
        404: "Not Found",
        405: "Method Not Allowed",
        408: "Request Timeout",
        409:"Duplicate Entry",
        410: "Gone: The page is no longer available and there is no forwarding address",
        422: "Unprocessable Entity: The request syntax is invalid",
        498: "Invalid Token",
        500: "Internal Server Error: There was an internal server error",
        503: "Service Unavailable: The service is unavailable",
        504: "Gateway Timeout: The deadline was exceeded",
    }

    if code:
        response_data["status_code"]=code
    status_message = status_messages.get(status_code)
    response_data["status"] = status_message

    return response_data
