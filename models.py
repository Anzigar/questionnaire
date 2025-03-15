from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    jina_kamili = Column(String(255))
    jinsi = Column(String(50))
    umri = Column(String(50))
    barua_pepe = Column(String(255))
    nambari_simu = Column(String(255))
    
    ngazi_elimi = Column(String(255))
    jina_kozi = Column(String(255))
    mwaka_kuhitimu = Column(String(50))
    
    taasisi_mwisho = Column(String(255), nullable=True)
    
    ujuzi_kompyuta = Column(String(50))
    lugha = Column(Text)  # Store as comma-separated values
    msaada = Column(Text)  # Store as comma-separated values
    
    # File reference - this would store path to uploaded file
    pasipoti_path = Column(String(255), nullable=True)
