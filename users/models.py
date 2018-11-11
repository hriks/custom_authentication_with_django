# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, IntegrityError

import json


class User(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        try:
            current = User.objects.get(id=self.id)
            if (current.password != str(self.password)):
                self.password = User.get_hashed_password(str(self.password))
        except User.DoesNotExist:
            self.username = self.username.lower()
            self.password = User.get_hashed_password(str(self.password))
        super(User, self).save(*args, **kwargs)

    @staticmethod
    def get_hashed_password(password):
        # Hash a password for the first time
        # Using bcrypt, the salt is saved into the hash itself
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    def check_password(self, password):
        # Check hased password. Using bcrypt, the salt is saved into the hash itself
        import bcrypt
        try:
            return bcrypt.hashpw(str(password), str(self.password)) == str(self.password)
        except Exception:
            # If Password has invalid Salt
            return False

    @classmethod
    def validateUser(cls, request):
        data = request.POST.dict()
        try:
            user = User.objects.get(username=data.get('username', ''))
            validated = user.check_password(data.get('password', ''))
            if validated:
                return user.accessToken(), "Hi %s!. You had been successfully authenticated." % user.username
            return None, "Invalid Password Provided."
        except User.DoesNotExist:
            return None, 'Invalid Username Provided.'
        return None, 'Something went wrong! Please try again.'

    @classmethod
    def getAuthenticatedUser(cls, request):
        try:
            data = json.loads(request.session['authToken'])
            return cls.objects.get(username=data['username'])
        except cls.DoesNotExist:
            return None

    def accessToken(self):
        return json.dumps({"username": self.username})

    @classmethod
    def createNew(cls, data):
        try:
            kwargs = {
                "username": data.get('username', ''),
                "password": data.get("password", ''),
                "name": data.get("name")
            }
            return cls.objects.create(
                **kwargs), "User successfully created. your username %s" % kwargs["username"]
        except IntegrityError:
            return None, "Username Already Exists. Please try again with another username."
