from django import forms

class NearByReastaurants(forms.ModelForm):
    class class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'