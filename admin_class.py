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
            print("3. 공지사항 관리 (신규)")
            print("4. 학적 변동 신청 관리 (신규)")
            print("5. 전체 목록 조회 (학생/교수/강좌)")
            print("6. 공지사항 조회 (공통)")
            print("7. 내 정보 조회/수정 (비밀번호 변경)")
            print("0. 로그아웃")
            choice = input("메뉴 선택: ")

            if choice == '1': self.create_course()
            elif choice == '2': self.delete_course()
            elif choice == '3': self.manage_notices()
            elif choice == '4': self.process_academic_requests()
            elif choice == '5': self.view_all_lists_menu()
            elif choice == '6': common.view_notices()
            elif choice == '7': self.my_profile_menu()
            elif choice == '0': print("로그아웃합니다."); common.pause(); break
            else: print("잘못된 입력입니다."); common.pause()

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
        """(수정) 1. 강좌 개설 (학점, 시간표 추가)"""
        common.clear_screen()
        print("--- 강좌 개설 ---")
        
        while True:
            course_id = input("개설할 강좌 코드 (예: C003): ").upper()
            if course_id in data.courses: print("이미 존재하는 강좌 코드입니다.")
            else: break
                
        title = input("강좌명: ")
        
        # 교수 목록 보여주기
        self.view_all_professors(pause=False)
        while True:
            prof_user_id = input("담당 교수의 로그인 ID: ")
            if prof_user_id not in data.professors: print("존재하지 않는 교수 ID입니다.")
            else: break
        
        # (신규) 학점 입력
        while True:
            try: credits = float(input("이수 학점 (예: 3 또는 1.5): ")); break
            except ValueError: print("숫자를 입력해주세요.")
            
        # (신규) 최대 인원 입력
        while True:
            try: max_capacity = int(input("최대 수강 인원: ")); break
            except ValueError: print("숫자를 입력해주세요.")

        # (신규) 시간표 입력
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

        # 새 강좌 데이터 구조
        data.courses[course_id] = {
            'title': title,
            'professor_user_id': prof_user_id,
            'student_user_ids': [],
            'max_capacity': max_capacity,
            'credits': credits,
            'time': course_time,
            'syllabus': '등록된 강의 계획서가 없습니다.', # 기본값
            'weekly_content': [] # 기본값
        }
        data.professors[prof_user_id]['courses_taught'].append(course_id)
        
        common.save_courses(); common.save_professors()
        print(f"\n[{course_id}] {title} 강좌 개설이 완료되었습니다.")
        common.pause()

    def delete_course(self):
        """2. 강좌 삭제 (연관된 모든 데이터 삭제)"""
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

        # 1. 교수 정보에서 삭제
        if prof_user_id in data.professors and course_id in data.professors[prof_user_id]['courses_taught']:
            data.professors[prof_user_id]['courses_taught'].remove(course_id)
            common.save_professors()

        # 2. 학생 수강 정보에서 삭제
        students_changed = False
        for student_user_id in student_user_ids:
            if student_user_id in data.students and course_id in data.students[student_user_id]['courses']:
                data.students[student_user_id]['courses'].remove(course_id)
                students_changed = True
        if students_changed: common.save_students()

        # 3. 성적 정보에서 삭제
        grades_changed = False
        for student_id in list(data.grades.keys()):
            if course_id in data.grades[student_id]:
                del data.grades[student_id][course_id]
                grades_changed = True
        if grades_changed: common.save_grades()
        
        # 4. (신규) 출석 정보에서 삭제
        if course_id in data.attendance:
            del data.attendance[course_id]
            common.save_attendance()
                
        # 5. 강좌 자체 삭제
        del data.courses[course_id]
        common.save_courses()
        
        print(f"[{course_id}] 강좌 및 모든 수강/성적/출석 정보가 삭제되었습니다."); common.pause()

    def manage_notices(self):
        """(신규) 3. 공지사항 관리"""
        common.clear_screen()
        print("--- 공지사항 관리 ---")
        common.view_notices() # 현재 공지 목록 먼저 보여주기
        
        print("\n1. 새 공지사항 작성")
        print("2. 공지사항 삭제")
        print("0. 뒤로가기")
        choice = input("선택: ")
        
        if choice == '1':
            title = input("제목: ")
            content = input("내용: ")
            # 새 공지 ID 생성 (간단하게)
            new_id = str(len(data.notices) + 1)
            new_notice = {
                'id': new_id,
                'title': title,
                'content': content,
                'author': self.info['name']
            }
            data.notices.append(new_notice)
            common.save_notices()
            print("공지사항이 등록되었습니다.")
        
        elif choice == '2':
            notice_id = input("삭제할 공지사항 ID: ")
            notice_to_delete = None
            for notice in data.notices:
                if notice['id'] == notice_id:
                    notice_to_delete = notice
                    break
            
            if notice_to_delete:
                data.notices.remove(notice_to_delete)
                common.save_notices()
                print(f"[ID: {notice_id}] 공지사항이 삭제되었습니다.")
            else:
                print("해당 ID의 공지사항을 찾을 수 없습니다.")
        common.pause()
        
    def process_academic_requests(self):
        """(신규) 4. 학적 변동 신청 관리"""
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
                target_req = req
                break
                
        if not target_req:
            print("해당 ID의 대기 중인 신청을 찾을 수 없습니다."); common.pause(); return

        print(f"\n[ID: {req_id}] {target_req['type']} 신청을 처리합니다.")
        print("1. 승인 (Approve)")
        print("2. 반려 (Reject)")
        print("0. 취소")
        choice = input("선택: ")

        if choice == '1':
            target_req['status'] = 'approved'
            # (중요) 학생 정보(data.students)의 상태(status)를 실제로 변경
            student_id = target_req['student_user_id']
            if student_id in data.students:
                # 간단한 로직: 휴학/자퇴는 상태 변경, 복학은 '재학'으로 변경
                if target_req['type'] == '복학':
                    data.students[student_id]['status'] = '재학'
                else:
                    data.students[student_id]['status'] = target_req['type'] # '휴학' 또는 '자퇴'
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
        """5. 전체 목록 조회 서브메뉴"""
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