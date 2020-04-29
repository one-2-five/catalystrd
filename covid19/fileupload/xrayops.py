import filetype
import time 
import os, subprocess
import shutil 
import platform

def findfiletype(filename):
    try:
        output = filetype.guess(filename).extension
    except:
        output = "Unknown"
    return output

def train_input_model(filepath):
    try:
        if "Win" not in platform.platform():
            print("Os not Windows")
            basepath = "./documents/"
            source = basepath + filepath
            destinationbase  = "./fileupload/uploads/"
            destinationfilename = filepath.lower()
            destination = destinationbase+destinationfilename
            print("Starting Copy")
            shutil.copy(source,destination)
            print("Executing predict.py")
            os.chdir('./fileupload/')
            subprocess.check_output("python ./predict.py",shell=True,stderr=subprocess.STDOUT)
            output=subprocess.check_output("python ./predict.py",shell=True,stderr=subprocess.STDOUT)
            print("#############################################################")
            print(output)
            deletecontents(destinationbase)
            if 'non-COVID-19' in str(output):
                resultStatus = 'Negative'
            else:
                resultStatus = 'Positive'
            print('Executing predict.py success')
            return resultStatus
        else:
            basepath = ".\\documents\\"
            source = basepath + filepath
            destinationbase  = ".\\fileupload\\uploads\\"
            destinationfilename = filepath.lower()
            destination = destinationbase+destinationfilename
            print("Starting Copy")
            shutil.copy(source,destination)
            print("Executing predict.py")
            os.chdir('.\\fileupload\\')
            subprocess.check_output("python .\\predict.py",shell=True,stderr=subprocess.STDOUT)
            output=subprocess.check_output("python .\\predict.py",shell=True,stderr=subprocess.STDOUT)
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
        print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        print('Executing predict.py Failed')
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
        
