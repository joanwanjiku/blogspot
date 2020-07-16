import urllib.request
import json

def get_random_quote():
    random_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    with urllib.request.urlopen(random_url) as url:
        result = url.read()
        response = json.loads(result)
    return response

