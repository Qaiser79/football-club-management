from fastapi import FastAPI
from app.routers.organization_router import router as organization_router
from app.routers import club_router
from app.routers import team_router
from app.routers import player_router
app = FastAPI(title="Football Club Management API")

@app.get("/")
def root():
    return {"message":"Football Club Management API is running!"}

app.include_router(organization_router)
app.include_router(club_router.router)
app.include_router(team_router.router)
app.include_router(player_router.router)