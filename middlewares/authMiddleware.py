from functools import wraps
from flask import jsonify, request
import logging
from authentification.authQueney import users_collection  # Import de la collection MongoDB

def get_user_role():
    """ Récupère le rôle de l'utilisateur via les headers ou la base de données """
    email = request.headers.get('User-Email')  # Récupération de l'email depuis les headers

    if not email:
        logging.warning("Tentative d'accès sans email dans les headers.")
        return None  # Aucun email fourni, donc accès interdit
    
    user = users_collection.find_one({"email": email})

    if not user:
        logging.warning(f"Utilisateur non trouvé pour l'email : {email}")
        return None  # L'utilisateur n'existe pas en base

    return user.get("role")  # Retourne le rôle de l'utilisateur

def admin_required(f):
    """ Décorateur pour restreindre l'accès aux admins et superadmins """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = get_user_role()

        if not user_role:
            return jsonify({'message': 'Accès refusé. Aucun utilisateur trouvé.'}), 403
        
        logging.info(f"User role: {user_role}")

        if user_role not in ['admin', 'superadmin']:
            return jsonify({'message': 'Accès refusé. Seuls les admins et superadmins sont autorisés.'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def superadmin_required(f):
    """ Décorateur pour restreindre l'accès uniquement aux superadmins """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = get_user_role()

        if not user_role:
            return jsonify({'message': 'Accès refusé. Aucun utilisateur trouvé.'}), 403
        
        logging.info(f"User role: {user_role}")

        if user_role != 'superadmin':
            return jsonify({'message': 'Accès refusé. Seuls les superadmins sont autorisés.'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def eu_required(f):
    """ Décorateur pour restreindre l'accès aux rôles : superadmin, admin et eu """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = get_user_role()

        if not user_role:
            return jsonify({'message': 'Accès refusé. Aucun utilisateur trouvé.'}), 403
        
        logging.info(f"User role: {user_role}")

        if user_role not in ['superadmin', 'admin', 'eu']:
            return jsonify({'message': 'Accès refusé. Seuls les utilisateurs avec le rôle superadmin, admin ou eu sont autorisés.'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
