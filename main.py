from time import strftime
from fastapi import FastAPI, HTTPException, Depends, Body, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, get_db, Base
from models import FormSubmission
from export_service import ExportService

# Application version and configuration
VERSION = "2.0.0"
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
API_TITLE = "Form Submission API"
API_DESCRIPTION = "API for processing and managing form submissions"

# Create database tables
Base.metadata.create_all(bind=engine)

#
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Enable CORS to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Define form data model
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

@app.post("/submit-form", response_model=FormDataResponse)
async def submit_form(form_data: FormDataRequest, db: Session = Depends(get_db)):
    try:
        # Create new database record
        db_submission = FormSubmission(
            jina_kamili=form_data.jinaKamili,
            jinsi=form_data.jinsi,
            umri=form_data.umri,
            barua_pepe=form_data.baruaPepe,
            nambari_simu=form_data.nambariSimu,
            ngazi_elimi=form_data.ngaziElimi,
            jina_kozi=form_data.jinaKozi,
            mwaka_kuhitimu=form_data.mwakaKuhitimu,
            taasisi_mwisho=form_data.taasisiMwisho,
            ujuzi_kompyuta=form_data.ujuziKompyuta,
            lugha=", ".join(form_data.lugha),
            msaada=", ".join(form_data.msaada)
        )
        
        # Add to database
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        
        return db_submission
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @app.post("/upload-file")
# async def upload_file(file: UploadFile = File(...), email: str = None, db: Session = Depends(get_db)):
#     try:
#         if not file:
#             raise HTTPException(status_code=400, detail="No file provided")
            
#         # Generate unique filename
#         file_extension = os.path.splitext(file.filename)[1]
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
#         # Handle case when email is not provided or empty
#         if email and email.strip():
#             email_prefix = email.replace('@', '_at_')
#         else:
#             email_prefix = "unknown"
            
#         # Generate random string - fix the hex conversion
#         import secrets
#         random_hex = secrets.token_hex(4)
        
#         unique_filename = f"{email_prefix}_{timestamp}_{random_hex}{file_extension}"
#         file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
#         # Save the file with better error handling
#         try:
#             with open(file_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)
#         except Exception as file_error:
#             raise HTTPException(status_code=500, detail=f"Error saving file: {str(file_error)}")
        
#         # Update database record if email is provided
#         if email and email.strip():
#             try:
#                 submission = db.query(FormSubmission).filter(FormSubmission.barua_pepe == email).order_by(FormSubmission.created_at.desc()).first()
#                 if submission:
#                     submission.pasipoti_path = file_path
#                     db.commit()
#             except Exception as db_error:
#                 # Continue even if DB update fails - at least the file is saved
#                 print(f"DB update error: {str(db_error)}")
        
#         return {"filename": unique_filename, "path": file_path}
#     except Exception as e:
#         # Log the full error for debugging
#         import traceback
#         print(f"Error in upload_file: {str(e)}")
#         print(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/export-excel")
async def export_excel(db: Session = Depends(get_db)):
    try:
        # Use the export service to generate Excel file
        excel_data = ExportService.export_to_excel(db)
        filename = ExportService.generate_filename()
        
        # Ensure filename has .xlsx extension
        if not filename.lower().endswith('.xlsx'):
            if '.' in filename:
                filename = filename.rsplit('.', 1)[0] + '.xlsx'
            else:
                filename += '.xlsx'
        
        # Save the Excel file to the uploads folder
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Write the Excel data to the file
        with open(file_path, "wb") as f:
            f.write(excel_data.getvalue())
            
        # Read the saved file and stream it to the client
        def iterfile():
            with open(file_path, "rb") as f:
                yield from f
        
        # Return Excel file as a downloadable response
        return StreamingResponse(
            iterfile(), 
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting data: {str(e)}")

@app.get("/submissions", response_model=SubmissionsResponse)
async def get_submissions(
    db: Session = Depends(get_db),
    search: Optional[str] = None,
    jinsi: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    page_size: int = 10
):
    """Get form submissions with filtering options and pagination"""
    query = db.query(FormSubmission)
    
    # Apply filters if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            FormSubmission.jina_kamili.ilike(search_term) | 
            FormSubmission.barua_pepe.ilike(search_term)
        )
    
    if jinsi:
        query = query.filter(FormSubmission.jinsi == jinsi)
        
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(FormSubmission.created_at >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            # Set end date to end of day
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(FormSubmission.created_at <= end)
        except ValueError:
            pass
    
    # Count total records for pagination info
    total_records = query.count()
    
    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    # Order by created_at descending
    submissions = query.order_by(FormSubmission.created_at.desc()).all()
    
    # Return paginated results with pagination metadata
    return {
        "items": submissions,
        "pagination": {
            "total": total_records,
            "page": page,
            "page_size": page_size,
            "pages": (total_records + page_size - 1) // page_size
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "API is running", 
        "version": VERSION,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    import logging
    
    # Configure logging format for better output
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "fmt": "%(asctime)s [%(levelname)s] %(message)s",
                "datefmt": " %Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO"},
        },
    }
    
    # Print application banner with URLs
    print(f"\n{'='*60}")
    print(f" {API_TITLE} v{VERSION}")
    print(f"{'='*60}")
    print(f" Base URL: {BASE_URL}")
    print(f" API Documentation: {BASE_URL}/docs")
    print(f" ReDoc Interface: {BASE_URL}/redoc")
    print(f" Health Check: {BASE_URL}/health")
    print(f"{'='*60}\n")
    
    # Run the Uvicorn server with custom settings
    uvicorn.run(
        app="main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info",
        log_config=log_config,
        workers=1
    )