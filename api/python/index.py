from fastapi import APIRouter
from fastapi import UploadFile, File, status, HTTPException
from fastapi.responses import RedirectResponse
import shutil

router = APIRouter()


@router.post("/uploader")
async def create_upload_file(file: UploadFile = File(...)):
    if file.filename == '':
        return RedirectResponse(url="/unauthorized", status_code=status.HTTP_302_FOUND)
    with open(f"music/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # print(file.content_type)
    if file.content_type not in ["video/mp4", "audio/mpeg", "application/octet-stream", "video/3gpp", "audio/x-m4a"]:
        return RedirectResponse(url="/unauthorized", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)


def test_response():
    # todo vérifier que l'on a bien reçu un fichier, autrement retourner prédiction = "" ou none
    # todo transformer
    # predictions = best_model.predict(val_dataset).argmax(axis=1)
    predictions = 'année 80'

    return predictions
    # return best_model.predict(val_dataset).argmax(axis=1)
