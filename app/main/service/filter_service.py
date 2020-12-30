from sqlalchemy import or_, and_, not_, extract
from app.main.model.job_domain_model import JobDomainModel
from app.main.model.resume_model import ResumeModel
from app.main.model.candidate_model import CandidateModel
from app.main.util.response import response_object
from os import abort
from app.main.model.filter_candidates import FilterCandidateModel
from app.main.model.recruiter_model import RecruiterModel
from flask_jwt_extended.utils import get_jwt_identity
from app.main import db


def add_new_filter(data):
    identity = get_jwt_identity()
    email = identity['email']
    hr = RecruiterModel.query.filter_by(email=email).first()

    new_filter = FilterCandidateModel(
        name=data['name'],
        job_domains=data['job_domains'] or None,
        provinces=data['provinces'] or None,
        atleast_skills=data['atleast_skills'] or None,
        required_skills=data['required_skills'] or None,
        not_allowed_skills=data['not_allowed_skills'] or None
    )

    try:
        hr.fiter_candidates.append(new_filter)
        db.session.add(hr)
        db.session.commit()
    except:
        abort(400)


    return response_object(message="Tạo bộ lọc mới thành công", data=new_filter.id)


def get_filter_list(args):
    page = args.get('page')
    page_size = args.get('page-size')

    identity = get_jwt_identity()
    email = identity['email']

    result = FilterCandidateModel.query\
        .join(RecruiterModel, RecruiterModel.id == FilterCandidateModel.recruiter_id)\
        .filter(RecruiterModel.email == email)\
        .paginate(page, page_size, error_out=False)

    return result.items, {
        'total': result.total,
        'page': result.page
    }

def get_filter_detail(id):
    filter = FilterCandidateModel.query.get(id)

    if not filter:
        abort(400)

    return filter


def contain_skill(skills):
    res = []
    for skill in skills:
        res.append(ResumeModel.technical_skills.contains(skill))
        res.append(ResumeModel.soft_skills.contains(skill))
    return res

def not_contain_skill(skills):
    res = []
    for skill in skills:
        res.append(not_(ResumeModel.technical_skills.contains(skill)))
        res.append(not_(ResumeModel.soft_skills.contains(skill)))
    return res

def find_candidates(args):
    query = ResumeModel.query

    page = args.get('page')
    page_size = args.get('page_size')
    job_domains = args.get('job_domains')
    provinces = args.get('provinces')
    atleast_skills = args.get('atleast_skills')
    not_allowed_skills = args.get('not_allowed_skills')
    required_skills = args.get('required_skills')
    min_year = args.get('min_year')
    max_year = args.get('max_year')
    gender = args.get('gender')
    months_of_experience = args.get('months_of_experience')

    if job_domains:
        query = query.filter(ResumeModel.job_domain_id.in_(job_domains))

    if provinces:
        province_ids = [int(id) for id in provinces]

        query = query.join(CandidateModel, CandidateModel.id == ResumeModel.cand_id)\
            .filter(CandidateModel.province_id.in_(province_ids))

    if atleast_skills:
        query = query.filter(or_(*contain_skill(atleast_skills)))

    if required_skills:
        query = query.filter(and_(*contain_skill(required_skills)))

    if not_allowed_skills:
        query = query.filter(and_(*not_contain_skill(not_allowed_skills)))

    if min_year:
        query = query.join(CandidateModel, CandidateModel.id == ResumeModel.cand_id)\
            .filter(extract('year', CandidateModel.date_of_birth) >= min_year)

    if max_year:
        query = query.join(CandidateModel, CandidateModel.id == ResumeModel.cand_id)\
            .filter(extract('year', CandidateModel.date_of_birth) <= max_year)

    if gender:
        gender = gender == 'true'
        query = query.join(CandidateModel, CandidateModel.id == ResumeModel.cand_id)\
            .filter(CandidateModel.gender == gender)

    if months_of_experience:
        query = query.filter(ResumeModel.months_of_experience >= months_of_experience)

    result = query\
        .order_by(ResumeModel.id.desc())\
        .paginate(page=page, per_page=page_size)

    return result.items, {
        'total': result.total,
        'page': result.page
    }