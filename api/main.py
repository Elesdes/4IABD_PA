import shutil

from fastapi import FastAPI, Request, UploadFile, File, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/templates', StaticFiles(directory='templates'), name='templates')

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/test', response_class=HTMLResponse)
def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})\

@app.get('/About', response_class=HTMLResponse)
def test(request: Request):
    return templates.TemplateResponse("/about.html", {"request": request})

@app.get('/generative', response_class=HTMLResponse)
def test(request: Request):
    return templates.TemplateResponse("generative.html", {"request": request})

@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
   return templates.TemplateResponse("index.html", {"request": request})

@app.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...)):
   with open(f"musique/{file.filename}", "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
   return RedirectResponse(url="/upload/",status_code=status.HTTP_302_FOUND)


@app.get("/index/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

if __name__ == "__main__":
    templates = Jinja2Templates(directory="templates")
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=8001,
                reload=True,
                log_level="debug")
