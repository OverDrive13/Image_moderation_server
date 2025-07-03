
Сервер для проверки изображений на NSFW контент с использованием Sightengine API.

## Установка и запуск

1. Создайте виртуальное окружение:
```bash
python -m venv venv
на Windows: source venv/Scripts/activate
на Linux/macOS: source venv/bin/activate.

2. Установите зависимости:
```bash
pip install -r requirements.txt

3. Создайте файл .env и добавьте API ключи:
env
ключи можно получить зарегистрировавшись на https://dashboard.sightengine.com/api-credentials
SIGHTENGINE_API_USER=
SIGHTENGINE_API_SECRET=

3. Запустите сервер:
```bash
uvicorn app:app --reload
```

Пример запроса
Отправка изображения на модерацию:

bash
curl -X POST -F "file=@\"путь к файлу/images.jpg\"" http://localhost:8000/moderate

Возможные ответы:

{"status": "OK"} - изображение безопасно

{"status": "REJECTED", "reason": "NSFW content"} - обнаружен NSFW контент