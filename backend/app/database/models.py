from sqlalchemy import Column, Integer, String, DateTime, Date
from datetime import datetime
from app.database.db import Base

class HMRCAuthToken(Base):
    __tablename__ = "hmrc_tokens"
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    expires_in = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class VATObligation(Base):
    __tablename__ = "vat_obligations"
    id = Column(Integer, primary_key=True, index=True)
    vrn = Column(String, nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    due = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
