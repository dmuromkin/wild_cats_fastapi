import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array

IMAGE_SIZE = 224
model = keras.models.load_model('app/models/wild_cats_model(96.0%).h5')

def predict_class(img_stream):
    img = load_img(img_stream, target_size=(IMAGE_SIZE, IMAGE_SIZE))  # Изменяем размер изображения
    img_array = img_to_array(img)  # Преобразуем в массив
    img_array = img_array / 255.0  # Нормализация
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    
    return int(predicted_class)