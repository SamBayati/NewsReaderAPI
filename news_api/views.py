# Import standard Python libraries for making HTTP requests and handling URLs
import http.client, urllib.parse

# Import Django's render function to display HTML templates
from django.shortcuts import render

# Import the requests library for making HTTP requests more easily
import requests

# Define the API key for accessing the news API 
# from thenewsapi.com 
API_KEY = 'rxKTZxW3nhxnLT5POZxuNPp2FsB4ReIWnCZrl3PG'

# Main view function that handles requests to the homepage
def home(request):
   # Use try-except to handle potential errors during API request
   try:
       # Define the base URL for the news API endpoint
       url = 'https://api.thenewsapi.com/v1/news/top'
       
       # Set up initial parameters for the API request including API key and result limit
       params = {
           'api_token': API_KEY,
           'limit': 3
       }
       
       # Check if any filter parameters were applied to the url by the user
       if request.GET:
           # Get language parameter from URL, default to empty string if not present
           language = request.GET.get('language','')
           # Get category parameter from URL, default to empty string if not present
           category = request.GET.get('category','')
           
           
           # If category was selected, add it to the API parameters
           if category:
               params['categories'] = category
           # If language was selected, add it to the API parameters
           if language:
               params['language'] = language
       

       # Send GET request to the API with our parameters
       response = requests.get(url, params=params)
       # Raise an exception if the request was unsuccessful
       response.raise_for_status()
       
       # Convert the JSON response to a Python dictionary
       data = response.json()
       # Extract the news articles from the 'data' key, default to empty list if not found
       news_items = data.get('data', [])
       
       # Prepare the context dictionary to send to the template
       context = {
           # list of news article
           'data': news_items,
           'meta': data.get('meta', {}),
           # selected langauge
           'selected_language': request.GET.get('language', ''),
           # selected category
           'selected_category': request.GET.get('category', '')
       }
       
       # Render the template with context data and return it
       return render(request, 'news_api/home.html', context)
   
       

   # Handle any errors that occurred during the API request
   except requests.RequestException as e:
       # Prepare error context
       context = {
           'error': f"Failed to fetch news: {str(e)}", # Error message
           'data': []                                  # Empty list since we have no news to display
       }

       # Render the template with error information
       return render(request, 'news_api/home.html', context)







# def home2(request):

#     conn = http.client.HTTPSConnection('api.thenewsapi.com')

#     params = urllib.parse.urlencode({
#     'api_token': API_KEY,
#     'categories': 'business,tech',
#     'limit': 50,
#     })

#     conn.request('GET', '/v1/news/all?{}'.format(params))

#     res = conn.getresponse()
#     data = res.read()

#     data2= data.decode('utf-8')

#     # return render (request, 'news_api/home.html',data2) 

    