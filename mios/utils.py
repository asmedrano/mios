from flask import session, escape

def get_user_session():
    if 'e' in session:
        user = escape(session['e'])
    else:
        user = False
    return user
