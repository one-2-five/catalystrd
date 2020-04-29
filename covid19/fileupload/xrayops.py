import filetype
import time 
import os, subprocess
import shutil 
import platform
import pandas as pd
import yaml
import dill
import cv2
import numpy as np
from covid19.settings import BASE_DIR
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def findfiletype(filename):
    try:
        output = filetype.guess(filename).extension
    except:
        output = "Unknown"
    return output

def train_input_model(filepath):
    try:
        print("Current dir is ",os.getcwd())
        os.chdir(BASE_DIR)
        print("Current dir is ",os.getcwd())
        if "Win" not in platform.platform():
            print("Os not Windows")
            basepath = os.getcwd()+"/documents/"
            source = basepath + filepath
            destinationbase  = os.getcwd()+"/fileupload/uploads/"
            if not os.path.exists(destinationbase):
                os.makedirs(destinationbase)
            destinationfilename = filepath.lower()
            destination = destinationbase+destinationfilename
            print("Starting Copy")
            print("Source is ", source)
            print("Destination is ",destination)
            shutil.copy(source,destination)
            print("Executing predict.py")
            os.chdir('./fileupload/')
            #subprocess.check_output("python ./predict.py",shell=True,stderr=subprocess.STDOUT)
            output = predictImage()
            if 'non-COVID-19' in str(output):
                resultStatus = 'Negative'
            else:
                resultStatus = 'Positive'
            print('Executing predict.py success')
            deletecontents(destinationbase)
            return resultStatus
        else:
            print("OS is Windows")
            basepath = os.getcwd()+'\\documents\\'
            source = basepath + filepath
            destinationbase  = os.getcwd()+'\\fileupload\\uploads\\'
            if not os.path.exists(destinationbase):
                os.makedirs(destinationbase)
            destinationfilename = filepath.lower()
            destination = destinationbase+destinationfilename
            print(os.getcwd())
            print("Starting Copy")
            shutil.copy(source,destination)
            print("Executing predict.py")
            os.chdir('.\\fileupload\\')
            #time.sleep(10)
            #subprocess.check_output("python .\\predict.py",shell=True,stderr=subprocess.STDOUT)
            output = predictImage()
            deletecontents(destinationbase)
            if 'non-COVID-19' in str(output):
                resultStatus = 'Negative'
            else:
                resultStatus = 'Positive'
            print('Executing predict.py success')
            return resultStatus
    except subprocess.CalledProcessError as e:
        os.chdir('..')
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        print('Executing predict.py Failed, This coming from xrayops.py')
        #time.sleep(10)
        resultStatus = 'Failed to Process'
        deletecontents(destinationbase)
        return resultStatus
    os.chdir(BASE_DIR)

def deletecontents(destinationbase):
    folder = destinationbase
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print('Deleting copied files')
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.chdir(BASE_DIR)

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
        return predictedClass