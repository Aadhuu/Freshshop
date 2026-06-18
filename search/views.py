from django.db.models import Q
from django.shortcuts import render
from django.views import View

from shop.models import Product


class SearchView(View):
    def get(self, request):
        query = request.GET['q']
        p = Product.objects.filter(Q(name__icontains=query) |
                                Q(description__icontains=query) |
                                Q(price__icontains=query))
        context = {'products': p}
        return render(request,'search.html',context)
