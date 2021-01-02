import datetime
from app.main.service.account_service import create_token
from app.main import db
from app.main.model.recruiter_model import RecruiterModel
from app.main.model.resume_model import  ResumeModel
from app.main.model.recruiter_resume_save_model import  RecruiterResumeSavesModel
from flask_restx import abort

def get_a_account_recruiter_by_email(email):
    return RecruiterModel.query.filter_by(email=email).first()

def get_all_recruiter():
    return RecruiterModel.query.all()


def insert_new_account_recruiter(account):
    new_account = RecruiterModel(
        email=account['email'],
        password=account['password'],
        phone = account['phone'],
        full_name = account['fullName'],
        gender = account['gender'],
        access_token=create_token(account['email'], 1/24),
        registered_on=datetime.datetime.utcnow()
    )
    db.session.add(new_account)
    db.session.commit()


def delete_a_recruiter_by_id(id):
    return RecruiterModel.query.filter_by(id=id).first()

def get_a_recruiter_by_email(name):
    return RecruiterModel.query.filter_by(name=name).first()

def set_token_recruiter(email, token):
    account = get_a_recruiter_by_email(email)
    account.access_token = token
    db.session.add(account)
    db.session.commit()

def verify_account_recruiter(email):
    account = get_a_account_recruiter_by_email(email)
    account.confirmed = True
    account.confirmed_on = datetime.datetime.utcnow()
    db.session.add(account)
    db.session.commit()



def alter_save_resume(rec_email, args):
    res_id = args['resume_id']
    status = args['status']

    #Check HR
    rec = RecruiterModel.query.filter_by(email=rec_email).first()
    if rec is None: abort(400)
    rec_id = rec.id
    
    # Create 
    if status != 0:
        # Check existence.
        res = ResumeModel.query.get(res_id)
        if res is None: abort(400)

        existed = RecruiterResumeSavesModel.query\
            .filter_by(recruiter_id=rec_id, resume_id=res_id)\
            .first()
        if existed is None:
            existed = RecruiterResumeSavesModel(
                recruiter_id=rec.id,
                resume_id=res_id,
            )
            db.session.add(existed)
            db.session.commit()

        return {
            'id': existed.id,
            'recruiter_id': existed.recruiter_id,
            'resume_id': existed.resume_id
        }

    # Remove
    if status == 0:
        # Check existence.
        remove = RecruiterResumeSavesModel.query\
            .filter_by(recruiter_id=rec_id, resume_id=res_id)\
            .first()
        if remove is None: abort(400)

        db.session.delete(remove)
        db.session.commit()

        return {
            'id': remove.id,
            'recruiter_id': remove.recruiter_id,
            'resume_id': remove.resume_id
        }
