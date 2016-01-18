# coding: UTF-8
from django.shortcuts import render
from django.db.models import Q
from purchasing.models import *
from django.contrib.auth.models import User

a = ContractDetail()
a.user = User.objects.get(username="123")
a.amount = 0
a.bidform = BidForm.objects.get(bid_id="111")
a.save()
