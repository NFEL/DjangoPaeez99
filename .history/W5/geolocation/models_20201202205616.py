# from django.db import models
from django.contrib.gis.db import models


class TehAddressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(city='تهران')


class Address(models.Model):
    STATE = [
        ('tehran', 'تهران'),
        ('alborz', 'البرز'),
        ('markazi', 'مرکزی'),
    ]

    state = models.CharField('استان', choices=STATE, max_length=20,blank=True, null=True)
    city = models.CharField('شهر', max_length=50,blank=True, null=True)
    street = models.CharField('خیابان', max_length=50,blank=True, null=True)
    alley = models.CharField('کوچه', max_length=50,blank=True, null=True)
    number = models.CharField('پلاک', max_length=50,blank=True, null=True)
    poste_code = models.CharField('کدپستی', max_length=50,blank=True, null=True)
    priority_address = models.SmallIntegerField(default=1)
    
    location = models.PointField('موقعیت جغرافیایی',geography=True)

    objects = models.Manager()
    teh_objects = TehAddressManager()


    def __str__(self) -> str:
        return str(self.location)