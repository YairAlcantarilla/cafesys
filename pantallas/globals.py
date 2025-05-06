# Global variables to be used across the application
current_user = "Usuario del sistema"

def set_current_user(username):
    """Set the current logged-in user"""
    global current_user
    current_user = username

def get_current_user():
    """Get the current logged-in user"""
    return current_user