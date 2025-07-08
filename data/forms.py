from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Select CSV File",
        widget=forms.ClearableFileInput(attrs={
            'class': 'file-input'
        })
    )