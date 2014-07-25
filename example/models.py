from django.db import models


class Author(models.Model):
    name = models.CharField('name', max_length=45, )

    def __unicode__(self):
        return u"%s" % self.name


class Book(models.Model):
    name = models.CharField('name', max_length=45, )
    iban = models.CharField('iban', max_length=34, )
    author = models.ForeignKey('Author', related_name='books', )

    def __unicode__(self):
        return u"%s" % self.name
