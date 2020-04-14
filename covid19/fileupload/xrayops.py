import filetype
import time 
import os, subprocess
import shutil 

def findfiletype(filename):
    try:
        output = filetype.guess(filename).extension
    except:
        output = "Unknown"
    return output

def train_input_model(filepath):
    try:
        #print("Inside trainmodel function")
        basepath = "C:\\Users\\eshit\\Desktop\\covid19\\covid19\\documents\\"
        filepath = filepath.lower()
        source = basepath + filepath  

        destination  = "C:\\wamp64\\www\\uploads\\"
        print("Starting Copy")
        shutil.copy(source,destination)
        print("Executing predict.py")
        command = "python C:\Repo\covid-cxr-master\src\predict.py " 
        #time.sleep(3)
        #output="non-COVID-19"
        output=subprocess.check_output("python C:/Repo/covid-cxr-master/src/predict.py",shell=True,stderr=subprocess.STDOUT)
        print("#############################################################")
        print(output)
        deletecontents(destination)
        if 'non-COVID-19' in str(output):
            resultStatus = 'Negative'
#        elif 'COVID-19 NEGATIVE' in str(output):
#            resultStatus = 'COVID-19 NEGATIVE'
        else:
            resultStatus = 'Positive'
        print('Executing predict.py success')
        return resultStatus
    except:
        print('Executing predict.py Failed')
        resultStatus = 'Failed to Process'
        deletecontents(destination)
        return resultStatus
        #time.sleep(5)

def deletecontents(destination):
    folder = destination
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
        
"""
def train_input_model(filepath):
    #print("Inside trainmodel function")
    try:
        print('Executing predict.py and filepath is ', filepath)
        #os.system('python C:\Repo\covid-cxr-master\src\predict.py' filepath)
        subprocess.run(["python", "C:\Repo\covid-cxr-master\src\predict.py", filepath])
        print('Executing predict.py success')
        return true
    except:
        print('Executing predict.py Failed')
        #time.sleep(5)
        return False
"""