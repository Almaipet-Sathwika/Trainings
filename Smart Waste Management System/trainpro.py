import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.optimizers import Adam


image_size = (128, 128)
input_shape = (128, 128, 3)
num_classes = 6

# Build custom CNN model
cnn_model = Sequential([
    Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax')

])


cnn_model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

cnn_model.summary()


train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    rotation_range=15,
    zoom_range=0.2
)

val_datagen = ImageDataGenerator(rescale=1./255)

#datasets
train_generator = train_datagen.flow_from_directory(
    'newdataset/train',
    target_size=image_size,
    batch_size=32,
    class_mode='sparse'
)

val_generator = val_datagen.flow_from_directory(
    'newdataset/val',
    target_size=image_size,
    batch_size=32,
    class_mode='sparse'
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-5,
    verbose=1
)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=15,
    restore_best_weights=True,
    verbose=1
)

history = cnn_model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=5,
    validation_data=val_generator,
    validation_steps=len(val_generator),
    callbacks=[reduce_lr, early_stopping]#checkpoint
)



import os
cnn_model.save('transfer_model.h5')

model_path = "transfer_model.h5" 
 
model_size = os.path.getsize(model_path)
 
model_size_mb = model_size / (1024 * 1024)
print(f"Model Size: {model_size_mb:.2f} MB")




import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model_path = "transfer_model.h5"
cnn_model = load_model(model_path)

model_size = os.path.getsize(model_path)
model_size_mb = model_size / (1024 * 1024)
print(f"Model Size: {model_size_mb:.2f} MB")

img_path = "3.jpg"

img = image.load_img(img_path, target_size=(128, 128))
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

pred = cnn_model.predict(img_array)
predicted_class = np.argmax(pred, axis=1)[0]

class_labels = ['cardboard', 'glass', 'metal', 'paper','plastic','trash'] 
predicted_label = class_labels[predicted_class]

print(f"Predicted Class Index: {predicted_class}")
print(f"Predicted Class Label: {predicted_label}")
 