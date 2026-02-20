import json
from sqlalchemy.orm import Session
from sqlalchemy import select
from dateutil.parser import isoparse

from .db import Base, engine
from .models import Team, Match


def init_db():
    Base.metadata.create_all(bind=engine)


def run_seed(db: Session, path: str = "seed/seed.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Teams
    code_to_id: dict[str, int] = {}
    for t in data.get("teams", []):
        team = db.scalar(select(Team).where(Team.code == t["code"]))
        if not team:
            team = Team(name=t["name"], code=t["code"])
            db.add(team)
            db.flush()
        code_to_id[t["code"]] = team.id

    # Matches
    created = 0
    for m in data.get("matches", []):
        kickoff_at = isoparse(m["kickoffAt"])
        home_id = code_to_id[m["homeCode"]]
        away_id = code_to_id[m["awayCode"]]

        exists = db.scalar(
            select(Match).where(
                Match.kickoff_at == kickoff_at,
                Match.home_team_id == home_id,
                Match.away_team_id == away_id,
            )
        )
        if exists:
            continue

        db.add(
            Match(
                group=m["group"],
                kickoff_at=kickoff_at,
                home_team_id=home_id,
                away_team_id=away_id,
                status=m.get("status", "SCHEDULED"),
                home_score=m.get("homeScore"),
                away_score=m.get("awayScore"),
            )
        )
        created += 1

    db.commit()
    return {"ok": True, "matches_created": created}
