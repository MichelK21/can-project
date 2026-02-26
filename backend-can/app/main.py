from fastapi import FastAPI, Depends, Header, HTTPException
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
def health(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    return {"status": "ok"}


# Seed DB
@app.post("/admin/seed")
def seed(db: Session = Depends(get_db)):
    return run_seed(db)


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

@app.get("/standings")
def standings(db: Session = Depends(get_db)):
   
    finished = db.scalars(
        select(Match).where(Match.status == "FT")
    ).all()

    teams = db.scalars(select(Team)).all()
    team_by_id = {t.id: t for t in teams}

   
    groups: dict[str, dict[int, dict]] = {}

    def ensure_team(group: str, team_id: int):
        groups.setdefault(group, {})
        groups[group].setdefault(team_id, {
            "teamId": team_id,
            "team": team_by_id[team_id].name,
            "code": team_by_id[team_id].code,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "points": 0,
            "gf": 0,
            "ga": 0,
            "gd": 0,
        })
        return groups[group][team_id]

    for m in finished:
        
        if m.home_score is None or m.away_score is None:
            continue

        g = m.group
        home = ensure_team(g, m.home_team_id)
        away = ensure_team(g, m.away_team_id)

        home["played"] += 1
        away["played"] += 1

        home["gf"] += m.home_score
        home["ga"] += m.away_score

        away["gf"] += m.away_score
        away["ga"] += m.home_score

        if m.home_score > m.away_score:
            home["wins"] += 1
            away["losses"] += 1
            home["points"] += 3
        elif m.home_score < m.away_score:
            away["wins"] += 1
            home["losses"] += 1
            away["points"] += 3
        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

   
    result: dict[str, list[dict]] = {}
    for g, table in groups.items():
        rows = list(table.values())
        for r in rows:
            r["gd"] = r["gf"] - r["ga"]

        rows.sort(key=lambda x: (x["points"], x["gd"], x["gf"]), reverse=True)
        result[g] = rows

    return result

