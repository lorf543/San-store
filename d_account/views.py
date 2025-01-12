from django.shortcuts import render

# Create your views here.


def my_account(request):
    context = {}
    return render (request,'d_account/my_account.html ',context)
