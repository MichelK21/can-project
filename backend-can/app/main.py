from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import get_db
from .models import Team, Match
from .seed import init_db, run_seed

app = FastAPI(title="CAN API", version="0.1.0")


# CORS pour Vue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Init DB au démarrage
@app.on_event("startup")
def startup():
    init_db()


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Seed DB
@app.post("/admin/seed")
def seed(db: Session = Depends(get_db)):
    return run_seed(db)


# Teams
@app.get("/teams")
def list_teams(db: Session = Depends(get_db)):
    rows = db.scalars(select(Team).order_by(Team.name)).all()

    return [
        {
            "id": t.id,
            "name": t.name,
            "code": t.code,
        }
        for t in rows
    ]


# Matches
@app.get("/matches")
def list_matches(db: Session = Depends(get_db)):
    rows = db.scalars(select(Match).order_by(Match.kickoff_at)).all()

    return [
        {
            "id": m.id,
            "group": m.group,
            "kickoffAt": m.kickoff_at.isoformat(),
            "homeTeamId": m.home_team_id,
            "awayTeamId": m.away_team_id,
            "homeScore": m.home_score,
            "awayScore": m.away_score,
            "status": m.status,
        }
        for m in rows
    ]