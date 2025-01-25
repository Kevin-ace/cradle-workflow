from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from services.keyword_extraction import extract_keywords
from services.summarization import summarize_text
from services.translation import translate_text

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/process")
async def process_text(request: Request):
    data = await request.json()
    text = data["text"]
    
    # Extract keywords
    keywords = extract_keywords(text)
    
    # Summarize text
    summary = summarize_text(text)
    
    # Translate summary
    translation = translate_text(summary, tgt_lang=data.get("language", "es"))
    
    return {
        "keywords": keywords,
        "summary": summary,
        "translation": translation
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)