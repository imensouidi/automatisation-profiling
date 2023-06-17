from functools import wraps 
from flask import abort, jsonify, request
import logging

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the user role from the request headers or session
        # Adjust this code according to how you store and retrieve user roles
        user_role = request.headers.get('User-Role')
        
        # Logging the user role
        logging.info(f"User role: {user_role}")

        # Check if the user has the "admin" or "superadmin" role
        if user_role not in ['admin', 'superadmin']:
            return jsonify({'message': 'Access denied. Only admin and superadmin roles are allowed.'}), 403
        return f(*args, **kwargs)

    return decorated_function


def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the user role from the request headers or session
        # Adjust this code according to how you store and retrieve user roles
        user_role = request.headers.get('User-Role')
        
        # Logging the user role
        logging.info(f"User role: {user_role}")

        # Check if the user has the "superadmin" role
        if user_role not in ['superadmin']:
            return jsonify({'message': 'Access denied. Only superadmin roles are allowed.'}), 403
        return f(*args, **kwargs)

    return decorated_function



def eu_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the user role from the request headers or session
        # Adjust this code according to how you store and retrieve user roles
        user_role = request.headers.get('User-Role')
        
        # Logging the user role
        logging.info(f"User role: {user_role}")

        # Check if the user has the "superadmin","admin" ,"eu" role
        if user_role not in ['superadmin','admin','eu']:
            return jsonify({'message': 'Access denied. Only eu roles are allowed.'}), 403
        return f(*args, **kwargs)

    return decorated_function