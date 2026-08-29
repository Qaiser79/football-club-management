from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.organization_router import router as organization_router
from app.routers import club_router
from app.routers import team_router
from app.routers import player_router
from app.routers import match_router
from app.routers import match_squad_router

app = FastAPI(title="Football Club Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message":"Football Club Management API is running!"}

app.include_router(organization_router)
app.include_router(club_router.router)
app.include_router(team_router.router)
app.include_router(player_router.router)
app.include_router(match_router.router)
app.include_router(match_squad_router.router)