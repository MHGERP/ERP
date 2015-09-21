from django.shortcuts import render

def purchasingFollowingViews(request):
    context={}
    return render(request,"purchasing/purchasing_following.html",context)
