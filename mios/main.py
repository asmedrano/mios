from flask import Flask, render_template, request, abort, session, escape

import simplejson as json
import requests
import utils
app = Flask(__name__)
app.config.from_object('settings')

@app.route("/")
def index():
    user = utils.get_user_session()
    return render_template("index.html", user=user)

@app.route("/")
def browser():
    return "Browser"



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
