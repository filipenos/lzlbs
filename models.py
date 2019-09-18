class Client:
    def __init__(self, name, email, id=None):
        self.name = name
        self.email = email
        self.id = id


class FavoriteList:
    def __init__(self, client_id, id=None):
        self.client_id = client_id
        self.id = id


class Whitelist:
    def __init__(self, favorite_list_id, product_id, id=None):
        self.favorite_list_id = favorite_list_id
        self.product_id = product_id
        self.id = id
