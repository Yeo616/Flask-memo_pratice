from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.memo_info import MemoCreateResource
from resources.memo_others import MemoResource
from resources.memo_publish import MemoPublishResource
from resources.memo_share import MemoShaereResource
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


api.add_resource(MemoCreateResource,'/memo/view') 
# 메모 생성, 메모 조회
api.add_resource(MemoResource,'/memo/<int:memo_id>')
# 메모 조회, 업데이트/수정, 삭제
api.add_resource(MemoPublishResource,'/memo/<int:memo_id>/publish') 
# 메모 공개, 임시저장 
api.add_resource(MemoShaereResource,'/friends/view')
# 친구 생성/맺기, 

if __name__ == '__main__':
    app.run()
    