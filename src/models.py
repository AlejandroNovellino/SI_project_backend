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
        self.email = kwargs.get('email')
        #self.set_password(kwargs.get('password'))
        self.password = kwargs["password"]
        self.username = kwargs["username"]

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Artist(db.Model):
    __tablename__ = 'artist'
    # way to define inheritance
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # data
    first_name = db.Column(db.String(80), unique=False, nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=True)
    age = db.Column(db.SmallInteger, unique=False, nullable=True)
    nationality = db.Column(db.String(40), unique=False, nullable=True)
    bio = db.Column(db.Text, unique=False, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity':'artist'
    }


    def __init__(self, **kwargs):
        super().__init__(
            email=kwargs["email"],
            password=kwargs["password"],
            username=kwargs["username"],
        )
        self.first_name=kwargs["first_name"],
        self.last_name=kwargs["last_name"],
        self.age=kwargs["age"],
        self.nationality=kwargs["nationality"],
        self.bio=kwargs["bio"],

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            **super.serialize(),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "nationality": self.nationality,
            "bio": self.nationality
        }
