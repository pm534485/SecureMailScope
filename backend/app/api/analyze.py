from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import shutil
import os
import uuid
import json
from pathlib import Path

# Add backend directory to sys path if running from different cwd
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from pcap_engine.packet_parser import PcapParser

router = APIRouter()

UPLOAD_DIR = Path("data/pcaps")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class AnalysisResponse(BaseModel):
    analysis_id: str
    filename: str
    status: str
    message: str

@router.post("/analyze", response_model=AnalysisResponse)
async def upload_pcap(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith(('.pcap', '.pcapng')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .pcap or .pcapng are allowed.")
    
    analysis_id = str(uuid.uuid4())
    filepath = UPLOAD_DIR / f"{analysis_id}_{file.filename}"
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Start analysis in background
    background_tasks.add_task(process_pcap, str(filepath), analysis_id)
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        filename=file.filename,
        status="processing",
        message="PCAP uploaded successfully. Analysis started."
    )

def process_pcap(filepath: str, analysis_id: str):
    try:
        parser = PcapParser(filepath)
        results = parser.analyze()
        
        # Save results to processed directory
        PROCESSED_DIR = Path("data/processed")
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        
        output_file = PROCESSED_DIR / f"{analysis_id}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
            
        print(f"Analysis {analysis_id} completed successfully.")
        
    except Exception as e:
        print(f"Analysis {analysis_id} failed: {str(e)}")

@router.get("/analysis/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    output_file = Path(f"data/processed/{analysis_id}.json")
    if not output_file.exists():
        return {"status": "processing_or_not_found"}
        
    with open(output_file, "r") as f:
        results = json.load(f)
        
    return {"status": "completed", "results": results}
