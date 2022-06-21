from http import HTTPStatus
from multiprocessing import connection
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector
from mysql_connection import get_connection

# --------------메모 생성---------------
class MemoListResource(Resource):
    @ jwt_required()

    def post(self):

        data = request.get_json()
        user_id= get_jwt_identity()

        try:
            # 데이터 insert 
            # 1. DB에 연결
            connection = get_connection()
# {
#     "title": "오전 미팅 주제",
#     "date": "2022-01-22",
#     "content": " 어댑터 만들어서 어쩌고 저쩌고 동해물과 백두산이 어쩌고.."
# }

            # 2. 쿼리문 만들기
            query = '''insert into recipe
                    (title,date,content,user_id)
                    values
                    (%s,%s,%s,%s,%s);'''
            record = (data['title'],data['date'], data['content'], user_id )

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query,record)

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {"error": str(e)}, 503

        return {"result":"success"},200

# # --------------생성한 메모 조회 --------------
#     def get(self):
#         # 저장되어있는 모든 API를 가져오는 것. 우선 mysql로 간다. 쿼리문을 가져와야하기 때문
#         # 쿼리 스트링으로 오는 데이터는 아래처럼 처리해준다.
#         offset = request.args.get('offset')
#         limit = request.args.get('limit')

#         try :
#             connection = get_connection()

#             query = '''select *
#                     from memo
#                     where is_publish =1;'''

#             cursor = connection.cursor(dictionary = True)
#             cursor.execute(query)

#             result_list = cursor.fetchall()

#             print(result_list)

#             i = 0
#             for record in result_list :
#                 # 한 행씩 가져와서, 그 행에 들어있는 i번째의 created_at을 ios 포맷으로 바꿔라.  
#                 result_list[i]['created_at'] = record['created_at'].isoformat()
#                 result_list[i]['updated_at'] = record['updated_at'].isoformat()
#                 i = i + 1             
                
#             cursor.close()
#             connection.close()


#         except mysql.connector.Error as e :
#             print(e)
#             cursor.close()
#             connection.close()

#             return {"error" : str(e)}, 503
#             # 503으로 보내겠다.
 
#         return { "result" : "success" , 
#                 "count" : len(result_list) ,
#                 "result_list" : result_list }, 200
#                 # 첫번째 키값
        