from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector


# 친구 맺기(팔로우 팔로이)
# 내 친구들의 메모만 불러오기
# 친구 끊기


class MemoShaereResource(Resource) :
    
# -------------------------------
#         친구 생성하기
# --------------------------------
    @ jwt_required()
    def post(self):

        data = request.get_json()
        user_id= get_jwt_identity()

        # 쿼리문
        # {
        #     "follower_id": 2,
        #     "followee_id": 3
        # }

        try:
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''insert into follows
                    (follower_id, followee_id)
                    values
                    (%s,%s);'''
            record = (data['follower_id'],data['followee_id'] )

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
#                친구 조회
# -------------------------------------------
    # def get(self):
    #     offset = request.args.get('offset')
    #     limit = request.args.get('limit')

    #     try :
    #         connection = get_connection()

    #         query = '''select *
    #                 from follows f
    #                 join user u
    #                     on f.followee_id = u.id
    #                 where f.followee_id =1;'''

    #         cursor = connection.cursor(dictionary = True)
    #         cursor.execute(query)

    #         result_list = cursor.fetchall()

    #         print(result_list)

    #         i = 0
    #         for record in result_list :
    #             result_list[i]['created_at'] = record['created_at'].isoformat()
    #             i = i + 1             
                
    #         cursor.close()
    #         connection.close()

    #     except mysql.connector.Error as e :
    #         print(e)
    #         cursor.close()
    #         connection.close()
    #         return {"error" : str(e)}, 503

    #     return { "result" : "success" , 
    #             "count" : len(result_list)}, 200

