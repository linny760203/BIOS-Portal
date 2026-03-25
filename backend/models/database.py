from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    display_name = Column(String)
    department = Column(String)
    email = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=datetime.utcnow)

class BiosRelease(Base):
    __tablename__ = "bios_releases"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    version = Column(String)
    file_path = Column(String)
    checksum = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, ForeignKey("users.id"))

class BiosConfig(Base):
    __tablename__ = "bios_configs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, index=True)
    config_type = Column(String)
    data = Column(JSON)
    version = Column(Integer, default=1)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
