from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import re
from typing import Optional

app = FastAPI()

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptionRequest(BaseModel):
    url: str
    language: Optional[str] = "es"

def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    Supports various formats like:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    # Regex for extracting video ID
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

@app.post("/transcribe")
async def transcribe_video(request: TranscriptionRequest):
    try:
        video_id = extract_video_id(request.url)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        # Fetch transcript
        # languages preference: requested language, then english as fallback if not strict
        # Note: Using v1.2.3+ object-oriented API
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id, languages=[request.language, 'en'])
        
        # Combine text
        # transcript_list is an iterable of FetchedTranscriptSnippet objects
        full_text = " ".join([item.text for item in transcript_list])
        
        # Convert segments to dicts for JSON response
        segments = [
            {
                "text": item.text,
                "start": item.start,
                "duration": item.duration
            }
            for item in transcript_list
        ]
        
        return {
            "video_id": video_id,
            "language": request.language,
            "transcript": full_text,
            "segments": segments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
