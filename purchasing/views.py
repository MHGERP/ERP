from django.shortcuts import render

def purchasingFollowingViews(request):
    #chousan1989
    #
    #
    context={}
    return render(request,"purchasing/purchasing_following.html",context)


def pendingOrderViews(request):
    context = {}
    return render(request, "purchasing/pending_order.html", context)
