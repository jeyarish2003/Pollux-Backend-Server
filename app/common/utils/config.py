class config:
       
    class Redis:
        # host="pollux_redis"
        # port=6379
        host="localhost"
        port=5031
      
    class postgres:
        # host="pollux_postgres"
        # port=5432
        host="localhost"
        port=5433
        user_name="pollux_user"
        password="pollux_pass"
        db_name="pollux_db"

    class jwt:
        SECRET_KEY = "your-super-secret-key"   
        ALGORITHM = "HS256"
        ISSUER="Poll@x"
        ACCESS_TOKEN_EXPIRE_MINUTES = 43500
        REFRESH_TOKEN_EXPIRE_DAYS = 30

