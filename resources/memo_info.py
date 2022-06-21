from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class MemoCreateResource(Resource) :
 
# --------------------------------------------
#                 메모 생성
# --------------------------------------------
    @ jwt_required()
    def post(self):

        data = request.get_json()
        user_id= get_jwt_identity()

        # {
        #     "title": "오전 미팅 주제",
        #     "date": "2022-01-22",
        #     "content": " 어댑터 만들어서 어쩌고 저쩌고 동해물과 백두산이 어쩌고.."
        # }

        try:
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into memo
                    (title, date, content, user_id)
                    values
                    (%s,%s,%s,%s);'''
            record = (data['title'],data['date'], data['content'],user_id )

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

# -------------------------------------------
#           메모 조회
# -------------------------------------------
    def get(self):
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select *
                    from memo
                    where is_publish =1
                    limit '''+offset+''' , '''+limit+''';'''

            cursor = connection.cursor(dictionary = True)
            cursor.execute(query)

            result_list = cursor.fetchall()

            print(result_list)

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

        return { "result" : "success" , 
                "count" : len(result_list)}, 200

