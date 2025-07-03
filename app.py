import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse


load_dotenv()

app = FastAPI()

SIGHTENGINE_API_URL = "https://api.sightengine.com/1.0/check.json"
MODELS = "nudity-2.0"


@app.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    """Проверка изображения на наличие NSFW контента."""
    if not file.filename.lower().endswith((".jpg", ".png")):
        raise HTTPException(
            status_code=400,
            detail='Неверный формат файла'
        )

    api_secret = os.getenv("SIGHTENGINE_API_SECRET")
    api_user = os.getenv("SIGHTENGINE_API_USER")

    if not api_secret or not api_user:
        raise HTTPException(
            status_code=500,
            detail='Не настроены API ключи'
        )

    try:
        file_content = await file.read()

        params = {
            'models': MODELS,
            'api_user': api_user,
            'api_secret': api_secret,
        }
        files = {'media': (file.filename, file_content, file.content_type)}

        response = requests.post(
            SIGHTENGINE_API_URL,
            files=files,
            data=params
        )
        response.raise_for_status()

        result = response.json()
        if result['status'] == 'failure':
            raise HTTPException(
                status_code=400,
                detail='Не удалось обработать изображение'
            )

        if 'nudity' in result:
            nsfw_score = max(
                result['nudity']['sexual_activity'],
                result['nudity']['sexual_display'],
                result['nudity']['erotica'],
                result['nudity']['suggestive']
            )

            if nsfw_score > 0.7:
                return {
                    "status": "REJECTED",
                    "reason": "NSFW content",
                    "score": nsfw_score
                }

        return {"status": "OK"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки изображения: {str(e)}"
        )
    finally:
        await file.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
