from models import Client, FavoriteList, Whitelist


class ClientDAO:
    def __init__(self, db):
        self.__db = db

    def save(self, client):
        cursor = self.__db.connection.cursor()

        if client.id:
            cursor.execute('UPDATE client SET name=%s, email=%s WHERE id=%s LIMIT 1', (client.name, client.email, client.id))
        else:
            cursor.execute('INSERT INTO client (name, email) VALUES (%s, %s)', (client.name, client.email))
            client.id = cursor.lastrowid
        self.__db.connection.commit()
        return client

    def get(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute('SELECT id, name, email FROM client WHERE id=%s LIMIT 1', (id,))
        result = cursor.fetchone()
        if result is None:
            return None
        return Client(result[1], result[2], result[0])

    def get_by_email(self, email):
        cursor = self.__db.connection.cursor()
        cursor.execute('SELECT id, name, email FROM client WHERE email=%s LIMIT 1', (email,))
        result = cursor.fetchone()
        if result is None:
            return None
        return Client(result[1], result[2], result[0])

    def delete(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute('DELETE FROM client WHERE id=%s LIMIT 1', (id, ))
        self.__db.connection.commit()


class FavoriteListDAO:
    def __init__(self, db):
        self.__db = db

    def save(self, client, favorite_list):
        cursor = self.__db.connection.cursor()
        cursor.execute('INSERT INTO favorite_list (client_id) VALUES (%s)', (client.id,))
        favorite_list.id = cursor.lastrowid
        self.__db.connection.commit()

    def get(self, client_id):
        cursor = self.__db.connection.cursor()
        cursor.execute('SELECT id, client_id FROM favorite_list WHERE client_id=%s LIMIT 1', (client_id, ))
        result = cursor.fetchone()
        if result is None:
            return None
        return FavoriteList(result[1], result[0])


class WhitelistDAO:
    def __init__(self, db):
        self.__db = db

    def save(self, whitelist):
        cursor = self.__db.connection.cursor()
        cursor.execute('INSERT INTO whitelist (favorite_list_id, product_id) VALUES (%s, %s)', (whitelist.favorite_list_id,whitelist.product_id))
        whitelist.id = cursor.lastrowid
        self.__db.connection.commit()

    def list(self, client_id):
        cursor = self.__db.connection.cursor()
        cursor.execute('SELECT w.id, w.favorite_list_id, w.product_id FROM whitelist w JOIN favorite_list f ON f.id = w.favorite_list_id WHERE f.client_id=%s', (client_id,))
        fetch = cursor.fetchall()
        return parse_whitelist(fetch)

    def exists(self, client_id, product_id):
        cursor = self.__db.connection.cursor()
        cursor.execute(
            'SELECT count(*) AS size FROM whitelist w JOIN favorite_list f ON f.id = w.favorite_list_id WHERE f.client_id=%s AND w.product_id=%s',
            (client_id,product_id))
        result = cursor.fetchone()
        if result is None or result[0] == 0:
            return False
        return True


def parse_whitelist(fetch):
    def parse(result):
        return Whitelist(result[1], result[2], result[0])
    return list(map(parse, fetch))
