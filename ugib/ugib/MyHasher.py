from django.contrib.auth.hashers import BasePasswordHasher
import bcrypt

class MyHasher:
    algorithm = "my"
    __salt = 10
    
    def salt(self):
        return bcrypt.gensalt(self.__salt)
    
    
    def encode(self, password, salt):
        return self.make_password(password)
    
    
    def make_password(self, password, hasher='default') -> str:
        if password:
           password = password.encode()
           return str(bcrypt.hashpw(password, self.salt())).split("'")[1]
        return None
        
        
    def check_password(self, password, hashed, setter=None, preferred='default'):
        return bcrypt.checkpw(password.encode(), hashed.encode())
            



