from django.http import HttpResponse
# def admin_required(fun):
#     def wrapper(request):
#         if request.user.is_superuser == False:
#             return HttpResponse("Admin User Only")
#         else:
#             return fun(request)
#     return wrapper

from django.shortcuts import render
from django.contrib import messages
def admin_required(fun):
    def wrapper(request):
        if request.user.is_superuser == False:
            messages.error(request,"You are not authorized to access this page")
            return render(request,'erorr.html')
        else:
            return fun(request)
    return wrapper