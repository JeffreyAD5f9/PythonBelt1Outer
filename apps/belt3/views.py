from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import *


def userInit(request):
    if 'userCurrent' in request.session:
            return User.objects.get(id = request.session['userCurrent'])



def index(request):

    return render(request, "belt3/index.html")



def Register(request):
    if request.method != 'POST':
        return redirect('/')
    test = User.objects.validUser(request.POST)

    if test['status'] == True:
        user = User.objects.userCreate(request.POST)
        request.session['userCurrent'] = user.id
        return redirect('/gotowishlist')
    else:
        for error in test['Errors']:
            messages.add_message(request, messages.ERROR, error, extra_tags="register")
        return redirect('/')



def GoToWishlist(request):
    user = userInit(request)
    wishItems = user.USER.all()
    Items= []
    for item in wishItems:
        Items.append(item.ItemObj.id)
    context = {
        'userInit': userInit(request),
        'wishItems': wishItems,
        'items' : Item.objects.exclude(id__in = Items)
    }

    return render(request, 'belt3/wishlist.html', context)


def GoToItemCreate(request):

    return render(request, 'belt3/itemCreate.html')


def Login(request):
    if request.method != 'POST':
        return redirect('/')
    test = User.objects.checkUser(request.POST)
    if test['status'] == True:
        request.session['userCurrent'] = test['user'].id
        return redirect('/gotowishlist')
    else:
        for error in test['Errors']:
		    messages.add_message(request, messages.ERROR, error, extra_tags="login")
        return redirect('/')



def Logout(request):
    request.session.clear()

    return redirect('/')



def ItemCreate(request):
    if request.method != 'POST':
        return redirect('/')
    test = Item.objects.validItem(request.POST, userInit(request))

    if test['status'] == True:
        item = Item.objects.itemCreator(request.POST, userInit(request))

        return redirect('/gotowishlist')
    else:
        for error in test['Errors']:
		    messages.add_message(request, messages.ERROR, error, extra_tags="create")
        return redirect('/gotowishlist')

def addExistingItem(request, itemAdd):
        user = userInit(request)
        item = Item.objects.wishForItem(User.objects.get(id = itemAdd), userInit(request))
        return redirect('/gotowishlist')


def Remove(request, itemRemove):
    Item.objects.get(id = itemRemove).delete()

    return redirect('/gotowishlist')



def viewItem(request, item):
    itemView = Item.objects.get(id = item)
    Users = item.USER.all()
    wishUsers = []
    for user in Users:
        wishUsers.append(itemView.UserObj)
    print wishUsers
    context = {
        'item' : itemView,
        'users' : wishUsers
    }

    return render(request, "belt3/viewItem.html", context)
