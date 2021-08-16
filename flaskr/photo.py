import os
import datetime as dt
import pprint as pp

from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for )
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from azure.storage.blob import BlobServiceClient,ContentSettings
blob_connect = os.environ['AzureWebJobsStorage']
blob_service_client = BlobServiceClient.from_connection_string(blob_connect)


from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_storage(file):
    container='data-ingress-api-upload'
    source='aquatic-insects'
    username=secure_filename(g.user["username"])

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        content_settings = ContentSettings(content_type=file.content_type)
        file.save(filename)
        blobspec="%s/%s/%s" % (source,username,filename)
        blob_client = blob_service_client.get_blob_client(container = container, blob = blobspec)
        with open(filename, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)
            print("Upload Done for:",blobspec)

def image_classification(file):
    results = {
        "username": secure_filename(g.user["username"]),
        "filename" : secure_filename(file.filename),
        "collection_time" : dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "insects" : [
            {"name": "Stonefly","count":3},
            {"name": "Mayfly","count":2}
        ]
    }

    return results

def post_results(results):
    pp.pprint(results)


@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for file in files:
            upload_file_to_storage(file)
            results=image_classification(file)
            post_results(results)
            os.remove(secure_filename(file.filename))


        flash('File(s) successfully uploaded')
    return render_template('photo/upload.html')

@bp.route('/index')
def index():
    db = get_db()
    photos = db.execute(
        'SELECT photo'
        ' FROM img i JOIN user u ON i.author_id = u.id'
    ).fetchall()
    
    
    return render_template('photo/index.html', photos=photos)

