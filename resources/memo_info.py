from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class MemoResource(Resource) :
    # 클라이언트로부터 /recipes/3 이런식으로 경로를 처리하므로
    def get(self, memo_id) :

        try :
            connection = get_connection()

            query = '''select *
                    from memo
                    where id = %s ;'''
            record = (memo_id, )
            
            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            cursor.execute(query, record)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
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


        return {'result' : 'success' ,
                'info' : result_list[0]}

    @jwt_required()
    # 데이터를 업데이트하는 API들은 put 함수를 사용한다.
    def put(self, recipe_id) :

        # body에서 전달된 데이터를 처리
        data = request.get_json()

        user_id = get_jwt_identity()


        # 디비 업데이트 실행코드
        try :
            # 데이터 업데이트 
            # 1. DB에 연결
            connection = get_connection()

            ### 먼저 recipe_id에 들어있는 user_id가 이 사람인지 먼저 확인한다.

            query = '''select user_id
                        from memo
                        where id = %s;'''
            record = (recipe_id,)

            # 커서 가져와서 execute
            cursor = connection.cursor(dictionary = True)
            cursor.execute(query, record)
            # 실행을 시키면 result_list가 온다. 
            result_lsit = cursor.fetchall()

            if len(result_lsit) == 0:
                cursor.close()
                connection.close()
                return{'error':'레시피 아이디가 잘못되었습니다.'},400

            recipe = result_lsit[0] # 레시피

            if recipe['user_id'] != user_id:
                cursor.close()
                connection.close()
                return{'error':'타인의 레시피를 수정할 수 없습니다.'},401
# ------------------------------------
            # 2. 쿼리문 만들기
            query = '''update recipe
                    set name = %s , description = %s , 
                    cook_time = %s , 
                    directions = %s
                    where id = %s ;'''
            
            record = (data['name'], data['description'],
                        data['cook_time'], data['directions'],
                        recipe_id )

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 503

        return {'result' :'success'}, 200


    # 삭제하는 delete 함수
    def delete(self, recipe_id) :

        # 디비 업데이트 실행코드
        try :
            # 데이터 삭제
            # 1. DB에 연결
            connection = get_connection()

            # 2. 쿼리문 만들기
            query = '''delete from recipe
                    where id = %s;'''
            
            record = (recipe_id, )

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다.
            cursor.execute(query, record)

            # 5. 커넥션을 커밋해줘야 한다 => 디비에 영구적으로 반영하라는 뜻
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 503

        return {'result':'success'},200