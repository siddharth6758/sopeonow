from django import forms

def validate_csv(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError("File must be a CSV")
    return value

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Select CSV File",
        required=True,
        validators=[validate_csv],
        widget=forms.ClearableFileInput(attrs={
            'class': 'file-input'
        })
    )