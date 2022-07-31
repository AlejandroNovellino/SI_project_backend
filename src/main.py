"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, uuid
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Artist, Project, ProjectVersion, FileID, Poll, Comment
#from models import Person

# information for the files
#UPLOAD_FOLDER = 'F:\\Projects\\SI_project_backend\\src\\\saved_uploads'
UPLOAD_FOLDER = 'saved_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# verify id the file is from an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/artist', methods=['GET', 'POST'])
def artist():
    '''
        POST: create the artist based on the info give it
        GET: get the artist based on the username and password combination
    '''
    # request of type POST
    if request.method == 'POST':
        try:
            data = request.json
            # create the user
            artist = Artist.create(**data)
            if not isinstance(artist, Artist):
                return jsonify({"msg": "Artist could not be created"}), 500
            return jsonify({"artist": artist.serialize()}), 201
        except:
            return jsonify({"msg": "Error with the request data"}), 400
    # request of type GET
    elif request.method == 'GET':
        try:
            data = request.json
            # get the artist by username and password
            artist = Artist.query.filter_by(username=data["username"], password=data["password"]).first()
            if not artist:
                return jsonify({"msg": "Combination is not valid"}), 400
            return jsonify({"artist": artist.serialize()}), 200
        except:
            return jsonify({"msg": "Error with the request data"}), 404

@app.route('/artist/log-in', methods=['POST'])
def artistGet():
    '''
        POST: get the artist based on the username and password combination
    '''
    # request of type POST
    if request.method == 'POST':
        try:
            data = request.json
            # get the artist by username and password
            artist = Artist.query.filter_by(username=data["username"], password=data["password"]).first()
            if not artist:
                return jsonify({"msg": "Combination is not valid"}), 404
            return jsonify({"artist": artist.serialize()}), 200
        except:
            return jsonify({"msg": "Error"}), 500

@app.route('/project', methods=['GET', 'POST'])
def project():
    '''
        POST: create the project based on the artist id and project info
        GET: get the project based on the id
    '''
    # request of type POST
    if request.method == 'POST':
        try:
            data = request.json
            # create the user
            project = Project.create(**data)
            if not isinstance(project, Project):
                return jsonify({"msg": "Project could not be created"}), 500
            artist = Artist.query.filter_by(id=data["artist_id"]).first()
            return jsonify({"artist": artist.serialize()}), 201
        except:
            return jsonify({"msg": "Error with the request data"}), 400
    # request of type GET
    elif request.method == 'GET':
        try:
            data = request.json
            # get the artist by username and password
            project = Project.query.filter_by(id=data["id"]).first()
            if not project:
                return jsonify({"msg": "Project with the id established does not exist"}), 400
            return jsonify({"project": project.serialize()}), 200
        except:
            return jsonify({"msg": "Error with the request data"}), 400

@app.route('/projects', methods=['GET'])
def projects():
    '''
        GET: get all the projects
    '''
    # request of type GET
    if request.method == 'GET':
        try:
            # get all the projects
            projects = Project.query.all()
            if not project:
                return jsonify({"msg": "Cannot get all the projects"}), 400
            return jsonify({"projects": [project.serialize() for project in projects]}), 200
        except:
            return jsonify({"msg": "Error with the request data"}), 400

@app.route('/project-version', methods=['GET', 'POST'])
def project_version():
    '''
        POST: create the project version based on the project id and project version info
        GET: get the project version based on the id
    '''
    # request of type POST
    if request.method == 'POST':
        try:
            data = request.json
            # create the user
            project_version = ProjectVersion.create(**data)
            if not isinstance(project_version, ProjectVersion):
                return jsonify({"msg": "Project version could not be created"}), 500

            artist = Artist.query.filter_by(id=data["artist_id"]).first()
            return jsonify({"artist": artist.serialize()}), 201
        except:
            return jsonify({"msg": "Error with the request data"}), 400
    # request of type GET
    elif request.method == 'GET':
        try:
            data = request.json
            # get the artist by username and password
            project_version = ProjectVersion.query.filter_by(id=data["id"]).first()
            if not project_version:
                return jsonify({"msg": "Project version with the id established does not exist"}), 400
            return jsonify({"project_version": project_version.serialize()}), 200
        except:
            return jsonify({"msg": "Error with the request data"}), 400

@app.route('/poll', methods=['GET', 'POST', 'PUT'])
def poll():
    '''
        POST: create the poll based on the artist id and info
        GET: get the poll based on the id
        PUT: update a product
    '''
    # request of type POST
    if request.method == 'POST':
        try:
            data = request.json
            # create the user
            poll = Poll.create(**data)
            if not isinstance(poll, Poll):
                return jsonify({"msg": "Poll could not be created"}), 500
            artist = Artist.query.filter_by(id=data["artist_id"]).first()
            return jsonify({"artist": artist.serialize()}), 201
        except:
            return jsonify({"msg": "Error with the request data"}), 400
    # request of type GET
    elif request.method == 'GET':
        try:
            data = request.json
            # get the artist by username and password
            poll = Poll.query.filter_by(id=data["id"]).first()
            if not poll:
                return jsonify({"msg": "Poll with the id established does not exist"}), 400
            return jsonify({"poll": poll.serialize()}), 200
        except:
            return jsonify({"msg": "Error with the request data"}), 400
    # request of type PUT
    elif request.method == 'PUT':
        try:
            data = request.json
            print(data)
            poll = Poll.query.get(data["id"])

            # update the poll
            poll.info = data["info"]

            db.session.commit()

            return jsonify({"msg": "Poll updated successfully"}), 202
        except BaseException as e:
            print(e)
            return jsonify({"msg": "Error with the request data"}), 400

@app.route('/comment', methods=['POST'])
def comment():
    '''
        POST: create a comment
    '''
    # request of type POST
    if request.method == 'POST':
        try:
            data = request.json
            # create the comment
            comment = Comment.create(**data)
            if not isinstance(comment, Comment):
                return jsonify({"msg": "Comment could not be created"}), 500
            artist = Artist.query.filter_by(id=data["artist_id"]).first()
            return jsonify({"artist": artist.serialize()}), 201
        except:
            return jsonify({"msg": "Error with the request data"}), 400

@app.route('/file', methods=['POST'])
def file_endpoint():
    '''
        POST: save the file based on the project id and the 
    '''
    # request of type POST
    if request.method == 'POST':
        try:
            print(request.json)
            print(request.files)
            # check if the post request has the file part
            if 'file' not in request.files:
                return jsonify({"msg": "No file passed"}), 400
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return jsonify({"msg": "Empty file passed"}), 400
            if file and allowed_file(file.filename):
                # create the fileId object
                data = request.form.copy()
                # save the filename and the unique id
                data["filename"] = file.filename
                # create the user
                file_id = FileID.create(**data)
                if not isinstance(file_id, FileID):
                    return jsonify({"msg": "File could not be saved"}), 500
                # if the object is created the file can be saved
                filename = secure_filename(file.filename)
                path_for_upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(path_for_upload_folder, filename))
                
                artist = Artist.query.filter_by(id=data["artist_id"]).first()
                return jsonify({"artist": artist.serialize()}), 201
        except BaseException as err:
            print(err)
            return jsonify({"msg": "Error with the request data"}), 400

@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    path_for_upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(
        path_for_upload_folder, filename
    )

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5040))
    app.run(host='0.0.0.0', port=PORT, debug=False)
