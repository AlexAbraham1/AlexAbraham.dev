from google.cloud import firestore

class FireStore():

    def __init__(self):
        self._db = firestore.Client()

    def get_value(self, key):
        settings = list(self._db.collection(u'settings').get())[0]
        return settings.get(key)