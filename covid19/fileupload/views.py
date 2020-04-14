from django.shortcuts import render
from . forms import DocumentForm
from . models import Document
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from . xrayops import findfiletype, train_input_model
from django.utils import timezone

#from . trainmodel import trainmodel
# Create your views here.

def model_form_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                filepath = obj.document
                obj.filetype = findfiletype(filepath)
                form.save()
                return redirect('/xray/upload/')
        else:
            form = DocumentForm()
        return render(request, 'upload.html', {
            'form': form
        })
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def xray_list(request):
    if request.user.is_authenticated:
        content = {'xray_list': Document.objects.all()}
        return render(request, "xraylist.html", content)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def trainmodel(request,id=0):
    obj = get_object_or_404(Document,pk=id)
    filepath = obj.document.name.split('/')[1]
    print("Got Object and filepath os ", filepath)
    updatedtime = timezone.now()
    try:
        status_of_covid = train_input_model(filepath)
        status_of_training="True"
        #print("Try works")
    except Exception as e:
        print("Exception follows")
        print(e)
        status_of_covid ="Failed to Process"
        status_of_training="False"
    Document.objects.filter(pk=id).update(training_status=status_of_training)
    Document.objects.filter(pk=id).update(covidstate=status_of_covid)
    Document.objects.filter(pk=id).update(updated=updatedtime)
    return redirect('/xray/')
    
def xray_delete(request,id=0):
    if request.user.is_authenticated:
        xray_item=Document.objects.get(pk=id)
        xray_item.delete()
        return redirect('/xray/')
    else:
        return redirect('/xray/')