from django.shortcuts import render

# Create your views here.
from .models import Product
# Getting one item
def detail_view(request,object_id=None):
    print(request)
    if object_id is not None:
        product = Product.objects.get(id=object_id)
        template = "detail_view.html"
        context = {
            "object": product
        }
    else:
        raise Http404
    return render(request, template, context)


def list_view(request):
    # Getting a list of items
    print(request)
    queryset = Product.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)
