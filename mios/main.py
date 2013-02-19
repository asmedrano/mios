import os
from flask import Flask, render_template, request, abort, session, escape, \
        redirect, g, abort, url_for
import simplejson as json
import requests
import utils
from bson.objectid import ObjectId
from data import *
app = Flask(__name__)
app.config.from_object('settings')

@app.before_request
def before_request():
    g.img_manager = ImageManager('test-db')

@app.teardown_request
def teardown_request(exception):
    g.img_manager.close_conn()

@app.route("/")
def index():
    user = utils.get_user_session()
    return render_template("index.html", user=user)

@app.route("/browse")
def browser():
    user = utils.get_user_session()
    if user is not False:
        imgs = g.img_manager.find()
    else:
        imgs = g.img_manager.find({'published':True}) # grab all the published images
    return render_template("browse.html", user=user, images=imgs)

@app.route("/actions/upload", methods=["POST"])
def upload():
    """ Recieves a list of images to upload """
    if request.method == 'POST':
        for file in request.files.getlist('images'):
            utils.put_file(file, g.img_manager, app)
    return redirect(url_for('browser'))

@app.route("/actions/update", methods=["POST"])
def update():
    if request.method == 'POST':
        u_query = {}
        u_vals = {} # the values to update
        if 'i_id' in request.form:
            u_query['_id'] = ObjectId(request.form['i_id'])

        if 'delete' not in request.form:
            # the update values
            if 'description' in request.form:
                u_vals['description'] = request.form['description']
            if 'tags' in request.form:
                tags = [tag.strip() for tag in request.form['tags'].split(',')]
                u_vals['tags'] = tags
            if 'published' in request.form:
                pval = request.form['published']
                if pval == 'on':
                    u_vals['published'] = True
            else:
                u_vals['published'] = False
            # do the update
            res = g.img_manager.update(u_query, **u_vals)
        else:
            # user is trying to remove image
            if request.form['delete'] == 'on':
                img = g.img_manager.find_one(u_query)
                if img:
                    utils.remove_img_from_fs(img, app)
                    g.img_manager.remove(img)

        # finally return redirect or json response if is_xhr
        if request.is_xhr:
            return json.dumps({'status':'ok'})

        return redirect(url_for('browser'))

@app.route("/auth/login", methods=['POST'])
def login():
    # The request has to have an assertion for us to verify
    if 'assertion' not in request.form:
        abort(400)
    # Send the assertion to Mozilla's verifier service.
    data = {'assertion': request.form['assertion'], 'audience': 'http://127.0.0.1:5000'}
    resp = requests.post('https://verifier.login.persona.org/verify', data=data, verify=True)
    # Did the verifier respond?
    if resp.ok:
        # Parse the response
        verification_data = json.loads(resp.content)
        # Check if the assertion was valid
        if verification_data['status'] == 'okay':
            # Log the user in by setting a secure session cookie
            session.update({'e': verification_data['email']})
            return resp.content
    # Oops, something failed. Abort.
    abort(500)

@app.route("/auth/logout", methods=['POST'])
def logout():
    session.pop('e', None)
    return json.dumps({'a':'logout'})




if __name__ == "__main__":
    app.run()
