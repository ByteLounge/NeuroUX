from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
import schemas
import os
import sys
import uuid
from datetime import datetime
from fastapi.responses import FileResponse

# Allow importing from the root for ml_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_engine.engine import NeuroUXEngine
from report_generator import ReportGenerator

app = FastAPI(title="NeuroUX API", description="Stateless Cognitive Load & Attention Engine")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
STORAGE_DIR = "../database/sessions"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Mount static files for serving images/heatmaps
app.mount("/static/sessions", StaticFiles(directory=STORAGE_DIR), name="sessions")

# In-memory storage for the *current* session only (or simple file-based tracking)
# Since we want no history, we'll keep it simple: files are stored in session folders
# and we provide a cleanup mechanism if needed, but for now we'll just store and serve.

engine_instance = NeuroUXEngine()
# Reports will be stored in the session folder itself
reporter = ReportGenerator("") # Will set path per request

@app.get("/")
def read_root():
    return {"message": "Welcome to NeuroUX Stateless API"}

@app.post("/api/v1/analyze", response_model=schemas.AnalysisResult)
async def analyze_ui(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(STORAGE_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)

    # 1. Save Original Image
    filename = file.filename
    file_path = os.path.join(session_dir, filename)
    with open(file_path, "wb+") as file_object:
        file_object.write(await file.read())

    # 2. Trigger ML Engine
    try:
        results = engine_instance.process_image(file_path, session_dir)
        
        # 3. Prepare response
        metrics = results["metrics"]
        saliency_filename = os.path.basename(results['saliency_heatmap_path'])
        
        analysis_result = schemas.AnalysisResult(
            id=session_id,
            created_at=datetime.now(),
            original_image_path=f"/static/sessions/{session_id}/{filename}",
            saliency_heatmap_path=f"/static/sessions/{session_id}/{saliency_filename}",
            cfi_score=metrics["cfi_score"],
            vcs_score=metrics["vcs_score"],
            ifs_score=metrics["ifs_score"],
            ddp_score=metrics["ddp_score"],
            ux_intelligence_score=metrics["ux_intelligence_score"],
            recommendations=[schemas.Recommendation(**rec) for rec in results["recommendations"]]
        )
        
        # 4. Pre-generate report for immediate download
        reporter.output_dir = session_dir
        reporter.generate_pdf(analysis_result.model_dump())
        
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/v1/export/{session_id}")
def export_report(session_id: int | str):
    report_path = os.path.join(STORAGE_DIR, str(session_id), f"report_{session_id}.pdf")
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found or session expired")
    
    return FileResponse(report_path, filename=f"NeuroUX_Report_{session_id}.pdf")
