import traceback
from app.database import Base, engine, SessionLocal
from app import models, auth
from app.main import app
from fastapi.testclient import TestClient

Base.metadata.create_all(bind=engine)

session = SessionLocal()
try:
    session.query(models.Draft).delete()
    session.query(models.Application).delete()
    session.query(models.User).delete()
    session.commit()

    user = models.User(username='testuser', hashed_password=auth.get_password_hash('testpass'))
    session.add(user)
    session.commit()
    session.refresh(user)

    app_obj = models.Application(
        job_title='Test Job',
        company='Test Co',
        jd_text='Job description',
        original_resume_text='Resume text',
        resume_sections='Summary: Test',
        user_id=user.id
    )
    session.add(app_obj)
    session.commit()
    session.refresh(app_obj)

    draft = models.Draft(
        application_id=app_obj.id,
        resume_rewrite='Hello world\n\nThis is a test resume\nLine 3',
        ats_score='80'
    )
    session.add(draft)
    session.commit()

    token = auth.create_access_token({'sub': user.username})
    client = TestClient(app)
    response = client.get(f'/applications/{app_obj.id}/download/resume', headers={'Authorization': f'Bearer {token}'})
    print('status', response.status_code)
    print('headers', response.headers)
    print('content_len', len(response.content))
    print('content_partial', response.content[:20])
except Exception:
    traceback.print_exc()
finally:
    session.close()
