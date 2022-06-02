"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Artist, Project, ProjectVersion, FileID, Poll
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

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
            return jsonify({"msg": "Artist created successfully"}), 201
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
            return jsonify({"msg": "Error with the request data"}), 400

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
            return jsonify({"msg": "Project created successfully"}), 201
        except:
            return jsonify({"msg": "Error with the request data"}), 400
    # request of type GET
    elif request.method == 'GET':
        try:
            data = request.json
            # get the artist by username and password
            project = Project.query.filter_by(id=data["id"]).first()
            print(project)
            if not project:
                return jsonify({"msg": "Project with the id established does not exist"}), 400
            return jsonify({"project": project.serialize()}), 200
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
            return jsonify({"msg": "Project version created successfully"}), 201
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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
