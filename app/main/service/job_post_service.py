from flask import json
from flask_restx.inputs import email
from app.main.util.response import response_object
import dateutil.parser
from app.main import db
from app.main.model.job_post_model import JobPostModel
from app.main.model.job_post_detail_model import JobPostDetailModel
from app.main.model.recruiter_model import RecruiterModel
from app.main.model.job_domain_model import JobDomainModel

def add_new_post(post):
    parse_deadline = dateutil.parser.isoparse(post['deadline'])

    recruiter = RecruiterModel.query.filter_by(email=post['recruiter_email']).first()
    job_domain = JobDomainModel.query.get(post['job_domain_id'])

    if (not recruiter) | (not job_domain):
        return "Error"

    job_post_detail = JobPostDetailModel(
        job_title=post['job_title'],
        contract_type=post['contract_type'],
        min_salary=post['min_salary'],
        max_salary=post['max_salary'],
        amount=post['amount'],
        deadline=parse_deadline
    )

    new_post = JobPostModel(
        job_domain_id=post['job_domain_id'],
        description_text=post['description_text'],
        requirement_text=post['requirement_text'],
        benefit_text=post['benefit_text'],
    )
    new_post.job_post_detail = job_post_detail

    recruiter.job_posts.append(new_post)
    job_domain.job_posts.append(new_post)

    db.session.add(recruiter)
    db.session.add(job_domain)
    db.session.add(new_post)
    db.session.commit()

    return response_object(code=200, message="Đăng tin tuyển dụng thành công", data=new_post.to_json()), 200