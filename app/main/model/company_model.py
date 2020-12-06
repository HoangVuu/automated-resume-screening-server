from sqlalchemy.orm import backref
from .. import db, flask_bcrypt


class CompanyModel(db.Model):
    """ company Model for storing user related details """
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