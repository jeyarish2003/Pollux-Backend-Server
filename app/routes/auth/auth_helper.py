import secrets
from dependencies.dependencies import postgres_helper as pg




async def get_userrole(userid:int):
    query="SELECT role_name FROM roles WHERE role_id= $1"

    result=await pg.execute(query,userid,fetch=True)

    return result[0]['role_name']

async def insert_user_session(
    user_id: int,
    company_id: int,
    refresh_token: str,
    created_by: str,
    device: str = None,
    client_ip: str = None,
    user_agent: str = None
):
    query = """
       INSERT INTO user_sessions
        (user_id,company_id, device, refresh_token, ip_address, user_agent, created_by)
        VALUES ($1,$2, $3, $4, $5, $6, $7)
        ON DUPLICATE KEY UPDATE
            refresh_token = VALUES(refresh_token),
            ip_address = VALUES(ip_address),
            user_agent = VALUES(user_agent),
            modified_by = VALUES(created_by),
            delete_flag = 0;
            """

    params = (
        user_id,
        company_id,
        device,
        refresh_token,
        client_ip,
        user_agent,
        created_by)
    
    await pg.execute(query, *params)




def generate_otp() -> str:
    return f"{secrets.randbelow(10000):04d}"

