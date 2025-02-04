from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic.base import TemplateView
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

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
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://38f51d56.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://38f51d56.us-south.apigw.appdomain.cloud/api/review"
        result = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context['reviews'] = result["reviews"]
        context['dealership_name'] = result["dealership_name"]
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    context['dealer_id'] = dealer_id
    if request.method == 'GET':
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect("djangoapp:add_review", dealer_id=dealer_id)
        else:
            car = CarModel.objects.get(pk=request.POST['car'])
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            review["purchase_date"] = request.POST['purchasedate']
            review["purchase"] = request.POST['purchasecheck']
            review["name"] = request.user.first_name+" "+request.user.last_name
            review["car_make"] = car.name
            review["car_model"] = car.carmake.name
            review["car_year"] = car.year.strftime('%Y')
            json_payload = dict()
            json_payload["review"] = review
            url = "https://38f51d56.us-south.apigw.appdomain.cloud/api/review"
            post_request(url, json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
