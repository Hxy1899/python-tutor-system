from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import code
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(code.router, prefix=f"{settings.API_V1_STR}/code", tags=["Code Management"])
from app.api.v1 import assignment, auth, stats
app.include_router(assignment.router, prefix=f"{settings.API_V1_STR}/assignments", tags=["Assignments"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(stats.router, prefix=f"{settings.API_V1_STR}/stats", tags=["Stats"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Python Tutor System API"}
