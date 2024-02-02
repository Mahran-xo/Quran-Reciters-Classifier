from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/upload_mp3")
async def upload_mp3(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/mpeg"):
        return {"error": "Invalid file format. Please upload an MP3 file."}

    # Process the MP3 file (optional)

    return {"message": "OK"}
