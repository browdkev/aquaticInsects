import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#@bp.route('/')
#def upload_form():
#    return render_template('photo/upload.html')


@bp.route('/', methods=('GET', 'POST'))
def upload_form():
    if request.method == 'POST':
        db = get_db()

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        #TODO Change to db upload
        for file in files:
            if file and allowed_file(file.filename):
                temp = file.read()
                db.execute(
                    'INSERT INTO img (author_id, photo)'
                    ' VALUES (?, ?)',
                    (g.user['id'], temp)
                )
                db.commit()
                
        flash('File(s) successfully uploaded')
    return render_template('photo/upload.html')