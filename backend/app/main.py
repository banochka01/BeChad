from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import jwt
from .database import Base, engine, get_db, settings
from .models import User, RefreshToken, DailyQuest, FriendRequest, Friendship
from .services import ph, verify_password, make_tokens, hash_token, seed_achievements, generate_plan, complete_quest, level_for_xp, coach_reply
Base.metadata.create_all(engine)
app=FastAPI(title="BeChad API", version="0.1.0", openapi_url="/api/v1/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=["*"] if settings.environment=="development" else [], allow_methods=["*"], allow_headers=["*"])
@app.on_event("startup")
def startup():
    db=next(get_db()); seed_achievements(db); db.close()
class Register(BaseModel): email: str; username: str=Field(min_length=3,max_length=40); password: str=Field(min_length=8,max_length=128)
class Login(BaseModel): email: str; password: str
class Onboarding(BaseModel): goals:list[str]; timeBudget:str; intensity:str
class Complete(BaseModel): questId:str; idempotencyKey:str
class Coach(BaseModel): message:str=Field(max_length=1000)
def current(authorization:str=Header(default=""), db:Session=Depends(get_db)):
    try:
        token=authorization.removeprefix("Bearer "); sub=jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], issuer=settings.jwt_issuer)["sub"]
        u=db.get(User,sub); assert u; return u
    except Exception: raise HTTPException(401,"invalid token")
@app.get("/health")
def health(): return {"status":"ok","service":"BeChad"}
@app.get("/ready")
def ready(db:Session=Depends(get_db)): db.execute(__import__('sqlalchemy').text('select 1')); return {"status":"ready"}
@app.get("/api/v1/version")
def version(): return {"name":"BeChad","version":"0.1.0"}
@app.post("/api/v1/auth/register")
def register(r:Register, db:Session=Depends(get_db)):
    if db.query(User).filter((User.email==r.email)|(User.username==r.username)).first(): raise HTTPException(409,"user exists")
    u=User(email=r.email, username=r.username, display_name=r.username, password_hash=ph.hash(r.password)); db.add(u); db.commit(); return make_tokens(db,u)
@app.post("/api/v1/auth/login")
def login(r:Login, db:Session=Depends(get_db)):
    u=db.query(User).filter_by(email=r.email).first()
    if not u or not verify_password(r.password,u.password_hash): raise HTTPException(401,"bad credentials")
    return make_tokens(db,u)
@app.post("/api/v1/auth/refresh")
def refresh(body:dict, db:Session=Depends(get_db)):
    rt=db.query(RefreshToken).filter_by(token_hash=hash_token(body.get("refreshToken","")), revoked=False).first()
    if not rt: raise HTTPException(401,"bad refresh")
    rt.revoked=True; u=db.get(User,rt.user_id); return make_tokens(db,u)
@app.post("/api/v1/auth/logout")
def logout(u:User=Depends(current), db:Session=Depends(get_db)): db.query(RefreshToken).filter_by(user_id=u.id).update({"revoked":True}); db.commit(); return {"ok":True}
@app.get("/api/v1/users/me")
def me(u:User=Depends(current)): return {"id":u.id,"email":u.email,"username":u.username,"displayName":u.display_name,"xp":u.xp, **level_for_xp(u.xp)}
@app.post("/api/v1/onboarding")
def onboard(o:Onboarding,u:User=Depends(current),db:Session=Depends(get_db)): return {"quests":[q.__dict__ for q in generate_plan(db,u,o.goals,o.timeBudget,o.intensity)]}
@app.get("/api/v1/quests/today")
def today(u:User=Depends(current),db:Session=Depends(get_db)): return db.query(DailyQuest).filter_by(user_id=u.id).all()
@app.post("/api/v1/quests/complete")
def complete(c:Complete,u:User=Depends(current),db:Session=Depends(get_db)): comp=complete_quest(db,u,c.questId,c.idempotencyKey); return {"completionId":comp.id,"xpAwarded":comp.xp_awarded,"profile":level_for_xp(u.xp)}
@app.get("/api/v1/progress/summary")
def progress(u:User=Depends(current),db:Session=Depends(get_db)): return {"xp":u.xp, **level_for_xp(u.xp), "achievements":[a.achievement_code for a in []]}
@app.post("/api/v1/coach/message")
def coach(c:Coach,u:User=Depends(current),db:Session=Depends(get_db)): return {"reply":coach_reply(db,u,c.message)}
@app.get("/api/v1/friends/search")
def search(q:str,u:User=Depends(current),db:Session=Depends(get_db)): return db.query(User).filter(User.username.contains(q), User.id!=u.id).limit(10).all()
