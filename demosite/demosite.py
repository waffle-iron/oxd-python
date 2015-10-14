import os
import sys
from flask import Flask, render_template, redirect, request

this_dir = os.path.dirname(os.path.realpath(__file__))
config = os.path.join(this_dir, 'demosite.cfg')

oxd_path = os.path.dirname(this_dir)
if oxd_path not in sys.path:
    sys.path.insert(0, oxd_path)

import oxdpython

app = Flask(__name__)
oxc = oxdpython.Client(config)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/authorize/')
def authorize():
    """The endpoint which is to be accessed but the user in order to start the
    authorization by the user"""

    auth_url = oxc.get_authorization_url()
    return redirect(auth_url)


@app.route('/callback')
def callabck():
    state = request.args.get('state')
    code = request.args.get('code')
    scopes = request.args.get('scope').split(" ")
    print "\n\ncalling get_tokens_by_code({0}, {1}, {2})".format(code, scopes, state)
    token = oxc.get_tokens_by_code(code, scopes, state)
    print "\n\nrecieved token: {0}".format(token)
    print "\n\ncalling get_user_info({})".format(token)
    user = oxc.get_user_info(token)
    print "\n\nrecived user: {}".format(user)

    return "User Name: {}".format(user.name)

if __name__ == "__main__":
    app.run(debug=True)
