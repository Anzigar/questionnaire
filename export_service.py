import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from models import FormSubmission
from datetime import datetime

class ExportService:
    @staticmethod
    def export_to_excel(db: Session):
        """
        Export all form submissions to Excel
        
        Args:
            db: Database session
            
        Returns:
            BytesIO object containing Excel file
        """
        # Get all submissions from database
        submissions = db.query(FormSubmission).all()
        
        # Convert to list of dictionaries for pandas
        data = []
        for submission in submissions:
            data.append({
                "Jina Kamili": submission.jina_kamili,
                "Jinsi": submission.jinsi,
                "Umri": submission.umri,
                "Barua Pepe": submission.barua_pepe,
                "Nambari Simu": submission.nambari_simu,
                "Ngazi ya Elimu": submission.ngazi_elimi,
                "Jina la Kozi": submission.jina_kozi,
                "Mwaka wa Kuhitimu": submission.mwaka_kuhitimu,
                "Taasisi ya Mwisho": submission.taasisi_mwisho or "",
                "Ujuzi wa Kompyuta": submission.ujuzi_kompyuta,
                "Lugha": submission.lugha,
                "Msaada": submission.msaada,
                "Tarehe ya Usajili": submission.created_at,
            })
        
        # Create pandas DataFrame and export to Excel
        df = pd.DataFrame(data)
        
        # Create BytesIO buffer to hold Excel file
        output = BytesIO()
        
        # Use ExcelWriter for more control
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Form Submissions', index=False)
            
            # Adjust column widths
            worksheet = writer.sheets['Form Submissions']
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + i)].width = min(max_length, 50)  # A, B, C, etc.
        
        # Reset buffer position to beginning
        output.seek(0)
        
        return output
    
    @staticmethod
    def generate_filename():
        """Generate a filename for the Excel export"""
        now = datetime.now()
        return f"form_submissions_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
