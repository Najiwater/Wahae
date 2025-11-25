# professor_class.py
import data
import common_module as common

class Professor:
    def __init__(self, user_id):
        self.user_id = user_id
        self.info = data.professors[user_id] 

    def professor_menu(self):
        while True:
            common.clear_screen()
            print(f"--- 교수 메뉴 ({self.info['name']}님) ---")
            print("1. 내 담당 강좌 관리 (계획서, 주차별 내용)")
            print("2. 담당 강좌 출석 관리")
            print("3. 담당 강좌 성적 관리")
            print("4. 강좌별 수강생 목록")
            print("5. 공지사항 조회")
            print("6. 내 정보 조회/수정 (비밀번호 변경)")
            print("0. 로그아웃")
            choice = input("메뉴 선택: ")

            if choice == '1': self.manage_lecture_content()
            elif choice == '2': self.manage_attendance()
            elif choice == '3': self.manage_grades()
            elif choice == '4': self.view_students_in_course()
            elif choice == '5': common.view_notices()
            elif choice == '6': self.my_profile_menu()
            elif choice == '0': print("로그아웃합니다."); common.pause(); break
            else: print("잘못된 입력입니다."); common.pause()

    def my_profile_menu(self):
        common.clear_screen()
        print("--- 내 정보 관리 ---")
        print(f"이름: {self.info['name']}")
        print(f"교번: {self.info['professor_id']}")
        print(f"소속: {self.info['department']}")
        print("\n1. 비밀번호 변경")
        print("0. 뒤로가기")
        choice = input("선택: ")
        if choice == '1':
            common.change_password(self.user_id)
        else:
            return

    def _select_my_course(self, menu_title):
        """(신규) 내 강좌를 선택하는 헬퍼 함수"""
        common.clear_screen()
        print(f"--- {menu_title} ---")
        
        if not self.info['courses_taught']:
            print("담당 중인 강좌가 없습니다."); common.pause(); return None
        
        print("--- 내 담당 강좌 목록 ---")
        for course_id in self.info['courses_taught']:
            course = data.courses.get(course_id)
            if course:
                print(f"[{course_id}] {course['title']}")
        
        print("-" * 20)
        course_id = input("관리할 과목 코드를 입력하세요: ").upper()
        
        if course_id not in self.info['courses_taught']:
            print("담당하고 있는 과목이 아닙니다."); common.pause(); return None
            
        return course_id, data.courses[course_id]

    def manage_lecture_content(self):
        """(신규) 1. 강의 계획서 및 주차별 내용 관리"""
        result = self._select_my_course("강의 콘텐츠 관리")
        if not result: return
        
        course_id, course = result

        while True:
            common.clear_screen()
            print(f"--- [{course_id}] {course['title']} 관리 ---")
            print("1. 강의 계획서(Syllabus) 수정")
            print("2. 주차별 학습 내용 관리")
            print("0. 뒤로가기")
            choice = input("선택: ")

            if choice == '1':
                print("\n[현재 강의 계획서]")
                print(course.get('syllabus', 'N/A'))
                print("\n(새 내용을 입력하세요. 비워두면 취소)")
                new_syllabus = input("> ")
                if new_syllabus:
                    course['syllabus'] = new_syllabus
                    common.save_courses()
                    print("강의 계획서가 저장되었습니다.")
                else:
                    print("취소되었습니다.")
                common.pause()
            
            elif choice == '2':
                self.manage_weekly_content(course)
            
            elif choice == '0':
                break

    def manage_weekly_content(self, course):
        """(신규) 주차별 학습 내용 관리 서브메뉴"""
        if 'weekly_content' not in course:
            course['weekly_content'] = []

        common.clear_screen()
        print(f"--- {course['title']} 주차별 내용 관리 ---")
        
        if not course['weekly_content']:
            print("등록된 내용이 없습니다.")
        else:
            for week_info in course['weekly_content']:
                print(f"- {week_info.get('week', 'N/A')}: {week_info.get('topic', 'N/A')}")
        
        print("\n1. 새 주차 내용 추가")
        print("2. 전체 초기화")
        print("0. 뒤로가기")
        choice = input("선택: ")
        
        if choice == '1':
            week = input("주차 (예: 1주차): ")
            topic = input("학습 내용: ")
            course['weekly_content'].append({'week': week, 'topic': topic})
            common.save_courses()
            print("추가되었습니다.")
        elif choice == '2':
            course['weekly_content'] = []
            common.save_courses()
            print("초기화되었습니다.")
        
        common.pause()

    def manage_attendance(self):
        """(신규) 2. 담당 강좌 출석 관리"""
        result = self._select_my_course("출석 관리")
        if not result: return
        
        course_id, course = result
        
        student_user_ids = course.get('student_user_ids', [])
        if not student_user_ids:
            print("수강생이 없어 출석을 관리할 수 없습니다."); common.pause(); return
            
        week = input("출석을 체크할 주차를 입력하세요 (예: 3주차): ")
        
        # 이 과목의 출석부가 없으면 생성
        if course_id not in data.attendance:
            data.attendance[course_id] = {}
            
        print(f"\n--- {week} 출석 체크 ---")
        print("(P: 출석, L: 지각, A: 결석, Enter: 스킵)")

        for student_user_id in student_user_ids:
            student = data.students.get(student_user_id)
            if not student: continue
            
            # 이 학생의 출석부가 없으면 생성
            if student_user_id not in data.attendance[course_id]:
                data.attendance[course_id][student_user_id] = {}
            
            current_status = data.attendance[course_id][student_user_id].get(week, 'N/A')
            
            status_input = input(f"- {student['name']} ({student['student_id']}) [현재: {current_status}]: ").upper()
            
            if status_input in ['P', 'L', 'A']:
                data.attendance[course_id][student_user_id][week] = status_input
            elif status_input == "":
                pass # 스킵
            else:
                print(" -> 잘못된 입력입니다. (P, L, A 중 하나)")

        common.save_attendance()
        print("\n출석부가 저장되었습니다.")
        common.pause()

    def manage_grades(self):
        """(수정) 3. 성적 관리"""
        result = self._select_my_course("성적 관리")
        if not result: return
        
        course_id, course = result
        student_user_ids = course.get('student_user_ids', [])

        if not student_user_ids:
            print("수강생이 없어 성적을 입력할 수 없습니다."); common.pause(); return
            
        print(f"\n--- [{course_id}] {course['title']} 성적 입력 ---")
        print("(A+, A0, B+, ..., F. Enter: 스킵)")

        grades_changed = False
        for student_user_id in student_user_ids:
            student = data.students.get(student_user_id)
            if not student: continue 

            student_grades = data.grades.get(student_user_id, {})
            current_grade = student_grades.get(course_id, '미입력')
            
            new_grade = input(f"- {student['name']} ({student['student_id']}) [현재: {current_grade}]: ").upper()
            
            if new_grade:
                if new_grade not in common.GRADE_TO_SCORE:
                    print(f" -> '{new_grade}'는 유효하지 않은 등급입니다. 스킵합니다.")
                    continue
                    
                if student_user_id not in data.grades:
                    data.grades[student_user_id] = {}
                
                data.grades[student_user_id][course_id] = new_grade
                print(f"  -> {new_grade}로 입력/수정 완료.")
                grades_changed = True

        if grades_changed:
            common.save_grades()
            print("\n성적 저장이 완료되었습니다.")
        else:
            print("\n성적 변경 사항이 없습니다.")
        common.pause()

    def view_students_in_course(self):
        """4. 강좌별 수강생 목록"""
        result = self._select_my_course("수강생 목록 조회")
        if not result: return
        
        course_id, course = result
        student_user_ids = course.get('student_user_ids', [])
        
        print(f"\n--- [{course_id}] {course['title']} 수강생 목록 ({len(student_user_ids)}명) ---")
        if not student_user_ids:
            print("수강생이 없습니다.")
        else:
            for student_user_id in student_user_ids:
                student = data.students.get(student_user_id)
                if student:
                    print(f"- {student['name']} ({student['student_id']}, {student['major']}) [학적: {student.get('status', 'N/A')}]")
        common.pause()