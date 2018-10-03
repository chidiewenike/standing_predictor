import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
import numpy as np
import matplotlib.pyplot as plt
import json
import os

dirList = os.listdir()
notInDir = True
while notInDir:
    
    modelLoad = input("Which model would you like to input? ")
    if (modelLoad in dirList):
        notInDir = False
    else:
        print("Input a valid h5 model file.")

dataCount = 0
dataList = []
trainingData = []
trainingLabel = []
testingData = []
testingLabel = []

word = "English_Premier_League"
for file in dirList:
    if word in file:
        dataCount += 1
        dataList.append(file)
trainingCount = int(dataCount * 3/4)
testingCount = int(dataCount - trainingCount)


seasonJson = [] 
oneSample = []
matSample = []
matLabel = []
i = 0
while (i < dataCount):
    with open(dataList[i]) as json_data:
        seasonJson.append(json.load(json_data))
    i += 1


oneTest = []
j = 0
while (j < trainingCount):
    k = 0
    matLabel = []
    matSample = []
    while (k < 20):
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Home_Wins"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Home_Losses"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Home_Draws"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Away_Wins"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Away_Draws"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Away_Losses"]))
        trainingData.append(oneSample)
        oneSample = []
        trainingLabel.append(float(k+1))
        k += 1
    j += 1

matSample = []
matLabel = []
oneTest = []
j = trainingCount
while (j < dataCount):
    k = 0
    matLabel = []
    matSample = []
    while (k < 20):
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Home_Wins"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Home_Losses"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Home_Draws"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Away_Wins"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Away_Draws"]))
        oneSample.append(float(seasonJson[j]["Season"]["Standing"]["Team"][k]["Away_Losses"]))
        testingData.append(oneSample)
        oneSample = []
        testingLabel.append(float(k+1))
        k += 1
    j += 1

trainingData = np.array(trainingData)
trainingLabel = np.array(trainingLabel)
testingData = np.array(testingData)
testingLabel = np.array(testingLabel)


trainingData = trainingData / 19.0
testingData = testingData / 19.0

print("Training Data:")
print(trainingData)
print("Training Label:")
print(trainingLabel)
print("Testing Data:")
print(testingData)
print("Testing Label:")
print(testingLabel)
print(len(trainingLabel))

model = keras.Sequential([
    keras.layers.Dense(128,activation=tf.nn.relu, input_shape=(6,)),
    keras.layers.Dense(280,activation=tf.nn.softmax)
])
model.summary()

model = keras.models.load_model(modelLoad)

model.compile(optimizer=tf.train.AdamOptimizer(),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
model.fit(trainingData,trainingLabel,epochs=2000)

model.summary()
test_loss, test_acc = model.evaluate(testingData,testingLabel)
print('Test accuracy: ', test_acc)

predictions = model.predict(testingData)
predictVal = [[10.0,4.0,5.0,3.0,6.0,10.0]]
predictVal = np.array(predictVal)
predict2 = model.predict(predictVal)
print(np.argmax(predict2))
accPer = int(100*test_acc)

dirList = os.listdir()
count = 0
inDir = False
while not(inDir):
    count+=1
    modelStorage = "EPLModel" + "_" + str(accPer) +  "_" + str(count) + ".h5" 
    inDir = True
    for file in dirList:
        if modelStorage in file:
            inDir = False

model.summary()
print("Model saved: " + modelStorage)
model.save(modelStorage)
