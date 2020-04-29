import filetype
import time 
import os, subprocess
import shutil 
import platform
from covid19.settings import BASE_DIR

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
            output=subprocess.check_output("python ./predict.py",shell=True,stderr=subprocess.STDOUT)
            print("#############################################################")
            print(output)
            print(destinationbase)
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
            destinationfilename = filepath.lower()
            destination = destinationbase+destinationfilename
            print(os.getcwd())
            print("Starting Copy")
            shutil.copy(source,destination)
            print("Executing predict.py")
            os.chdir('.\\fileupload\\')
            #time.sleep(10)
            #subprocess.check_output("python .\\predict.py",shell=True,stderr=subprocess.STDOUT)
            output=subprocess.check_output("python .\predict.py",shell=True,stderr=subprocess.STDOUT)
            #os.chdir('..')
            print("#############################################################")
            print(output)
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
