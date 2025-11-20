# admin_class.py
import data
import common_module as common
from datetime import datetime

class Admin:
    def __init__(self, user_id):
        self.user_id = user_id
        self.info = data.admins[user_id] 

    def admin_menu(self):
        while True:
            common.clear_screen()
            print(f"--- 행정직원 메뉴 ({self.info['name']}님) ---")
            print("1. 강좌 개설 (학점, 시간표 포함)")
            print("2. 강좌 삭제")
            print("3. 공지사항 관리")
            print("4. 학적 변동 신청 관리")
            print("5. 사용자 계정 관리")
            print("6. 전체 목록 조회 (학생/교수/강좌)")
            print("7. 공지사항 조회 (공통)")
            print("8. 내 정보 조회/수정 (비밀번호 변경)")
            print("0. 로그아웃")
            choice = input("메뉴 선택: ")

            if choice == '1': self.create_course()
            elif choice == '2': self.delete_course()
            elif choice == '3': self.manage_notices()
            elif choice == '4': self.process_academic_requests()
            elif choice == '5': self.manage_users_menu()
            elif choice == '6': self.view_all_lists_menu()
            elif choice == '7': common.view_notices()
            elif choice == '8': self.my_profile_menu()
            elif choice == '0': print("로그아웃합니다."); common.pause(); break
            else: print("잘못된 입력입니다."); common.pause()

    # --- 사용자 관리 기능 (추가/삭제/초기화) ---

    def manage_users_menu(self):
        """(수정) 5. 사용자 관리 서브메뉴 - 계정 추가/삭제/비밀번호 초기화"""
        while True:
            common.clear_screen()
            print("--- 사용자 계정 관리 ---")
            print("1. 신규 사용자 계정 추가 (학생/교수/행정직원)")
            print("2. 기존 사용자 계정 삭제")
            print("3. 사용자 비밀번호 초기화")
            print("0. 뒤로가기")
            choice = input("선택: ")
            
            if choice == '1':
                print("\n**추가할 계정의 역할을 선택하세요.**")
                print(" 1) 학생  2) 교수  3) 행정직원")
                role_choice = input("선택: ")
                if role_choice == '1': self.add_user('student')
                elif role_choice == '2': self.add_user('professor')
                elif role_choice == '3': self.add_user('admin')
                else: print("잘못된 선택입니다."); common.pause()
            
            elif choice == '2':
                self.delete_user()
            
            elif choice == '3':
                self.reset_password()
                
            elif choice == '0':
                break
            else:
                print("잘못된 입력입니다."); common.pause()

    def add_user(self, role):
        """(기존) 사용자 추가 공통 함수"""
        common.clear_screen()
        print(f"--- {role.upper()} 계정 추가 ---")
        
        while True:
            user_id = input(f"사용할 아이디: ")
            if user_id in data.users:
                print("이미 존재하는 아이디입니다.")
            elif not user_id:
                print("아이디는 비워둘 수 없습니다.")
            else:
                break
                
        password = input(f"사용할 초기 비밀번호 (미입력 시 '1234'): ")
        if not password:
            password = "1234"
            
        name = input(f"이름: ")

        # data.users에 기본 정보 추가
        data.users[user_id] = {'password': password, 'role': role}
        
        # 역할(role)에 따라 상세 정보 추가
        if role == 'student':
            student_id = input("학번: ")
            major = input("전공: ")
            data.students[user_id] = {
                'name': name, 'student_id': student_id,
                'major': major, 'courses': [], 'status': '재학'
            }
            # 초기 성적 정보 생성
            data.grades[user_id] = {}
            common.save_students(); common.save_grades()
            print(f"\n[학생] {name}({user_id})님 계정이 추가되었습니다.")
        
        elif role == 'professor':
            professor_id = input("교번: ")
            department = input("소속 학과: ")
            data.professors[user_id] = {
                'name': name, 'professor_id': professor_id,
                'department': department, 'courses_taught': []
            }
            common.save_professors()
            print(f"\n[교수] {name}({user_id})님 계정이 추가되었습니다.")

        elif role == 'admin':
            admin_id = input("직원번호: ")
            department = input("소속 부서: ")
            data.admins[user_id] = {
                'name': name, 'admin_id': admin_id,
                'department': department
            }
            common.save_admins()
            print(f"\n[행정직원] {name}({user_id})님 계정이 추가되었습니다.")
        
        # 공통 users.json 파일 저장
        common.save_users()
        common.pause()

    def delete_user(self):
        """(신규) 사용자 계정 삭제 기능"""
        common.clear_screen()
        print("--- 사용자 계정 삭제 ---")
        
        user_id = input("삭제할 사용자의 ID를 입력하세요 (0: 취소): ")
        if user_id == '0': return
        
        if user_id not in data.users:
            print("존재하지 않는 사용자 ID입니다.")
            common.pause()
            return
            
        if user_id == self.user_id:
            print("현재 로그인한 본인의 계정은 삭제할 수 없습니다.")
            common.pause()
            return

        user_role = data.users[user_id]['role']
        name = "N/A"
        
        # 1. 역할별 상세 데이터 삭제 및 이름 확인
        if user_role == 'student':
            name = data.students.pop(user_id, {}).get('name', 'N/A')
            # 수강 강좌 정리 (만약 학생이 수강 중이었다면)
            for course_id, course_info in data.courses.items():
                if user_id in course_info['student_user_ids']:
                    course_info['student_user_ids'].remove(user_id)
            if user_id in data.grades:
                del data.grades[user_id] # 성적 정보 삭제
            common.save_students(); common.save_courses(); common.save_grades()
            
        elif user_role == 'professor':
            name = data.professors.pop(user_id, {}).get('name', 'N/A')
            # 담당 강좌 정리 (담당 교수를 'TBD'로 변경)
            for course_id, course_info in data.courses.items():
                if course_info['professor_user_id'] == user_id:
                    course_info['professor_user_id'] = 'TBD' 
            common.save_professors(); common.save_courses()
            
        elif user_role == 'admin':
            name = data.admins.pop(user_id, {}).get('name', 'N/A')
            common.save_admins()
            
        # 2. users.json에서 로그인 정보 삭제
        del data.users[user_id]
        common.save_users()
        
        print(f"\n[{user_role.upper()}] {name}({user_id}) 계정이 시스템에서 완전히 삭제되었습니다.")
        common.pause()

    def reset_password(self):
        """(신규) 사용자 비밀번호 초기화 기능"""
        common.clear_screen()
        print("--- 사용자 비밀번호 초기화 ---")

        user_id = input("비밀번호를 초기화할 사용자의 ID를 입력하세요 (0: 취소): ")
        if user_id == '0': return

        if user_id not in data.users:
            print("존재하지 않는 사용자 ID입니다.")
            common.pause()
            return

        # 초기화할 비밀번호 설정 (기본값: 1234)
        new_password = input("새로운 초기 비밀번호를 입력하세요 (미입력 시 '1234'): ")
        if not new_password:
            new_password = '1234'
            
        data.users[user_id]['password'] = new_password
        common.save_users()
        
        print(f"\nID: {user_id} 사용자의 비밀번호가 '{new_password}'로 초기화되었습니다.")
        common.pause()
    # --- 사용자 관리 기능 끝 ---


    def my_profile_menu(self):
        common.clear_screen()
        print("--- 내 정보 관리 ---")
        print(f"이름: {self.info['name']}")
        print(f"직원번호: {self.info['admin_id']}")
        print(f"소속: {self.info['department']}")
        print("\n1. 비밀번호 변경")
        print("0. 뒤로가기")
        choice = input("선택: ")
        if choice == '1':
            common.change_password(self.user_id)
        else:
            return

    def create_course(self):
        common.clear_screen()
        print("--- 강좌 개설 ---")
        
        while True:
            course_id = input("개설할 강좌 코드 (예: C003): ").upper()
            if course_id in data.courses: print("이미 존재하는 강좌 코드입니다.")
            else: break
                
        title = input("강좌명: ")
        
        self.view_all_professors(pause=False)
        while True:
            prof_user_id = input("담당 교수의 로그인 ID: ")
            if prof_user_id not in data.professors: print("존재하지 않는 교수 ID입니다.")
            else: break
        
        while True:
            try: credits = float(input("이수 학점 (예: 3 또는 1.5): ")); break
            except ValueError: print("숫자를 입력해주세요.")
            
        while True:
            try: max_capacity = int(input("최대 수강 인원: ")); break
            except ValueError: print("숫자를 입력해주세요.")

        print("\n--- 시간표 입력 ---")
        while True:
            day = input("요일 (예: 월, 화, 수): ")
            if day not in ['월', '화', '수', '목', '금', '토', '일']: print("정확한 요일을 입력하세요."); continue
            break
        while True:
            try: start_time = int(input("시작 교시 (숫자, 24시 기준, 예: 10): ")); break
            except ValueError: print("숫자를 입력해주세요.")
        while True:
            try: end_time = int(input("종료 교시 (숫자, 24시 기준, 예: 12): ")); break
            except ValueError: print("숫자를 입력해주세요.")

        course_time = {'day': day, 'start': start_time, 'end': end_time}

        data.courses[course_id] = {
            'title': title, 'professor_user_id': prof_user_id,
            'student_user_ids': [], 'max_capacity': max_capacity,
            'credits': credits, 'time': course_time,
            'syllabus': '등록된 강의 계획서가 없습니다.',
            'weekly_content': []
        }
        data.professors[prof_user_id]['courses_taught'].append(course_id)
        
        common.save_courses(); common.save_professors()
        print(f"\n[{course_id}] {title} 강좌 개설이 완료되었습니다.")
        common.pause()

    def delete_course(self):
        common.clear_screen()
        print("--- 강좌 삭제 ---")
        
        if not self.view_all_courses(pause=False): common.pause(); return
        print("-" * 20)
        course_id = input("삭제할 강좌 코드를 입력하세요: ").upper()

        if course_id not in data.courses:
            print("존재하지 않는 강좌 코드입니다."); common.pause(); return

        course_to_delete = data.courses[course_id]
        prof_user_id = course_to_delete['professor_user_id']
        student_user_ids = course_to_delete['student_user_ids']

        if prof_user_id in data.professors and course_id in data.professors[prof_user_id]['courses_taught']:
            data.professors[prof_user_id]['courses_taught'].remove(course_id)
            common.save_professors()

        students_changed = False
        for student_user_id in student_user_ids:
            if student_user_id in data.students and course_id in data.students[student_user_id]['courses']:
                data.students[student_user_id]['courses'].remove(course_id)
                students_changed = True
        if students_changed: common.save_students()

        grades_changed = False
        for student_id in list(data.grades.keys()):
            if course_id in data.grades[student_id]:
                del data.grades[student_id][course_id]
                grades_changed = True
        if grades_changed: common.save_grades()
        
        if course_id in data.attendance:
            del data.attendance[course_id]
            common.save_attendance()
                
        del data.courses[course_id]
        common.save_courses()
        
        print(f"[{course_id}] 강좌 및 모든 수강/성적/출석 정보가 삭제되었습니다."); common.pause()

    def manage_notices(self):
        common.clear_screen()
        print("--- 공지사항 관리 ---")
        common.view_notices()
        
        print("\n1. 새 공지사항 작성")
        print("2. 공지사항 삭제")
        print("0. 뒤로가기")
        choice = input("선택: ")
        
        if choice == '1':
            title = input("제목: ")
            content = input("내용: ")
            new_id = str(len(data.notices) + 1)
            new_notice = {
                'id': new_id, 'title': title,
                'content': content, 'author': self.info['name']
            }
            data.notices.append(new_notice)
            common.save_notices()
            print("공지사항이 등록되었습니다.")
        
        elif choice == '2':
            notice_id = input("삭제할 공지사항 ID: ")
            notice_to_delete = None
            for notice in data.notices:
                if notice['id'] == notice_id:
                    notice_to_delete = notice; break
            
            if notice_to_delete:
                data.notices.remove(notice_to_delete)
                common.save_notices()
                print(f"[ID: {notice_id}] 공지사항이 삭제되었습니다.")
            else:
                print("해당 ID의 공지사항을 찾을 수 없습니다.")
        common.pause()
        
    def process_academic_requests(self):
        common.clear_screen()
        print("--- 학적 변동 신청 관리 ---")
        
        pending_requests = [req for req in data.academic_requests if req['status'] == 'pending']
        
        if not pending_requests:
            print("대기 중인 신청이 없습니다."); common.pause(); return

        print("--- 승인 대기 목록 ---")
        for req in pending_requests:
            print(f"[ID: {req['req_id']}] {req['student_name']} ({req['student_user_id']}) - {req['type']} 신청 (사유: {req['reason']})")
        
        print("-" * 20)
        req_id = input("처리할 신청 ID (0: 취소): ")
        if req_id == '0': return

        target_req = None
        for req in data.academic_requests:
            if req['req_id'] == req_id and req['status'] == 'pending':
                target_req = req; break
                
        if not target_req:
            print("해당 ID의 대기 중인 신청을 찾을 수 없습니다."); common.pause(); return

        print(f"\n[ID: {req_id}] {target_req['type']} 신청을 처리합니다.")
        print("1. 승인 (Approve)")
        print("2. 반려 (Reject)")
        print("0. 취소")
        choice = input("선택: ")

        if choice == '1':
            target_req['status'] = 'approved'
            student_id = target_req['student_user_id']
            if student_id in data.students:
                if target_req['type'] == '복학':
                    data.students[student_id]['status'] = '재학'
                else:
                    data.students[student_id]['status'] = target_req['type']
                common.save_students()
                common.save_academic_requests()
                print(f"{target_req['student_name']} 학생의 {target_req['type']}이(가) 승인되었습니다.")
            else:
                print("오류: 해당 학생 정보를 찾을 수 없습니다.")
        
        elif choice == '2':
            target_req['status'] = 'rejected'
            common.save_academic_requests()
            print("반려 처리되었습니다.")
            
        common.pause()

    def view_all_lists_menu(self):
        common.clear_screen()
        print("--- 전체 목록 조회 ---")
        print("1. 전체 학생 목록")
        print("2. 전체 교수 목록")
        print("3. 전체 강좌 목록")
        print("0. 뒤로가기")
        choice = input("선택: ")
        
        if choice == '1': self.view_all_students(pause=True)
        elif choice == '2': self.view_all_professors(pause=True)
        elif choice == '3': self.view_all_courses(pause=True)
        else: return

    def view_all_students(self, pause=True):
        if pause: common.clear_screen()
        print("--- 전체 학생 목록 ---")
        if not data.students: print("등록된 학생이 없습니다.")
        else:
            for user_id, info in data.students.items():
                print(f"[{info['student_id']}] {info['name']} ({info['major']}) [학적: {info.get('status', 'N/A')}, ID: {user_id}]")
        if pause: common.pause()

    def view_all_professors(self, pause=True):
        if pause: common.clear_screen()
        print("--- 전체 교수 목록 ---")
        if not data.professors: print("등록된 교수가 없습니다.")
        else:
            for user_id, info in data.professors.items():
                print(f"[{info['professor_id']}] {info['name']} ({info['department']}, ID: {user_id})")
        if pause: common.pause()

    def view_all_courses(self, pause=True):
        if pause: common.clear_screen()
        print("--- 전체 강좌 목록 ---")
        if not data.courses: print("개설된 강좌가 없습니다.")
        else:
            for cid, course in data.courses.items():
                prof_name = data.professors.get(course['professor_user_id'], {}).get('name', 'N/A')
                student_count = len(course['student_user_ids'])
                max_cap = course.get('max_capacity', 'N/A')
                print(f"[{cid}] {course['title']} (담당: {prof_name}, 학점: {course.get('credits', 'N/A')}) [정원: {student_count}/{max_cap}]")
        if pause: common.pause()