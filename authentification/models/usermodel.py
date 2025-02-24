from pymongo import MongoClient

def get_users_collection():
    client = MongoClient('mongodb+srv://mariembnacef:azerty123@cluster0.0e48dj1.mongodb.net/?retryWrites=true&w=majority')
    db = client['queney']
    return db['utilisateurs']

class User:
    def __init__(self, email, password, name, role, status):
        self.email = email
        self.password = password
        self.name = name
        self.status = status
        self.role = role

    def save(self):
        # Créer un dictionnaire avec les données de l'utilisateur
        user_data = {
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'role': self.role,
            'status': self.status
        }
        # Insérer le dictionnaire dans la collection "utilisateurs" de la base de données
        result = collection.insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def find_by_email(email):
        # Rechercher un utilisateur dans la collection "utilisateurs" par email
        user = collection.find_one({'email': email})
        return user

    def __repr__(self):
        # Méthode pour représenter l'objet utilisateur sous forme de chaîne de caractères
        return f"User(email='{self.email}', name='{self.name}', role='{self.role}', status='{self.status}')"



