from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import os
from datetime import datetime
from sqlalchemy.orm import Session

from database import get_db
from questionnaire_service.models import FormSubmission
from questionnaire_service.schemas import FormDataRequest, FormDataResponse, SubmissionsResponse
from export_service import ExportService

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

VERSION = "1.0.0"

@router.post("/submit-form", response_model=FormDataResponse)
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

@router.get("/export-excel")
async def export_excel(db: Session = Depends(get_db)):
    try:
        excel_data = ExportService.export_to_excel(db)
        filename = ExportService.generate_filename()
        
        if not filename.lower().endswith('.xlsx'):
            if '.' in filename:
                filename = filename.rsplit('.', 1)[0] + '.xlsx'
            else:
                filename += '.xlsx'
 
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Write the Excel data to the file
        with open(file_path, "wb") as f:
            f.write(excel_data.getvalue())
    
        def iterfile():
            with open(file_path, "rb") as f:
                yield from f
    
        return StreamingResponse(
            iterfile(), 
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting data: {str(e)}")

@router.get("/submissions", response_model=SubmissionsResponse)
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
    
    # Order by created_at descending first, then apply pagination
    query = query.order_by(FormSubmission.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    submissions = query.all()
    
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

@router.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "API is running", 
        "version": VERSION,
        "timestamp": datetime.now().isoformat()
    }
