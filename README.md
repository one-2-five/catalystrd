This is a simple web application based on Django framework(python)
We strongly recommend to use anaconda and install python in specific env

Steps to be followed  



1.	Install Ananconda , follow  https://docs.anaconda.com/anaconda/install/
2.	Create your env ref: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf 
3.	Change to newly created ENV using command
    #conda activate envname
4.	Install python version 3.7.7 using command 
    #conda install python=3.7.7
5.	Install packages required for this setup using command
    #pip install -r requirements.txt

    requirements.txt file you will find in this repo : "covid19webapp/covid19/"
    
6.	Run Django server using  command
    #python manage.py runserver
    
    Access your application using http://127.0.0.1:8000/xray url. 
    
7.  default username is admin and password is admin
    please change once you login in admin console

8.  Create normal user in admin console


