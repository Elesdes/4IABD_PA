# This script sets up a FastAPI application and defines several HTTP routes.
# It uses the Jinja2 templating engine to render HTML templates for different pages
# and serves static files from "static" and "templates" directories.
# The '/index' route accepts a 'year' parameter which is used to display the prediction result on the index page.
# The application is set to run on the local machine (127.0.0.1) at port 8001.
# Hot reloading is enabled which is useful during development as the server will automatically update upon code changes.
# The log level is set to "debug" for detailed logging.


# Importing the necessary libraries
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from python import index  # Importing routes defined in index.py

# Instantiating the FastAPI application
app = FastAPI()

# Including the routes defined in the router object in the index module
app.include_router(index.router)

# Mounting the directories for static files
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/templates', StaticFiles(directory='templates'), name='templates')

# Setting up Jinja2 template engine to use "templates" directory
templates = Jinja2Templates(directory="templates")


# Defining routes

# Main index route
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Return the index.html file as response
    return templates.TemplateResponse("index.html", {"request": request})

# Unauthorized access route
@app.get('/unauthorized', response_class=HTMLResponse)
def test(request: Request):
    # Return the index.html file with an additional message about the error
    return templates.TemplateResponse("index.html", {"request": request, "class_year": "Veuillez soumettre un fichier mp3."})

# About page route
@app.get('/about', response_class=HTMLResponse)
def test(request: Request):
    # Return the about.html file as response
    return templates.TemplateResponse("/about.html", {"request": request})

# Generative page route
@app.get('/generative', response_class=HTMLResponse)
def test(request: Request):
    # Return the generative.html file as response
    return templates.TemplateResponse("generative.html", {"request": request})

# Route for showing prediction result
@app.get("/index", response_class=HTMLResponse)
async def read_item(request: Request, year):
    # Return the index.html file with an additional parameter containing the year prediction
    return templates.TemplateResponse("index.html", {"request": request, "class_year": year})


# Running the application with uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app",  # application instance to run
                host="127.0.0.1",  # Host address
                port=8001,  # Port to listen to
                reload=True,  # Enable hot-reloading
                log_level="debug")  # Logging level
