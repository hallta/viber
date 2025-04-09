"""
Utility decorators for the Viber application.
"""

from functools import wraps
from typing import Callable, Any
from flask import session, redirect, url_for, request

def login_required(f: Callable) -> Callable:
    """
    Decorator to require login for routes.
    
    Args:
        f: The route function to wrap
    
    Returns:
        Callable: The wrapped function
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'authenticated' not in session:
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function 