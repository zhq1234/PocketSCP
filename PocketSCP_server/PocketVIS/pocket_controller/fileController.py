from flask import Blueprint, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from pocket_service import forcePlotService
from pocket_service.fileService import handleData

upload = Blueprint("upload", __name__)
CORS(upload, resource=r"/*")


@upload.route("/upload", methods=["GET","POST"])
def uploadFile():
    if request.method == 'POST':
        print(request.files)
        xtc = request.files['xtc']
        pdb = request.files['pdb']
        uuid_str = uuid.uuid4().hex
        os.mkdir('F:\\proj\\dataset\\test\\uploadFile\\'+uuid_str)
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        xtc.save(os.path.join('F:\\proj\\dataset\\test\\uploadFile\\'+uuid_str, xtc.filename))
        pdb.save(os.path.join('F:\\proj\\dataset\\test\\uploadFile\\' + uuid_str, pdb.filename))
        handleData(uuid_str,pdb.filename,xtc.filename)
        return uuid_str

@upload.route("/updateData", methods=["GET"])
def updateData():
    # request.get_data(as_text=True)
    return 'success'