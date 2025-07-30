import jwt

class JWT_Manager:
    def __init__(self):
        with open("private.pem", "rb") as f:
            self.private_key = f.read()

        with open("public.pem", "rb") as f:
            self.public_key = f.read()

        self.algorithm = "RS256"

    def encode(self, data):
        try:
            return jwt.encode(data, self.private_key, algorithm=self.algorithm)
        except Exception as e:
            print("Error al codificar token:", e)
            return None

    def decode(self, token):
        try:
            return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        except Exception as e:
            print("Error al decodificar token:", e)
            return None 