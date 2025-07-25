from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django import forms
from django.contrib import messages

class HomePageView(TemplateView):
    template_name = "pages/home.html"

class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: Nicolas Rico",
            }
        )
        return context

class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "price": 1000}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 699}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 50}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 450}
    ] 
 
class ProductIndexView(View): 
    template_name = 'pages/products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = 'pages/products/show.html' 
    def get(self, request, id): 
        viewData = {} 
        try:
            product = Product.products[int(id)-1]
            viewData["title"] = product["name"] + " - Online Store" 
            viewData["subtitle"] =  product["name"] + " - Product information" 
            viewData["product"] = product 
            return render(request, self.template_name, viewData)
        except IndexError:
            return HttpResponseRedirect('/')
    
class ProductForm(forms.Form): 
    name = forms.CharField(required=True) 
    price = forms.FloatField(required=True) 
 
 
class ProductCreateView(View): 
    template_name = 'pages/products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            if price < 0:
                form.add_error('price', 'Price must be greater than 0')
                viewData = {}
                viewData["title"] = "Create product"
                viewData["form"] = form
                return render(request, self.template_name, viewData)
            messages.success(request, 'Product Created !')
            return redirect('form')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)