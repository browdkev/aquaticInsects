import os,sys

from flask import Flask

# create and configure the app
app = Flask('AquaticInsects', instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

print("CONFIG",app.config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

import flaskr.db as db
db.init_app(app)

import flaskr.auth as auth
app.register_blueprint(auth.bp)

import flaskr.photo as photo
app.register_blueprint(photo.bp)
app.add_url_rule('/', endpoint='upload_form')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
