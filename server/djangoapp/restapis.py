import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    # Call get method of requests library with URL and parameters
    if 'apikey' in kwargs:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs, auth=HTTPBasicAuth('apikey',kwargs['apikey']))
    else:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            if dealer["_id"][0] == "_":
                continue
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealerId=kwargs["dealer_id"])
    if json_result:
        reviews = json_result["reviews"]
        for review in reviews:
            if review["_id"][0] == "_":
                continue
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], 
                            purchase=review["purchase"], review=review["review"], 
                            purchase_date=review["purchase_date"], car_make=review["car_make"], 
                            car_model=review["car_model"], car_year=review["car_year"], 
                            sentiment=analyze_review_sentiments(review["review"]))
            results.append(review_obj)

    return {"reviews": results, "dealership_name": json_result["dealership_name"]}


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    response = get_request("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com" \
                            "/instances/907132ea-df9d-46ce-adb8-d5d49c827a7a/v1/analyze", text=text, 
                            version="2021-08-01", features=["sentiment"], 
                            apikey="SBLTeFzPKBwQ-Hu8ebSYNwcg7rieY1J2WRGsRD74TVqD")
    print(response)
    return response["sentiment"]["document"]["label"]

