import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import numpy as np
from numpy.linalg import norm
import os
from tqdm import tqdm
import pickle

model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False
model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])
print(model.summary())


def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalised_result = result / norm(result)
    return normalised_result


file_names = []
for file in os.listdir('images'):
    file_names.append(os.path.join('images', file))
feature_list = []
for file in tqdm(file_names):
    feature_list.append(extract_features(file, model))
print(np.array(feature_list).shape)
pickle.dump(feature_list,open('embeddings.pkl', 'wb'))
pickle.dump(file_names,open('file_names.pkl', 'wb'))
