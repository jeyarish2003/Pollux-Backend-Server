from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware




from dependencies.dependencies import verifyAuth, postgres_helper as pg

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔼 Startup
    await pg.init_pool()
    yield
    # 🔽 Shutdown
    await pg.close_pool()

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Who is allowed to make requests
    allow_credentials=True, # Allow cookies/auth headers
    allow_methods=["*"],    # Which HTTP methods are allowed (GET, POST, etc.)
    allow_headers=["*"],    # Which headers can be included in the request
)


# Include your route modules here
from routes.auth import auth
app.include_router(auth.router)
