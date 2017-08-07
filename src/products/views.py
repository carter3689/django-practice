from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
# Create your views here.
from .models import Product

def detail_slug_view(request,slug=None):
    print(request)
    try:
        product = get_object_or_404(Product,slug=slug)
    except:
        product = Product.objects.filter(slug=slug).order_by("title").first() # This will gain access to our slug and order by our title
    print(slug)
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)
# Getting one item
def detail_view(request,object_id=None):
    print(request)
    product = get_object_or_404(Product,id=object_id)
    template = "detail_view.html"
    context = {
        "object": product
    }
    return render(request, template, context)

####### Reference Code ###################

    # if object_id is not None:
    #     try:
    #         product = Product.objects.get(id=object_id)
    #     except Product.DoesNotExist:
    #         product = None
    #     template = "detail_view.html"
    #     context = {
    #         "object": product
    #     }
    # else:
    #     raise Http404
    # return render(request, template, context)


def list_view(request):
    # Getting a list of items
    print(request)
    queryset = Product.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)
