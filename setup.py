# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-like-syste',
    version='0.0.1',
    author=u'Domenik Jones',
    author_email='domenik.jones.gmail.com',
    packages=['like_system'],
    url='https://github.com/r00tl3ss/django-like-system.git',
    license='BSD licence, see LICENCE.rst',
    description='Django based like system. Inspired by django.contrib.comments.',
    long_description=open('README.md').read(),
)