from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    # data
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    # camp necessary for inheritance
    type = db.Column(db.String(40))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

    def __init__(self, **kwargs):
        self.email = kwargs['email']
        #self.set_password(kwargs['password'])
        self.password = kwargs["password"]
        self.username = kwargs["username"]

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Artist(User, db.Model):
    __tablename__ = 'artist'
    # way to define inheritance
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # data
    first_name = db.Column(db.String(80), unique=False, nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=True)
    age = db.Column(db.SmallInteger, unique=False, nullable=True)
    nationality = db.Column(db.String(40), unique=False, nullable=True)
    bio = db.Column(db.Text, unique=False, nullable=True)
    # one to many relationships
        # list of projects
    projects = db.relationship('Project', backref='project')

    __mapper_args__ = {
        'polymorphic_identity':'artist'
    }

    def __init__(self, **kwargs):
        super().__init__(
            email=kwargs["email"],
            password=kwargs["password"],
            username=kwargs["username"],
        )
        if "first_name" in kwargs:
            self.first_name=kwargs["first_name"]
        if "last_name" in kwargs:
            self.last_name=kwargs["last_name"]
        if "age" in kwargs:
            self.age=kwargs["age"]
        if "nationality" in kwargs:
            self.nationality=kwargs["nationality"]
        if "bio" in kwargs:
            self.bio=kwargs["bio"]
    
    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return element

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return_dict = {
            **super().serialize(),
            "firstName": self.first_name,
            "lastName": self.last_name,
            "age": self.age,
            "nationality": self.nationality,
            "bio": self.nationality
        }

        if self.projects:
            return_dict["projects"] = list(map(lambda project: project.serialize(), self.projects))

        return return_dict

class Project(db.Model):
    __tablename__ = 'project'
    # data
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.Text, unique=False, nullable=False)
    header = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
        # foreign key to artist
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    # one to many relationships
        # list of ids to the files
    files = db.relationship('FileID', backref='project')
        # list of versions
    versions = db.relationship('ProjectVersion', backref='project')
        #list of polls
    polls = db.relationship('Poll', backref='project')

    def __init__(self, **kwargs):
        self.tittle = kwargs['tittle']
        self.header = kwargs["header"]
        self.description = kwargs["description"]
        self.artist_id = kwargs["artist_id"]

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return element

    def serialize(self):
        return_dict = {
            "id": self.id,
            "artist_id": self.artist_id,
            "tittle": self.tittle,
            "header": self.header,
            "description": self.description 
        }

        if self.versions:
            return_dict["versions"] = list(map(lambda version: version.serialize(), self.versions))

        if self.polls:
            return_dict["polls"] = list(map(lambda poll: poll.serialize(), self.polls))

        return return_dict

class ProjectVersion(db.Model):
    __tablename__ = 'projectVersion'
    # data
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.Text, unique=False, nullable=False)
    header = db.Column(db.Text, unique=False, nullable=True)
    description = db.Column(db.Text, unique=False, nullable=True)
        # foreign key to project
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    # one to many relationships
        # list of id to the files
    files = db.relationship('FileID', backref='projectVersion')

    def __init__(self, **kwargs):
        self.tittle = kwargs['tittle']
        self.header = kwargs["header"]
        self.description = kwargs["description"]
        self.project_id = kwargs["project_id"]

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return element

    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "tittle": self.tittle,
            "header": self.header,
            "description": self.description 
        }

class Poll(db.Model):
    __tablename__ = 'poll'
    # data
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.JSON)
        # foreign key to project
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    # info struct
    #info = {
    #   "question": 'Is react-polls useful?', 
    #   "pollAnswers": [
    #       {option: 'Yes', votes: 8},
    #       {option: 'No', votes: 10}
    #   ]
    #}
    #
    #

    def __init__(self, **kwargs):
        self.info = kwargs['info']
        self.project_id = kwargs['project_id']

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return element
    
    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            **self.info,
        }

class FileID(db.Model):
    __tablename__ = 'fileID'
    # data
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
        # foreign key to project
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
        # foreign key to project version
    project_version_id = db.Column(db.Integer, db.ForeignKey('projectVersion.id'))

    def __init__(self, **kwargs):
        self.filename = kwargs["filename"]
        self.project_id = kwargs.get('project_id')
        self.project_version_id = kwargs.get('project_version_id')

    @classmethod
    def create(cls, **kwargs):
        element = cls(**kwargs)
        db.session.add(element)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return element

    def serialize(self):
        return_dict = {
            "id": self.id,
            "filename": self.filename
        }

        if self.project_id:
            return_dict["project_id"] = id.project_id
        if self.project_version_id:
            return_dict["project_version_id"] = self.project_version_id

        return return_dict
