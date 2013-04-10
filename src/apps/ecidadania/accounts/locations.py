from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5)

    def __unicode__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
