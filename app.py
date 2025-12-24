from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess, uuid, os

app = FastAPI()

@app.post("/convert")
async def convert_video(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    inp = f"/tmp/{uid}_in.mp4"
    out = f"/tmp/{uid}_out.mp4"

    # save uploaded file
    with open(inp, "wb") as f:
        f.write(await file.read())

    # run ffmpeg
    subprocess.run([
        "ffmpeg", "-y",
        "-i", inp,
        "-vf", "scale=1080:1920",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        out
    ], check=True)

    return FileResponse(
        out,
        media_type="video/mp4",
        filename="output.mp4"
    )
