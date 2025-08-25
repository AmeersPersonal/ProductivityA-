import uuid as id

class User():
    def __init__(self, username, email, uuid=None):
        self.username = username
        self.email = email
        if not uuid:
            uuid = str(id.uuid4())
        self.uuid  = uuid

    def get_uuid(self):
        return self.uuid
    
    def get_email(self):
        return self.email

    def get_username(self):
        return self.name

    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email        