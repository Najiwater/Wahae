# main.py
import common_module as common
from student_class import Student
from professor_class import Professor
from admin_class import Admin

def main():
    """메인 실행 함수"""
    
    # --- 프로그램 시작 시 모든 데이터 로드 ---
    common.load_all_data()
    
    while True:
        common.clear_screen()
        print("================================")
        print("         학사관리 시스템         ")
        print("================================")
        print("1. 학생")
        print("2. 교수")
        print("3. 행정직원")
        print("4. 회원가입")
        print("5. 종료")
        print("--------------------------------")
        choice = input("메뉴 선택: ")

        if choice == '1':
            user_id = common.login('student')
            if user_id:
                student_handler = Student(user_id)
                student_handler.student_menu()
                
        elif choice == '2':
            user_id = common.login('professor')
            if user_id:
                prof_handler = Professor(user_id)
                prof_handler.professor_menu()

        elif choice == '3':
            user_id = common.login('admin')
            if user_id:
                admin_handler = Admin(user_id)
                admin_handler.admin_menu()

        elif choice == '4':
            common.signup()
            common.pause()

        elif choice == '5':
            print("프로그램을 종료합니다. 모든 변경사항이 저장되었습니다.")
            break

        else:
            print("잘못된 입력입니다. 1~5 사이의 숫자를 입력해주세요.")
            common.pause()

if __name__ == "__main__":
    main()