from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic.base import TemplateView
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Homepage View
class Homepage(TemplateView):
    template_name = 'djangoapp/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Homepage, self).get_context_data(*args, **kwargs)
        context['name'] = 'Best Cars'
        return context

# Create an `about` view to render a static about page
class About(TemplateView):
    template_name = 'djangoapp/about.html'

    def get_context_data(self, *args, **kwargs):
        context = super(About, self).get_context_data(*args, **kwargs)
        context['name'] = 'About Us'
        return context


# Create a `contact` view to return a static contact page
class Contact(TemplateView):
    template_name = 'djangoapp/contact.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Contact, self).get_context_data(*args, **kwargs)
        context['name'] = 'Contact Us'
        return context

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

