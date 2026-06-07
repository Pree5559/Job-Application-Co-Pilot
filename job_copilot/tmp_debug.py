import traceback
from app.database import Base, engine, SessionLocal
from app import models
from app.main import download_resume

Base.metadata.create_all(bind=engine)

session = SessionLocal()
try:
    session.query(models.Draft).delete()
    session.query(models.Application).delete()
    session.query(models.User).delete()
    session.commit()

    user = models.User(username='testuser', hashed_password='x')
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

    from sqlalchemy.orm import joinedload
    app_obj = session.query(models.Application).options(joinedload(models.Application.drafts)).filter(models.Application.id==app_obj.id).first()

    try:
        resp = download_resume(app_id=app_obj.id, current_user=user, db=session)
        print('returned', type(resp))
    except Exception:
        traceback.print_exc()
finally:
    session.close()
