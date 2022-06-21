from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.memo_list import MemoListResource
from resources.memo_info import MemoResource
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource

app = Flask(__name__)

app.config.from_object(Config)
jwt = JWTManager(app)


api = Api(app)

from resources.user import jwt_blacklist

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload):
    # 메뉴얼에 써져있는 내용
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api.add_resource(UserRegisterResource,'/users/register')
api.add_resource(UserLoginResource,'/users/login')
api.add_resource(UserLogoutResource, '/users/logout')


api.add_resource(MemoResource,'/memo/<int:recipe_id>') 
api.add_resource(MemoListResource,'/memo')

if __name__ == '__main__':
    app.run()
    