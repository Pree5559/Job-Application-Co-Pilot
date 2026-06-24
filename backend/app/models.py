# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    applications = relationship("Application", back_populates="owner")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    jd_text = Column(Text, nullable=False)
    jd_url = Column(String, nullable=True)
    original_resume_text = Column(Text, nullable=False)
    resume_sections = Column(Text, nullable=True)
    status = Column(String, default="not yet")  # applied / not yet / rejected / interviewed
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="applications")
    drafts = relationship("Draft", back_populates="application", uselist=False)

class Draft(Base):
    __tablename__ = "drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), unique=True)
    fit_analysis = Column(Text, nullable=True)
    resume_rewrite = Column(Text, nullable=True)
    cover_letter = Column(Text, nullable=True)
    interview_qa = Column(Text, nullable=True)
    ats_score = Column(Text, nullable=True)
    
    application = relationship("Application", back_populates="drafts")