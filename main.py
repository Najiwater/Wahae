# main.py

import common_module as common
import data
from admin_class import Admin
from student_class import Student
from professor_class import Professor
# ... (다른 import) ...


def login(role):
    """
    (main.py 내부에 추가)
    사용자 ID와 비밀번호를 받아 로그인 처리를 수행하는 함수
    """
    common.clear_screen()
    print(f"--- {role.upper()} 로그인 ---")

    user_id = input("아이디: ")
    password = input("비밀번호: ")

    if user_id not in data.users:
        print("존재하지 않는 사용자 ID입니다.")
        common.pause()
        return None

    user_info = data.users[user_id]
    
    # 1. 역할 일치 확인
    if user_info['role'] != role:
        print("선택하신 역할(메뉴)과 ID의 역할이 일치하지 않습니다. 올바른 메뉴를 선택해주세요.")
        common.pause()
        return None
    
    # 2. 비밀번호 확인
    if user_info['password'] == password:
        # 로그인 성공 시 이름을 가져와서 표시
        user_name = "사용자"
        if role == 'student' and user_id in data.students: user_name = data.students[user_id]['name']
        elif role == 'professor' and user_id in data.professors: user_name = data.professors[user_id]['name']
        elif role == 'admin' and user_id in data.admins: user_name = data.admins[user_id]['name']
        
        print(f"\n✨ {user_name}님 ({user_id}) 환영합니다! ✨")
        common.pause()
        return user_id
    else:
        print("비밀번호가 일치하지 않습니다.")
        common.pause()
        return None


def main():
    common.load_all_data() # 데이터 로드 확인
    
    while True:
        common.clear_screen()
        print("--- 학사 관리 시스템 ---")
        print("1. 학생")
        print("2. 교수")
        print("3. 행정직원")
        print("0. 종료")
        choice = input("메뉴 선택: ")

        user_id = None
        
        if choice == '1':
            user_id = login('student') # common.login('student') 대신 login('student') 호출
            if user_id:
                student = Student(user_id)
                student.student_menu()

        elif choice == '2':
            user_id = login('professor') # common.login('professor') 대신 login('professor') 호출
            if user_id:
                professor = Professor(user_id)
                professor.professor_menu()

        elif choice == '3':
            user_id = login('admin') # common.login('admin') 대신 login('admin') 호출
            if user_id:
                admin = Admin(user_id)
                admin.admin_menu()
                
        elif choice == '0':
            print("시스템을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")
            common.pause()

if __name__ == '__main__':
    main()