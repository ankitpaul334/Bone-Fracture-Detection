import numpy as np
import pandas as pd
import os.path
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.optimizers import Adam



#Load  X-ray dataset +ve/-ve
def load_path(path):
    dataset = []
    for folder in os.listdir(path):  # each body part folder
        folder = path + '/' + str(folder)
        if os.path.isdir(folder):  # Check folder
            for body in os.listdir(folder):  # subfolders 
                path_p = folder + '/' + str(body)
                for id_p in os.listdir(path_p):  # patient IDs
                    patient_id = id_p
                    path_id = path_p + '/' + str(id_p)
                    for lab in os.listdir(path_id):  # labels (fractured/normal)
                        if lab.split('_')[-1] == 'positive':  
                            label = 'fractured'
                        elif lab.split('_')[-1] == 'negative':  
                            label = 'normal'
                        path_l = path_id + '/' + str(lab)
                        for img in os.listdir(path_l):  # images in the folder
                            img_path = path_l + '/' + str(img)
                            dataset.append({'label': body, 'image_path': img_path})  # Store image path and label
    return dataset


''' load data from path'''
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
image_dir = THIS_FOLDER + '/Dataset'
data = load_path(image_dir)

labels = []
filepaths = []
Labels = ["Elbow", "Hand", "Shoulder"]

for row in data:
    labels.append(row['label'])
    filepaths.append(row['image_path'])

filepaths = pd.Series(filepaths, name='Filepath').astype(str) 
labels = pd.Series(labels, name='Label') 

images = pd.concat([filepaths, labels], axis=1) #df combining

''' 10% test 
    90% train - 80% train / 20% val
    total = 10% test, 72% training and 18% validation'''

train_df, test_df = train_test_split(images, train_size=0.9, shuffle=True, random_state=1)
     
#Preprocessing

train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
    validation_split=0.2)

test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.resnet50.preprocess_input)

train_images = train_generator.flow_from_dataframe(
    dataframe=train_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=64,
    shuffle=True,
    seed=42,
    subset='training'
)

val_images = train_generator.flow_from_dataframe(
    dataframe=train_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=64,
    shuffle=True,
    seed=42,
    subset='validation'
)

test_images = test_generator.flow_from_dataframe(
    dataframe=test_df,
    x_col='Filepath',
    y_col='Label',
    target_size=(224, 224),
    color_mode='rgb',
    class_mode='categorical',
    batch_size=32,
    shuffle=False
)

pretrained_model = tf.keras.applications.resnet50.ResNet50(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg')

pretrained_model.trainable = False

inputs = pretrained_model.input
x = tf.keras.layers.Dense(128, activation='relu')(pretrained_model.output)
x = tf.keras.layers.Dense(50, activation='relu')(x)
outputs = tf.keras.layers.Dense(len(Labels), activation='softmax')(x)
model = tf.keras.Model(inputs, outputs)
print(model.summary())

model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

''' early stop when our model is over fit or vanishing gradient, with restore best values'''
callbacks = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
history = model.fit(train_images, validation_data=val_images, epochs=25,
                    callbacks=[callbacks])

#save model to this path
model.save(THIS_FOLDER + "/weights/ResNet50_BodyParts.h5")
results = model.evaluate(test_images, verbose=0)
print(results)
print(f"Test Accuracy: {np.round(results[1] * 100, 2)}%")


''' create plots for accuracy and save it'''
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

''' create plots for loss and save it'''
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
