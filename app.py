from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import subprocess, uuid, os

app = FastAPI()

@app.post("/convert")
async def convert(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    inp = f"/tmp/{uid}_in.mp4"
    out = f"/tmp/{uid}_out.mp4"

    # Save input
    with open(inp, "wb") as f:
        f.write(await file.read())

    # Run ffmpeg
    subprocess.run([
        "ffmpeg", "-y", "-i", inp,
        "-filter_complex",
        "[0:v]scale=1080:-1,boxblur=20:1,setsar=1[bg];"
        "[0:v]scale=-1:1920,setsar=1[fg];"
        "[bg]crop=1080:1920[bg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-movflags", "+faststart",
        out
    ], check=True)

    # 🔑 stream file manually
    def iterfile():
        with open(out, "rb") as f:
            yield from f

    return StreamingResponse(
        iterfile(),
        media_type="video/mp4",
        headers={
            "Content-Disposition": "attachment; filename=short.mp4"
        }
    )
