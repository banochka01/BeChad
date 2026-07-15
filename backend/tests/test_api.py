from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def auth():
    r=c.post('/api/v1/auth/register',json={'email':'a@example.com','username':'alice','password':'password123'})
    if r.status_code==409: r=c.post('/api/v1/auth/login',json={'email':'a@example.com','password':'password123'})
    return {'Authorization':'Bearer '+r.json()['accessToken']}
def test_health_auth_plan_complete_idempotent_coach():
    assert c.get('/health').json()['status']=='ok'
    h=auth(); me=c.get('/api/v1/users/me',headers=h); assert me.status_code==200
    plan=c.post('/api/v1/onboarding',headers=h,json={'goals':['fitness','reading'],'timeBudget':'15-30','intensity':'normal'}); assert plan.status_code==200
    qid=c.get('/api/v1/quests/today',headers=h).json()[0]['id']
    a=c.post('/api/v1/quests/complete',headers=h,json={'questId':qid,'idempotencyKey':'k1'}).json()
    b=c.post('/api/v1/quests/complete',headers=h,json={'questId':qid,'idempotencyKey':'k1'}).json()
    assert a['xpAwarded']==b['xpAwarded']
    assert 'reply' in c.post('/api/v1/coach/message',headers=h,json={'message':'help'}).json()
