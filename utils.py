from passlib.hash import pbkdf2_sha256 # 이건, 암호화 알고리즘. 256을 제일 많이 씀

# 원문 비밀번호를, 암호화 하는 함수

def hash_password(original_password):
    salt = 'yh*hello12'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password

# 비밀번호가 맞는지 확인하는 함수, True/False를 리턴한다.
def check_password(original_password, hashed_password):
    # 이미 라이브러리가 있다.
    salt = 'yh*hello12'
    check = pbkdf2_sha256.verify(original_password + salt, hashed_password)
    # True인지 False인지 체크를 해준다.

    return check
    
