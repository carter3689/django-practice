from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# Create your views here.

from digitalmarket.mixins import MultiSlugMixin

from .forms import ProductModelForm
from .models import Product

#Creating a ListView using the Class Based Version of the views
class ProductDetailView(MultiSlugMixin,DetailView):
    model = Product

    # def get_object(self,*args, **kwargs):
    #     print(self.kwargs)
    #     slug = self.kwargs.get("slug")
    #     ModelClass = self.model
    #     if slug is not None:
    #             try:
    #                 obj = get_object_or_404(ModelClass,slug=slug)
    #             except:
    #                 obj = ModelClass.objects.filter(slug=slug).order_by("title").first()
    #     else:
    #         obj = super(ProductDetailView,self).get_object(*args,**kwargs)
    #     return obj

    def get_context_data(self,**kwargs):
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        print(context)
        return context

#Creating a ListView using the Class Based Version of the views
class ProductListView(ListView):
    model = Product
    # template_name = "list_view.html"
    #
    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView,self).get_context_data(**kwargs)
    #     print(context)
    #     context["queryset"] = self.get_queryset()
    #     return context

    def get_queryset(self,*args,**kwargs):
        qs = super(ProductListView,self).get_queryset(**kwargs) #The super keyword is referring to the parent class - which in the case is ProductListView()
        return qs

def create_view(request):
    print(request.POST)
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data.get("publish"))
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "form":form
    }
    return render(request,template,context)

def update_view(request,object_id=None):
    print(request)
    product = get_object_or_404(Product,id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        print(form.cleaned_data.get("publish"))
        instance = form.save(commit=False)
        #instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "object": product,
        "form":form
    }
    return render(request, template, context)

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
