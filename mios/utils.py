from flask import session, escape
from werkzeug import secure_filename
import os
from data import *

def get_user_session():
    if 'e' in session:
        user = escape(session['e'])
    else:
        user = False
    return user

def allowed_file(filename, allowed):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed

def put_file(file, img_manager, app):
    """ Save file data to db and filesystem """
    if allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        img = Image(name=filename)
        i_id = str(img_manager.insert([img])[0])
        fname, ftype = filename.rsplit(".")
        filename = fname + "_"+ i_id + "." + ftype
        file.save(os.path.join(app.config['UPLOAD_DIRECTORY'], filename))

def remove_img_from_fs(img, app):
    """ remove the img for the os or eventuall S3 or something like that """
    targ_dir = app.config['UPLOAD_DIRECTORY']
    path = os.path.join(targ_dir, img.get_file_name())
    os.remove(path)
