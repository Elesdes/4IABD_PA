from fastapi import APIRouter
from fastapi import UploadFile, File, status
from fastapi.responses import RedirectResponse
import shutil

router = APIRouter()


@router.post("/uploader")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f"musique/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)


def test_response():
    # todo transformer
    # predictions = best_model.predict(val_dataset).argmax(axis=1)
    predictions = 'année 80'
    return predictions
    # return best_model.predict(val_dataset).argmax(axis=1)
