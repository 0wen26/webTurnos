from django import forms
from .models import PDFUpload

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFUpload
        fields = ['file']  # Puedes incluir otros campos si los necesitas
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()  # O cualquier otro campo que necesites
    
class OvertimeUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Sube tu PDF')
