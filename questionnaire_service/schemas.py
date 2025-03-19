from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Define form data request model
class FormDataRequest(BaseModel):
    jinaKamili: str
    jinsi: str
    umri: str
    baruaPepe: str
    nambariSimu: str
    ngaziElimi: str
    jinaKozi: str
    mwakaKuhitimu: str
    taasisiMwisho: Optional[str] = None
    ujuziKompyuta: str
    lugha: List[str]
    msaada: List[str]

# Define form data response model
class FormDataResponse(BaseModel):
    id: int
    jina_kamili: str
    jinsi: str
    barua_pepe: str
    created_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

# Define pagination response model
class PaginationResponse(BaseModel):
    total: int
    page: int
    page_size: int
    pages: int

class SubmissionsResponse(BaseModel):
    items: List[FormDataResponse]
    pagination: PaginationResponse
