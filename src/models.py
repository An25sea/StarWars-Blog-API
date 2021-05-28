from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
# do not serialize the password, its a security breach
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    color_eyes = db.Column(db.String(250), nullable=False)
    color_hair = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    birth = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    color_skin = db.Column(db.String(250), nullable=False)

    

    def __repr__(self):
        return '<name %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "color_eyes": self.color_eyes,
            "color_hair": self.color_hair,
            "gender": self.gender,
            "birth": self.birth,
            "height": self.height,
            "color_skin": self.color_skin,
# do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250))
    rotation = db.Column(db.String(250))
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    orbital=db.Column(db.String(250), nullable=False)
    gravity=db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<name %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation": self.rotation,
            "population": self.population,
            "terrain": self.terrain,
            "orbital": self.orbital,
            "gravity": self.gravity,
# do not serialize the password, its a security breach
        }
#example_table = Table('example', Base.metadata,
#Column("user_id", Integer, ForeignKey("User.id")),
#Column("brother_id", Integer, ForeignKey("Brother.id"))
#)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship("Planet")
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship("Person")
    

    def __repr__(self):
        return '<id %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "person_id": self.person_id,
           
            # do not serialize the password, its a security breach
        }