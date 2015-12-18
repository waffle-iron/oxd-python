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
    if request.args.get('state'):
        state = request.args.get('state')
        code = request.args.get('code')
        scopes = request.args.get('scope').split(" ")
        token = oxc.get_tokens_by_code(code, scopes, state)
    else:
        token = oxc.get_tokens_by_code_by_url(request.url)
    user = oxc.get_user_info(token)

    return render_template("home.html", user=user)


@app.route('/logout')
def logout():
    html = oxc.logout(True)
    html = "Logout successfull Server returned html: %s" % (html,)
    return render_template("home.html", logout_html=html)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
