from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess, uuid, os

app = FastAPI()

@app.post("/convert")
async def convert_video(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    inp = f"/tmp/{uid}_in.mp4"
    out = f"/tmp/{uid}_out.mp4"

    with open(inp, "wb") as f:
        f.write(await file.read())

    cmd = [
        "ffmpeg", "-y", "-i", inp,
        "-filter_complex",
        "[0:v]scale=1080:-1,boxblur=20:1,setsar=1[bg];"
        "[0:v]scale=-1:1920,setsar=1[fg];"
        "[bg]crop=1080:1920[bg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        out
    ]

    subprocess.run(cmd, check=True)

    return FileResponse(out, media_type="video/mp4", filename="short.mp4")


@app.get("/")
def root():
    return {"status": "ffmpeg api running"}
