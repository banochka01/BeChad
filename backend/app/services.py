import hashlib, secrets
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from sqlalchemy.orm import Session
from .database import settings
from .models import Achievement, DailyQuest, QuestCompletion, Streak, User, UserAchievement, XpEvent, RefreshToken, FriendRequest, Friendship, CoachMessage
ph=PasswordHasher()
ACH=[("first_quest","First Quest","Complete one quest"),("perfect_day","Perfect Day","Complete all main quests"),("streak_3","3 Day Flame","Keep a 3 day streak"),("streak_7","7 Day Flame","Keep a 7 day streak"),("streak_30","30 Day Flame","Keep a 30 day streak"),("pushups_100","100 Pushups","Log 100 pushups"),("squats_500","500 Squats","Log 500 squats"),("pages_100","100 Pages","Read 100 pages"),("language_60","60 Language Minutes","Practice 60 minutes"),("weeks_10","10 Weeks","Complete 10 weeks"),("quests_100","100 Quests","Complete 100 quests"),("first_friend","First Friend","Add a friend")]
def level_for_xp(xp:int)->dict:
    level=1; need=100
    while xp>=need: xp-=need; level+=1; need=int(need*1.25)+50
    return {"level":level,"xpIntoLevel":xp,"xpToNext":need}
def hash_token(t): return hashlib.sha256(t.encode()).hexdigest()
def make_tokens(db:Session,u:User):
    access=jwt.encode({"sub":u.id,"iss":settings.jwt_issuer,"exp":datetime.now(timezone.utc)+timedelta(minutes=15)},settings.jwt_secret,algorithm="HS256")
    refresh=secrets.token_urlsafe(48); db.add(RefreshToken(user_id=u.id, token_hash=hash_token(refresh))); db.commit()
    return {"accessToken":access,"refreshToken":refresh,"tokenType":"bearer"}
def verify_password(p,h):
    try: return ph.verify(h,p)
    except Exception: return False
def seed_achievements(db):
    for c,t,d in ACH:
        if not db.get(Achievement,c): db.add(Achievement(code=c,title=t,description=d))
    db.commit()
def generate_plan(db,u:User, goals:list[str], time_budget:str, intensity:str):
    diff={"light":("easy",10),"normal":("normal",20),"intense":("hard",35)}.get(intensity,("normal",20))
    templates={"fitness":["10 pushups","20 squats","Plank 30 seconds"],"languages":["Practice language 10 minutes","Complete one language lesson"],"reading":["Read 5 pages"],"productivity":["15 minutes focused work"],"sleep":["Prepare for bed on time"],"custom":["Complete custom habit"]}
    today=datetime.now(timezone.utc).date()
    quests=[]
    for d in range(7):
        for i,g in enumerate(goals or ["fitness"]):
            title=templates.get(g,templates["custom"])[(d+i)%len(templates.get(g,templates["custom"]))]
            q=DailyQuest(user_id=u.id, day=str(today+timedelta(days=d)), title=title, category=g, difficulty=diff[0], base_xp=diff[1]+min(d*2,10), is_main=i<3)
            db.add(q); quests.append(q)
    db.commit(); return quests
def complete_quest(db,u:User,quest_id:str,idem:str):
    existing=db.query(QuestCompletion).filter_by(user_id=u.id,idempotency_key=idem).first()
    if existing: return existing
    q=db.get(DailyQuest,quest_id); assert q and q.user_id==u.id
    xp=min(q.base_xp,60); comp=QuestCompletion(user_id=u.id,quest_id=q.id,idempotency_key=idem,xp_awarded=xp)
    db.add(comp); db.add(XpEvent(user_id=u.id,amount=xp,reason="quest_completion",ref_id=q.id)); u.xp+=xp
    st=db.get(Streak,u.id) or Streak(user_id=u.id); day=q.day
    if st.last_day!=day: st.current = st.current+1 if st.last_day else 1; st.best=max(st.best,st.current); st.last_day=day
    db.merge(st); db.commit(); award(db,u); return comp
def award(db,u):
    count=db.query(QuestCompletion).filter_by(user_id=u.id).count(); codes=[]
    if count>=1: codes.append("first_quest")
    if count>=100: codes.append("quests_100")
    st=db.get(Streak,u.id)
    if st and st.current>=3: codes.append("streak_3")
    if st and st.current>=7: codes.append("streak_7")
    for c in codes:
        if not db.get(UserAchievement,{"user_id":u.id,"achievement_code":c}): db.add(UserAchievement(user_id=u.id,achievement_code=c))
    db.commit()
def coach_reply(db,u,msg):
    text="Nice momentum. Complete one small main quest today to protect your streak."
    db.add(CoachMessage(user_id=u.id,role="user",content=msg)); db.add(CoachMessage(user_id=u.id,role="assistant",content=text)); db.commit(); return text
