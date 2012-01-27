from django import forms

class SpreadsheetForm(forms.Form):
    node_id = forms.IntegerField()
    url = forms.URLField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    city = forms.CharField()
    province = forms.CharField()
    postal_code = forms.CharField(required=False)
    country = forms.CharField()
    email = forms.EmailField()
    latitude = forms.FloatField()
    longitude = forms.FloatField()
