
from sqlalchemy.orm import backref
from .. import db, flask_bcrypt


class CompanyModel(db.Model):
    """ company Model for storing account related details """
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(180))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    website = db.Column(db.String(255))
    description = db.Column(db.String(255))

    recruiter = db.relationship('RecruiterModel', backref=backref("company", uselist=False),uselist=False)

    def __init__(self, name, location, phone, email, logo, website,description):
        self.name = name
        self.location = location
        self.phone = phone
        self.email = email
        self.logo = logo
        self.website = website
        self.description = description

    def __repr__(self):
        return "<User '{}'>".format(self.name)

    def to_json(self):
        return {
            "id": int(self.id),
            "name": self.name,
            "location": self.location,
            "phone": self.phone,
            "email": self.email,
            "logo": self.logo,
            "website": self.website,
            "description": self.description,
        }
