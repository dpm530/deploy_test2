from __future__ import unicode_literals
from django.db import models
import re,bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def currentUser(self, request):
        id=request.session['user_id']

        return User.objects.get(id=id)

    def validateUser(self,form_data):
        errors=[]
        if len(form_data['name'])==0:
            errors.append('Name is Required.')
        if len(form_data['alias'])==0:
            errors.append('Alias is Required.')
        if len(form_data['email'])==0:
            errors.append('Email is Required.')
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('Please enter a valid email!')
        if len(form_data['password'])==0 or len(form_data['password'])<8:
            errors.append('Password must  be at least 8 characters long.')
        if form_data['password'] != form_data['password_confirmation']:
            errors.append('Password Confirmation must match Password.')

        return errors

    def validateLogin(self,form_data):
        errors=[]

        if len(form_data['email'])==0:
            errors.append('Email is Required.')
        if len(form_data['password'])==0:
            errors.append('Password is Required.')

        return errors

    def createUser(self,form_data):
        password=str(form_data['password'])
        hashed_pw=bcrypt.hashpw(password, bcrypt.gensalt())

        user=User.objects.create(
            name=form_data['name'],
            alias=form_data['alias'],
            email=form_data['email'],
            password=hashed_pw,
        )

        return user


class User(models.Model):
    name=models.CharField(max_length=255)
    alias=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    friends=models.ManyToManyField('self',related_name='friended_by')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
