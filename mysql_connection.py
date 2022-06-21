import mysql.connector 

def get_connection():
    connection = mysql.connector.connect(
        host = 'yh-db.c6isfff1nnnu.ap-northeast-2.rds.amazonaws.com',
        # host 를 써야, 접속할수가 있다. mysql참고 혹은 aws 참고
        database = 'memo',
        # mysql의 스키마 이름
        user = 'memo_user',
        password = 'memo1234'
    )
    return connection