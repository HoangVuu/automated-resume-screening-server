from datetime import datetime

from flask.wrappers import Response
from app.main.util.response import response_object
from app.main.util.custom_jwt import Candidate_only, HR_only
from flask_jwt_extended.utils import get_jwt_identity
from flask import request

from ..dto.job_post_dto import JobPostDto
from flask_restx import Resource
from ..service.job_post_service import add_new_post, count_jobs, \
        delete_job_post, get_hr_posts, hr_get_detail, apply_cv_to_jp,\
        get_job_post_for_candidate, search_jd_for_cand, \
        update_jp, close_jp, proceed_resume


from app.main.config import Config as config

api = JobPostDto.api
_job_post = JobPostDto.job_post



#################################
#
# Job Posts: GET, PUT, DELETE
#
#################################
delete_parser = api.parser()
delete_parser.add_argument("ids", type=int, action="split", location="args", required=True)
@api.route('')
class JobPost(Resource):
    @api.doc('add a new job post')
    @api.expect(_job_post, validate=True)
    @HR_only
    def post(self):
        data = request.json
        return add_new_post(data)

    @api.doc('get list of job post')
    def get(self):
        is_hr = request.args.get('is_hr') == 'true'

        page = request.args.get('page', config.DEFAULT_PAGE, type=int)
        page_size = request.args.get('page-size', config.DEFAULT_PAGE_SIZE, type=int)
        posted_in = request.args.get('posted_in', 0, type=int)
        deadline = request.args.get('deadline', 0, type=int)
        view = request.args.get('view', 0, type=int)
        apply = request.args.get('apply', 0, type=int)
        save = request.args.get('save', 0, type=int)

        is_showing = request.args.get('is_showing') == 'true'

        sort_values = { 'posted_in': posted_in, 'deadline': deadline, 'view': view, 'apply': apply, 'save': save }

        if is_hr:
            return get_hr_posts(page, page_size, sort_values, is_showing)
        
        api.abort(400)

    

    @api.doc('delete job list with given id')
    @api.expect(delete_parser)
    @HR_only
    def delete(self):
        args = delete_parser.parse_args()
        ids = args['ids']
        return delete_job_post(ids)




@api.route('/count')
class JobPostCount(Resource):
    @api.doc('get count of job post is closed or not')
    @HR_only
    def get(self):
        return count_jobs()



#################################
#
# Job Post Detail: GET, PUT
#
#################################
update_JP_parser = api.parser()
update_JP_parser.add_argument("job_domain_id", type=int, location="json")
update_JP_parser.add_argument("description_text", location="json")
update_JP_parser.add_argument("requirement_text", location="json")
update_JP_parser.add_argument("benefit_text", location="json")
update_JP_parser.add_argument("job_title", location="json")
update_JP_parser.add_argument("contract_type", type=int, location="json")
update_JP_parser.add_argument("min_salary", type=float, location="json")
update_JP_parser.add_argument("max_salary", type=float, location="json")
update_JP_parser.add_argument("amount", type=int, location="json")
update_JP_parser.add_argument("is_active", type=bool, location="json")
update_JP_parser.add_argument("deadline", type=datetime, location="json")
update_JP_parser.add_argument("province_id", type=int, location="json")
@api.route('/<int:id>')
class JobPostDetail(Resource):
    @api.doc('get detail of job post')
    def get(self, id):
        is_hr = request.args.get('is_hr') == 'true'

        if is_hr:
            return hr_get_detail(id)

    @api.doc('Update job post details.')
    @api.marshal_with(JobPostDto.response_for_update_job_post_from_hr, code=200)
    @HR_only
    def put(self, id):
        args = update_JP_parser.parse_args()
        identity = get_jwt_identity()
        recruiter_email = identity['email']
        data = update_jp(id, recruiter_email, args)
        return response_object(data=data)



#################################
#
# Close Job Post
#
#################################
@api.route('/<int:id>/close')
class CloseJobPost(Resource):
    @api.doc('Update job post details.')
    @api.marshal_with(JobPostDto.response_for_update_job_post_from_hr, code=200)
    @HR_only
    def post(self, id):
        identity = get_jwt_identity()
        recruiter_email = identity['email']
        data = close_jp(id, recruiter_email)
        return response_object(data=data)



#################################
#
# Apply CV
#
#################################
@api.route('/<int:jp_id>/apply')
class SubmitResumeForJD(Resource):
    apply_parser = api.parser()
    apply_parser.add_argument("resume_id", type=int, location="json", required=True)
    apply_parser.add_argument("Authorization", location="headers", required=True)
    @api.doc('Submit CV.')    
    @api.expect(apply_parser)
    # @Candidate_only
    def post(self, jp_id):
        args = self.apply_parser.parse_args()
        data = apply_cv_to_jp(jp_id, args)

        if data == 409:
            return response_object(
                code=409,
                message="CV này đã gửi vào tin đăng này."
            ), 409

        return response_object(data=data), 200



#################################
#
# Get job post detail for candidate
#
#################################
@api.route('/<int:jp_id>/cand')
class CandidateJP(Resource):
    @api.doc('Get job post by id for candidate.')
    @api.marshal_with(JobPostDto.job_post_for_cand, code=200)
    def get(self, jp_id):
        data = get_job_post_for_candidate(jp_id)
        return response_object(data=data)



#################################
#
# Search job post for candidate
#
#################################
cand_search_jp_parser = api.parser() 
cand_search_jp_parser.add_argument("posted_date", type=int, location="args", required=False) # Today, 3 days, 7 days, ...
cand_search_jp_parser.add_argument("contract_type", type=int, location="args", required=False) # fulltime (0), parttime (1), internship (2)
cand_search_jp_parser.add_argument("max_salary", type=float, location="args", required=False)
cand_search_jp_parser.add_argument("min_salary", type=float, location="args", required=False)
cand_search_jp_parser.add_argument("page", type=int, location="args", required=False, default=1)
cand_search_jp_parser.add_argument("page-size", type=int, location="args", required=False, default=10)
cand_search_jp_parser.add_argument("q", location="args", required=False)
cand_search_jp_parser.add_argument("province_id", type=int, location="args", required=False)
@api.route('/cand')
class JobPostForCand(Resource):
    @api.doc('Get job post by id for candidate.')
    @api.expect(cand_search_jp_parser)
    @api.marshal_with(JobPostDto.job_post_in_search_cand_response, code=200)
    def post(self):
        args = cand_search_jp_parser.parse_args()
        (data, pagination) = search_jd_for_cand(args)
        return response_object(data=data, pagination=pagination)




#################################
#
# Reject/Approve CV
#
#################################
proceed_resume_parser = api.parser()
proceed_resume_parser.add_argument('status', type=int, required=True)
proceed_resume_parser.add_argument('submission_id', type=int, required=True)
@api.route('/<int:jp_id>/update')
class ProceedResume(Resource):
    @api.doc('Get job post by id for candidate.')
    @api.expect(proceed_resume_parser)
    @HR_only
    def post(self, jp_id):
        args = proceed_resume_parser.parse_args()
        identity = get_jwt_identity()
        recruiter_email = identity['email']        
        data = proceed_resume(jp_id, recruiter_email, args)
        return response_object(data=data)

