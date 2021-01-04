from app.main.util.custom_fields import NullableFloat
from flask_restx import Namespace, fields, Model
from app.main.dto.base_dto import base
from app.main.util.format_text import format_contract, format_salary
from app.main.dto.resume_dto import ResumeDTO

class JobPostDto:
    api = Namespace('Job Posts', description='job post related operation')

    job_post = api.model('job_post', {
        'recruiter_email': fields.String(required=True, description='email of hr who post this job'),
        'job_domain_id': fields.Integer(required=True, description='id domain of this post'),
        'description_text': fields.String(required=True, description='job description'),
        'requirement_text': fields.String(required=True, description='job requirement'),
        'benefit_text': fields.String(required=True, description='benefit for candidate'),
        'job_title': fields.String(required=True, description='job title'),
        'contract_type': fields.Integer(required=True, description='type of contract'),
        'min_salary': NullableFloat(required=False, description='minimum salary'),
        'max_salary': NullableFloat(required=False, description='maximum salary'),
        'amount': fields.Integer(required=True, description='amount of candidates is recruiting'),
        'education_level': fields.Integer(required=True, description='education_level of candidates is recruiting'),
        'majors': fields.String(required=True, description='majors of candidates is recruiting'),
        'province_id': fields.String(required=True, description='locations of candidates is recruiting'),
        'deadline': fields.DateTime(required=True, description='last day for candidate to apply'),
    })

    job_list = api.model('job_list', {
        'id': fields.Integer(description='id of job post'),
        'job_title': fields.String(description='job title'),
        'salary': fields.String(description='salary for candidate'),
        'posted_in': fields.DateTime(description='when did this post?'),
        'deadline': fields.DateTime(description='last day for candidate to apply'),
        'total_apply': fields.Integer(description='nums of candidate who applied this post'),
        'new_apply': fields.Integer(description='nums of candidate who applied this post recently'),
        'total_view': fields.Integer(description='nums of candidate who viewed this post'),
    })



    # Response job post for cand
    job_post_for_cand_fields = api.model("job_post_for_cand_fields", {
        'id': fields.Integer, 
        'job_title': fields.String, 
        'job_domain': fields.String(attribute='job_domain.name'),
        'salary': fields.String(attribute=lambda x: format_salary(x.min_salary, x.max_salary)), 
        'posted_in': fields.DateTime(),
        'deadline': fields.DateTime,
        'contract_type': fields.String(attribute=lambda x: format_contract(x.contract_type)),
        'description': fields.String(attribute='description_text'),
        'requirement': fields.String(attribute='requirement_text'),
        'benefit': fields.String(attribute='benefit_text'),
        'amount': fields.Integer,
        'company_name': fields.String(attribute=lambda x: x.recruiter.company.name if x.recruiter.company is not None else None),
        'company_logo': fields.String(attribute=lambda x: x.recruiter.company.logo if x.recruiter.company is not None else None),
        'company_background': fields.String(attribute=lambda x: x.recruiter.company.background if x.recruiter.company is not None else None),
        # 'total_view': fields. post.total_views,
        # 'total_save': fields. post.total_views,
        # 'total_apply': fields. post.total_applies,
    })
    job_post_for_cand = api.inherit('job_post_for_cand', base, {
        'data': fields.Nested(job_post_for_cand_fields)
    })



    # Response for search job post
    single_job_post_in_search_fields = api.model("single_job_post_in_search_fields", {
        'job_title': fields.String,
        'company_name': fields.String(attribute=lambda x: x.recruiter.company.name if x.recruiter.company is not None else None),
        'last_edit': fields.DateTime(),
        'salary': fields.String(attribute=lambda x: format_salary(x.min_salary, x.max_salary)),
        'contact_type': fields.String(attribute=lambda x: format_contract(x.contract_type)),
        'province_id': fields.String,
        'job_post_id': fields.Integer(attribute=lambda x: x.id),
        'job_description': fields.String(attribute=lambda x: x.description_text),
    })
    pagination = api.model('pagination', {
        'page': fields.Integer,
        'total': fields.Integer,
    })
    job_post_in_search_cand_response = api.inherit('job_post_in_search_cand_response', base, {
        'data': fields.List(fields.Nested(single_job_post_in_search_fields)),
        'pagination': fields.Nested(pagination)
    })


    #Response for update job post from HR
    response_for_update_job_post_from_hr_fields = api.model("response_for_update_job_post_from_hr_fields", {
        'id': fields.Integer,
        'job_title': fields.String, 
        'job_domain': fields.String(attribute="job_domain.name"),
        'salary': fields.String(attribute=lambda x: format_salary(x.min_salary, x.max_salary)), 
        'posted_in': fields.DateTime(),
        'deadline': fields.DateTime(),
        'last_edit': fields.DateTime(),
        'contract_type': fields.String(attribute=lambda x: format_contract(x.contract_type)),
        'amount': fields.Integer,
        'description': fields.String(attribute='description_text'),
        'requirement': fields.String(attribute='requirement_text'),
        'benefit': fields.String(attribute='benefit_text'),
        'total_views': fields.Integer,
        'total_saves': fields.Integer,
        'total_applies': fields.Integer
    })
    response_for_update_job_post_from_hr = api.inherit('response_for_update_job_post_from_HR', base, {
        'data': fields.List(fields.Nested(single_job_post_in_search_fields)),
    })


    ########################################
    # Get matched cand info with job post
    ########################################
    candidate_detail_fields = api.model('candidate_detail_fields', {
        'id': fields.Integer,
        'email': fields.String,
        'password_hash': fields.String,
        'phone': fields.String,
        'full_name': fields.String,
        'gender': fields.Boolean,
        'date_of_birth': fields.DateTime(),
        'status': fields.Integer,
        'province_id': fields.Integer,
        'access_token': fields.String,
        'registered_on': fields.DateTime(),
        'confirmed': fields.Boolean,
        'confirmed_on': fields.DateTime()
    })
    submission_fields = api.model('submission_fields', {
        'id': fields.Integer,
        'resume_id': fields.Integer,
        'job_post_id': fields.Integer,
        'submit_date': fields.DateTime(),
        'score': fields.Float,
        'process_status': fields.Boolean,
        'score_array': fields.String,
        'score_explanation_array': fields.String
    })
    submission_cand_info_fields = api.model('submission_cand_info_fields', {
        'submission': fields.Nested(submission_fields),
        'candidate': fields.Nested(candidate_detail_fields),
        'resume': fields.Nested(ResumeDTO.resume_detail_fields),
        'scores': fields.Raw
    })
    get_cand_info_with_matched_job_post_response = api.inherit('get_cand_info_with_matched_job_post_response', base, {
        'data': fields.Nested(submission_cand_info_fields)
    })


    ###############################
    # Get list applied candidates
    ###############################
    applied_cand_fields = api.model('applied_cand_fields', {
        'submission': fields.Nested(submission_fields),
        'candidate': fields.Nested(candidate_detail_fields),
        'scores': fields.Raw
    })
    applied_cand_list_response = api.inherit('applied_cand_list_response', base, {
        'data': fields.List(fields.Nested(applied_cand_fields)),
        'pagination': fields.Nested(pagination)
    })