import pandas as pd
import yaml
import dill
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def remText(img):
    mask = cv2.threshold(img, 230, 255, cv2.THRESH_BINARY)[1][:, :, 0].astype(np.uint8)
    img = img.astype(np.uint8)
    remTextResult = cv2.inpaint(img, mask, 10, cv2.INPAINT_NS).astype(np.float32)
    return remTextResult
    
def predictInstance(x, model):
    y = model.predict(x)  
    if y.shape[1] == 1:
        probsPredicted = np.concatenate([1.0 - y, y], axis=1)  
    else:
        probsPredicted = y
    return probsPredicted





def predictImage(imageDirectory=None):

    # Load Config.YML
    cfg = yaml.full_load(open("./config.yml", 'r'))

    # Restore the model and class indices
    model = load_model(cfg['MODELPATH'], compile=False)
    classIndex = dill.load(open(cfg['CLASS_INDEX'], 'rb'))
    classNames = cfg['CLASSES']

    
    col_names = ['Image Filename', 'Predicted Class']
    for c in cfg['CLASSES']:
        col_names.append('p(' + c + ')')
    if imageDirectory is None:
        imageDirectory = cfg['INPUTPATH']
    
    imagedataFrame = pd.DataFrame({'filename': os.listdir(imageDirectory)})

    
    imageDataGen = ImageDataGenerator(preprocessing_function=remText, samplewise_std_normalization=True,
                                 samplewise_center=True)
    imageIter = imageDataGen.flow_from_dataframe(dataframe=imagedataFrame, directory=imageDirectory, x_col="filename",
                                          target_size=cfg['IMGDIM'], batch_size=1, class_mode=None,
                                          shuffle=False)

    # Predict all images in the input directory
    rows = []

    for filename in imagedataFrame['filename'].tolist():

        # Get preprocessed image for prediction.
        try:
            x = imageIter.next()
        except StopIteration:
            break
        y = np.squeeze(predictInstance(x, model))

       
        p = [y[classNames.index(c)] for c in classIndex]
        predictedClass = classNames[np.argmax(p)]
        print(predictedClass)

if __name__ == '__main__':
    remTextResults = predictImage()
