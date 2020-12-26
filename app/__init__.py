from app.main.util.dto import CandidateDto
from datetime import datetime
from os import error

from flask import Blueprint
from flask.globals import request
from flask_mail import Message
from flask_restx import Api, fields

from app.main.resource.errors import UnauthorizedError

from .main.controller.company_controller import api as company_ns
from .main.controller.account_controller import api as account_ns
from .main.controller.candidate_controller import apiCandidate as candidate_ns
from .main.controller.recruiter_controller import apiRecruiter as recruiter_ns
from .main.controller.job_post_controller import api as job_post_ns
from .main.controller.job_domain_controller import api as job_domain_ns
# from .main.controller.upload_controller import api as upload_ns
from .main.controller.resume_controller import api as resume_ns

blueprint = Blueprint('api', __name__, url_prefix="/api", template_folder='templates')


api = Api(blueprint,
          title='API DOCUMENT FOR AUTOMATED RESUME SCREENING',
          version='1.0'
          )

api.add_namespace(account_ns, path='/user')
api.add_namespace(company_ns, path='/company')
api.add_namespace(candidate_ns, path='/user')
api.add_namespace(recruiter_ns, path='/user')
api.add_namespace(job_post_ns, path='/job-posts')
api.add_namespace(job_domain_ns, path='/job-domains')
# api.add_namespace(upload_ns, path='/upload')
api.add_namespace(resume_ns, path='/resume')

@api.errorhandler(UnauthorizedError)
def handle_custom_exception(error):
    '''Access denied'''
    return {
        "timestamp": datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),
        "status": 403,
        "error": "Forbidden",
        "message": "Access denied",
        "path": request.url
    }, 403
