import urllib.request, json

ENDPOINT = 'http://challenge-api.luizalabs.com/api/product/{}'

class ProductService:
    def list(page):
        baseurl = ENDPOINT.format('?page={}'.format(page or 1))
        try:
            with urllib.request.urlopen(baseurl) as url:
                return json.loads(url.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None

    def get(product_id):
        if product_id == None:
            return None

        baseurl = ENDPOINT.format(product_id)
        try:
            with urllib.request.urlopen(baseurl) as url:
                return json.loads(url.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None