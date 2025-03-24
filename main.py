import io
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.templating import Jinja2Templates

from app.classificator import predict_class
from app.consts.animal_texts import CLASS_LABELS_LOCALIZED, CLASS_SHORT_INFO
from app.consts.api_params import API_DESCRIPTION, API_TITLE

# Инициализация FastAPI, Jinja2Templates. Монтирование папки static с изображениями
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version="0.0.1",
)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name="static")

# GET. Получение описания
@app.get("/api/about", 
         response_class = PlainTextResponse,
         summary='Описание')
def get_text():
    return "Представляем сервис для классификации изображений"

# GET. Получение списка классов
@app.get("/api/animals", 
         response_class = JSONResponse,
         summary='Получение списка классов')
def get_animals():
    animals_list = []
    id = 0
    for el in CLASS_LABELS_LOCALIZED:
        animals_list.append({"id": id,"classname": el})
        id+=1
    return animals_list

# GET. Получение html страницы с инфой о классе
@app.get("/api/animal_info/{index}",
    summary="Короткая информация о виде",
    description="Получение короткой информаци")
def get_animal_page(request: Request, index: int):
    if 0 <= index < len(CLASS_LABELS_LOCALIZED):
        title = CLASS_LABELS_LOCALIZED[index]
        description = CLASS_SHORT_INFO[index]
        img_path = f"/static/{index}.jpg"  # Пусть картинка хранится в /static/images/
    else:
        raise HTTPException(status_code=404, detail="Неверный индекс")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": title,
        "description": description,
        "img_path": img_path
    })

# POST. Распознование класса по входному изображению
@app.post("/api/recognize",
    response_class= JSONResponse,
    summary="Распознование изображения",
    description="Определение принадлежности к классу")

async def get_animal_class(img: UploadFile = File(...)):
    img_bytes = await img.read()  # Читаем байты файла
    img_stream = io.BytesIO(img_bytes)  # Создаём поток для загрузки изображения
    predicted_class =  predict_class(img_stream)
    
    return { "id": predicted_class,"classname": CLASS_LABELS_LOCALIZED[predicted_class] }