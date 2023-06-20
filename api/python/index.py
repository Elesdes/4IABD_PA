from fastapi import APIRouter
from fastapi import UploadFile, File, status
from fastapi.responses import RedirectResponse
import shutil

router = APIRouter()


@router.post("/uploader")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f"musique/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # print(file.content_type)
    if file.content_type not in ["video/mp4", "audio/mpeg", "application/octet-stream", "video/3gpp", "audio/x-m4a"]:
        return RedirectResponse(url="/test", status_code=status.HTTP_403_FORBIDDEN)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


def test_response():
    # todo vérifier que l'on a bien reçu un fichier, autrement retourner prédiction = "" ou none
    # todo transformer
    # predictions = best_model.predict(val_dataset).argmax(axis=1)
    predictions = 'année 80'

    return predictions
    # return best_model.predict(val_dataset).argmax(axis=1)
