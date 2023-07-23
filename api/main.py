import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from python import index

app = FastAPI()

app.include_router(index.router)

app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/templates', StaticFiles(directory='templates'), name='templates')

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/unauthorized', response_class=HTMLResponse)
def test(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request, "class_year": "Veuillez soumettre un fichier mp3."})


@app.get('/generative', response_class=HTMLResponse)
def generative(request: Request):
    return templates.TemplateResponse("generative.html", {"request": request})


@app.get('/about', response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("/about.html", {"request": request})


@app.get("/index", response_class=HTMLResponse)
async def read_item(request: Request, year):
    return templates.TemplateResponse("index.html", {"request": request, "class_year": year})


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=8001,
                reload=True,
                log_level="debug")
