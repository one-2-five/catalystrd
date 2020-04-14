from django import forms
from . models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description','document',  )
        #fields = ('description','document', )
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(DocumentForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['description'].required = True
        self.fields['document'].required = True