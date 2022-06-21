from http import HTTPStatus
from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

from email_validator import validate_email, EmailNotValidError

from utils import check_password, hash_password

# ----------회원가입------------

class UserRegisterResource(Resource):
    def post(self):
    #     {
    # "email": "abc@naver.com",
    # "password": "1234",
    # "username": "홍길동"
    #   }

        # 1. 쿨라이언트가 body에 보내준 json을 받아온다.
        # body로 받는 데이터는 아래 함수를 사용한다.
        data = request.get_json()

        # 2. 이메일 주소형식이 제대로 된 주소형식인지, 확인하는 코드 작성.
        try:
            validate_email(data['email'])

        except EmailNotValidError as e:
            print(str(e))
            return {'error': str(e)}, 400

        # 3. 비밀번호의 길이가 유효한지 체크한다.
        # 비번 길이는 4자리 이상, 12자리 이하로만!
        if len(data['password'])< 4 or len(data['password']) > 12:
            return {'error': "비번 길이를 확인하세요"},400

        # 4. 비밀번호를 암호화 한다.
        hashed_password = hash_password( data['password'] )
        print(hashed_password)

        # 5. DB에 회원정보를 저장한다.

        try:
            # 데이터 insert 
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into user
                    (email,password,user_name)
                    values
                    (%s,%s,%s);'''
            record = ( data['email'], hashed_password, data['username'])

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query,record)

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # 5-1 DB에 저장된 아이디값 가져오기.
            user_id = cursor.lastrowid

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"error": str(e)}, 503
        
        # 암호화 하는 방법
        access_token = create_access_token(user_id)
        # 대게는 이런 변수명으로 저장한다.

        return {"result":"success", 'access_token': access_token},200



# --------- 로그인
class UserLoginResource(Resource):

    def post (self):

        # 0. postman가서 API를 먼저 만든다. 

        # {
        # "email": "abc@gmail.com",
        # "password": "1234"
        # }

        # 1. 클라이어런트로부터 body로 넘어온 데이터를 받아온다. (email와 passwords) 

        data = request.get_json()

        # 2. email로, DB에 이 이메일과 일치하는 데이터를 가져온다.
        try :
            connection = get_connection()

            query = '''select *
                    from user
                    where email = %s;'''

            record = (data['email'] , )

        # select문은, dictionary = True를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query, record)

            # select문은, 아래 함수를 이용해서, 데이터를 가져온다. 
            result_list = cursor.fetchall()
            # 여기에 쿼리의 결과가 있음
            # 암호화 하고, DB 회원 테이블에다가 insert, 인서트한 커서에 방금 insert한 user_id를 가져온다. 

            print(result_list)
            # 디버깅 하라 때는 프린트문을 항상 찍어본다. 

            # 중요! 디비에서 가져온 timestamp 는 
            # 파이썬의 datetime 으로 자동 변경된다.
            # 문제는! 이데이터를 json 으로 바로 보낼수 없으므로,
            # 문자열로 바꿔서 다시 저장해서 보낸다.
            i = 0
            for record in result_list :
                result_list[i]['created_at'] = record['created_at'].isoformat()
                result_list[i]['updated_at'] = record['updated_at'].isoformat()
                i = i + 1               
                
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e)}, 503

        # 3. result_list의 행의 갯수가 1개이면, 유저 데이터를 정상적으로 받아온것이고, 
        # 행의 갯수가 0이면, 요청한 이메일은, 회원가입이 되어있지 않은 이메일이다.

        if len(result_list) !=1:
            return{'error': ' 회원가입이 안된 이메일입니다.'}, 400

        # 4. 비밀번호가 맞는지 확인한다.
        user_info = result_list[0]
        # 결과가 리스트니까, 리스트 안에있는 딕셔너리를 가져오겠다는 뜻

        # data['password']와 user_info['password']를 비교
        check = check_password(data['password'],user_info['password'])

        if check == False:
            return {'error':'비밀번호가 맞지 않습니다.'}
            
        # user_id를 바로 보내면 안되고, JWT로 암호화 해서 보내준다.
        # 암호화 하는 방법
        access_token = create_access_token(user_info['id'])
        # 대게는 이런 변수명으로 저장한다.

        return {'result': 'success',
                'access_token':access_token},200

        # return {'result': 'success',
        #         'user_id':user_info['id']},200
    
# ------------------------------------------#
from flask_jwt_extended import get_jwt

jwt_blacklist = set()

# 로그아웃 기능을 하는 클래스 (2022.06.21)
class UserLogoutResource(Resource) :
    @jwt_required()   # 헤더에 access토큰이 있는 요청만 수행한다.
    def post(self):
        jti = get_jwt()['jti']
        print(jti)
        
        jwt_blacklist.add(jti)

        return {'result':'success'},200





