from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/templates', StaticFiles(directory='templates'), name='templates')

templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return {"message": "Hello Oui"}


@app.get('/index', response_class=HTMLResponse)
def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})\

@app.get('/About', response_class=HTMLResponse)
def test(request: Request):
    return templates.TemplateResponse("/about.html", {"request": request})

@app.get('/generative', response_class=HTMLResponse)
def test(request: Request):
    return templates.TemplateResponse("generative.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=8001,
                reload=True,
                log_level="debug")
