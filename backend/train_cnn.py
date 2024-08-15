import json
import os
import shutil
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model
from efficientnet.tfkeras import EfficientNetB0


dataset_path = '.\\split_dataset\\'
tmp_debug_path = '.\\tmp_debug'
checkpoint_filepath = '.\\tmp_checkpoint'

print(f'Creating Directory: {tmp_debug_path}')
os.makedirs(tmp_debug_path, exist_ok=True)

print(f'Creating Directory: {checkpoint_filepath}')
os.makedirs(checkpoint_filepath, exist_ok=True)

def get_filename_only(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]

input_size = 128
batch_size_num = 32
train_path = os.path.join(dataset_path, 'train')
val_path = os.path.join(dataset_path, 'val')
test_path = os.path.join(dataset_path, 'test')

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1/255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_generator = train_datagen.flow_from_directory(
    directory=train_path,
    target_size=(input_size, input_size),
    color_mode="rgb",
    class_mode="binary",
    batch_size=batch_size_num,
    shuffle=True
)

val_datagen = ImageDataGenerator(rescale=1/255)

val_generator = val_datagen.flow_from_directory(
    directory=val_path,
    target_size=(input_size, input_size),
    color_mode="rgb",
    class_mode="binary",
    batch_size=batch_size_num,
    shuffle=True
)

test_datagen = ImageDataGenerator(rescale=1/255)

test_generator = test_datagen.flow_from_directory(
    directory=test_path,
    classes=['real', 'fake'],
    target_size=(input_size, input_size),
    color_mode="rgb",
    class_mode=None,
    batch_size=1,
    shuffle=False
)

# Build model
efficient_net = EfficientNetB0(
    weights='imagenet',
    input_shape=(input_size, input_size, 3),
    include_top=False,
    pooling='max'
)

model = Sequential([
    efficient_net,
    Dense(units=512, activation='relu'),
    Dropout(0.5),
    Dense(units=128, activation='relu'),
    Dense(units=1, activation='sigmoid')
])

model.summary()

# Compile model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

custom_callbacks = [
    EarlyStopping(
        monitor='val_loss',
        mode='min',
        patience=5,
        verbose=1
    ),
    ModelCheckpoint(
        filepath=os.path.join(checkpoint_filepath, 'best_model.keras'),
        monitor='val_loss',
        mode='min',
        verbose=1,
        save_best_only=True
    )
]

# Train network
num_epochs = 20
history = model.fit(
    train_generator,
    epochs=num_epochs,
    steps_per_epoch=len(train_generator),
    validation_data=val_generator,
    validation_steps=len(val_generator),
    callbacks=custom_callbacks
)

print(history.history)

# Uncomment the plotting section if needed
# import matplotlib.pyplot as plt
# acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']
# loss = history.history['loss']
# val_loss = history.history['val_loss']
# epochs = range(1, len(acc) + 1)
# plt.plot(epochs, acc, 'bo', label='Training Accuracy')
# plt.plot(epochs, val_acc, 'b', label='Validation Accuracy')
# plt.title('Training and Validation Accuracy')
# plt.legend()
# plt.figure()
# plt.plot(epochs, loss, 'bo', label='Training Loss')
# plt.plot(epochs, val_loss, 'b', label='Validation Loss')
# plt.title('Training and Validation Loss')
# plt.legend()
# plt.show()

best_model = load_model(os.path.join(checkpoint_filepath, 'best_model.keras'))

# Generate predictions
test_generator.reset()
preds = best_model.predict(test_generator, verbose=1)

test_results = pd.DataFrame({
    "Filename": test_generator.filenames,
    "Prediction": preds.flatten()
})
print(test_results)
