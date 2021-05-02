from app.main.service.career_service import match_domains_with_cand_skills
from app.main.util.custom_jwt import Candidate_only
from ..util.dto import CareerDto
from flask_restx import Resource
from flask import request
from flask_jwt_extended.utils import get_jwt_identity

api = CareerDto.api

explore_skills = api.parser()
explore_skills.add_argument("Authorization", location="headers", required=False)
@api.route('/career/explore_skills')
class ExploreSkills(Resource):
    @api.doc("explore skills matching with domain")
    @api.expect(explore_skills)
    @Candidate_only
    def get(self):
        identity = get_jwt_identity()
        email = identity['email']        
        return match_domains_with_cand_skills(email)