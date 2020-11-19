from flask_restx import Namespace, fields


class UserDto:
    api = Namespace(
        'User', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        # 'public_id': fields.String(description='user Identifier')
    })
    user_login = api.model('user_login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        # 'public_id': fields.String(description='user Identifier')
    })