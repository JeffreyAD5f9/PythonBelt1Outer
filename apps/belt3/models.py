from __future__ import unicode_literals

from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def validUser(self, post):
        valid = True
        errors = []
        if len(post.get('name')) == 0:
            errors.append('Name must not be empty.')
            valid = False
        if len(post.get('username')) == 0:
            errors.append('Username must not be empty.')
            valid = False
        if len(post.get('email')) == 0:
            errors.append('Email must not be empty.')
            valid = False
        if post.get('cpassword') != post.get('password'):
            errors.append('User Password and Confirmation do not Match.')
            valid = False
        return {"status" : valid, "Errors" : errors}



    def userCreate(self, post):
        return User.objects.create(
            Name = post.get('name'),
            Username = post.get('username'),
            Email = post.get('email'),
            Pass = bcrypt.hashpw(post.get('password').encode(),bcrypt.gensalt())
        )



    def checkUser(self, post):
        valid = True
        errors = []
        user = User.objects.filter(Email = post.get('logemail')).first()

        if len(post.get('logemail')) == 0:
            errors.append('Email must not be empty.')
            valid = False
        if len(post.get('logpassword')) == 0:
            errors.append('Enter Password.')
            valid = False
        if not user:
            errors.append('Email not found in Database.')
            valid = False
        else:
            if bcrypt.hashpw(post.get('logpassword').encode(), user.Pass.encode()) != user.Pass:
                errors.append('Email and Password do not Match.')
                valid = False
            else:
                return {'status': True, 'user': user}
        return {"status" : valid, "Errors" : errors}



class ItemManager(models.Manager):
    def validItem(self, post, currentUser):
        valid = True
        errors = []

        if len(post.get('itemName')) == 0:
            messages.append('Name of Item must not be empty.')
            valid = False

        return {"status" : valid, "Errors" : errors}


    def wishForItem(self, post, currentUser):
        valid = True
        errors = []
        item = Item.objects.filter(ItemName = post.get('itemName')).first()
        return Item.objects.create(
            ItemName = item.ItemName,
            UserObj = currentUser,
            ItemObj = item
        )


    def itemCreator(self, post, currentUser):
        return Item.objects.create(
            ItemName = post.get('itemName'),
            UserObj = currentUser,
            ItemObj = currentUser
        )




class User(models.Model):
    Name = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Pass = models.CharField(max_length=255)
    CPass = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.Name + " " + self.Username + " " + self.Email

class Item(models.Model):
    ItemName = models.CharField(max_length=255)
    UserObj = models.ForeignKey(User, related_name = "USER")
    ItemObj = models.ForeignKey(User, related_name = "ITEM")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ItemManager()
