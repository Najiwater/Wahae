# student_class.py
import data
import common_module as common
from datetime import datetime



class Student:
    def __init__(self, user_id):
        self.user_id = user_id
        self.info = data.students[user_id] 

    def student_menu(self):
        while True:
            common.clear_screen()
            print(f"--- 학생 메뉴 ({self.info['name']}님 | {self.info['status']}) ---")
            print("1. 수강 신청 (시간 충돌 감지)")
            print("2. 수강 철회")
            print("3. 내 시간표/수강과목 조회")
            print("4. 강의 상세 조회 (계획서, 주차별 내용)")
            print("5. 성적 조회 (GPA 계산)")
            print("6. 학적 변동 신청 (휴학 등)")
            print("7. 공지사항 조회")
            print("8. 내 정보 조회/수정 (비밀번호 변경)")
            print("0. 로그아웃")
            choice = input("메뉴 선택: ")

            if choice == '1': self.register_course()
            elif choice == '2': self.drop_course()
            elif choice == '3': self.view_my_timetable()
            elif choice == '4': self.view_course_details()
            elif choice == '5': self.view_grades()
            elif choice == '6': self.request_academic_change()
            elif choice == '7': common.view_notices()
            elif choice == '8': self.my_profile_menu()
            elif choice == '0': print("로그아웃합니다."); common.pause(); break
            else: print("잘못된 입력입니다."); common.pause()

    def my_profile_menu(self):
        common.clear_screen()
        print("--- 내 정보 관리 ---")
        print(f"이름: {self.info['name']}")
        print(f"학번: {self.info['student_id']}")
        print(f"전공: {self.info['major']}")
        print(f"학적: {self.info['status']}")
        print("\n1. 비밀번호 변경")
        print("0. 뒤로가기")
        choice = input("선택: ")
        if choice == '1':
            common.change_password(self.user_id)
        else:
            return

    def _get_course_display_list(self, course_id_list):
        """과목 ID 리스트를 받아 보기 좋은 문자열 리스트로 반환"""
        display_list = []
        if not course_id_list:
            return display_list, False
            
        for cid in course_id_list:
            course = data.courses.get(cid)
            if not course:
                display_list.append(f"[{cid}] (삭제된 과목)")
                continue
                
            prof_name = data.professors.get(course['professor_user_id'], {}).get('name', 'N/A')
            time_info = course.get('time', {})
            time_str = f"{time_info.get('day', 'N/A')} {time_info.get('start', '')}-{time_info.get('end', '')}"
            display_list.append(f"[{cid}] {course['title']} (교수: {prof_name} | 시간: {time_str})")
        return display_list, True

    def register_course(self):
        common.clear_screen()
        print("--- 수강 신청 ---")
        
        # 1. 전체 강좌 목록 표시
        print("--- 전체 개설 강좌 ---")
        all_course_ids = list(data.courses.keys())
        display_list, has_courses = self._get_course_display_list(all_course_ids)
        if not has_courses:
            print("개설된 강좌가 없습니다."); common.pause(); return

        for item in display_list:
            course_id = item.split(']')[0][1:]
            course = data.courses[course_id]
            current_count = len(course['student_user_ids'])
            max_cap = course.get('max_capacity', 'N/A')
            print(f"{item} [정원: {current_count}/{max_cap}]")
        
        print("-" * 20)
        course_id = input("수강 신청할 과목 코드를 입력하세요: ").upper()
        course = data.courses.get(course_id)

        # 2. 유효성 검사
        if not course: print("존재하지 않는 과목 코드입니다.")
        elif course_id in self.info['courses']: print("이미 수강 중인 과목입니다.")
        elif len(course['student_user_ids']) >= course.get('max_capacity', float('inf')): print("수강 인원이 마감되었습니다.")
        # 3. (신규) 시간표 충돌 검사
        elif common.check_time_conflict(self.info['courses'], course_id):
            print("시간표가 겹쳐 수강 신청할 수 없습니다.")
        else:
            # 4. 수강 신청 처리
            self.info['courses'].append(course_id)
            course['student_user_ids'].append(self.user_id)
            common.save_students(); common.save_courses()
            print(f"[{course_id}] {course['title']} 과목 수강 신청이 완료되었습니다.")
        
        common.pause()

    def drop_course(self):
        common.clear_screen()
        print("--- 수강 철회 ---")
        
        display_list, has_courses = self._get_course_display_list(self.info['courses'])
        if not has_courses:
            print("수강 중인 과목이 없습니다."); common.pause(); return
            
        for item in display_list: print(item)
        print("-" * 20)
        course_id = input("수강 철회할 과목 코드를 입력하세요: ").upper()

        if course_id not in self.info['courses']:
            print("수강 중인 과목이 아닙니다.")
        else:
            course = data.courses.get(course_id)
            self.info['courses'].remove(course_id)
            if course and self.user_id in course['student_user_ids']:
                course['student_user_ids'].remove(self.user_id)
            
            common.save_students(); common.save_courses()
            print(f"[{course_id}] {course['title'] if course else ''} 과목 수강 철회가 완료되었습니다.")
        
        common.pause()

    def view_my_timetable(self):
        """(신규) 3. 내 시간표/수강과목 조회"""
        common.clear_screen()
        print(f"--- {self.info['name']}님 시간표/수강과목 ---")
        
        display_list, has_courses = self._get_course_display_list(self.info['courses'])
        if not has_courses:
            print("수강 중인 과목이 없습니다.")
        else:
            for item in display_list:
                print(item)
        common.pause()
        
    def view_course_details(self):
        """(신규) 4. 강의 상세 조회 (계획서, 주차별 내용)"""
        common.clear_screen()
        print("--- 강의 상세 조회 ---")
        
        display_list, has_courses = self._get_course_display_list(self.info['courses'])
        if not has_courses:
            print("수강 중인 과목이 없습니다."); common.pause(); return
            
        for item in display_list: print(item)
        print("-" * 20)
        course_id = input("상세 조회할 과목 코드를 입력하세요: ").upper()
        
        if course_id not in self.info['courses']:
            print("수강 중인 과목이 아닙니다."); common.pause(); return

        course = data.courses[course_id]
        common.clear_screen()
        print(f"--- [{course_id}] {course['title']} 상세 정보 ---")
        
        # 1. 강의 계획서
        print("\n[강의 계획서]")
        print(course.get('syllabus', '등록된 강의 계획서가 없습니다.'))
        
        # 2. 주차별 학습 내용
        print("\n[주차별 학습 내용]")
        weekly_content = course.get('weekly_content', [])
        if not weekly_content:
            print("등록된 주차별 학습 내용이 없습니다.")
        else:
            for week_info in weekly_content:
                print(f"- {week_info.get('week', 'N/A')}: {week_info.get('topic', 'N/A')}")
        
        # 3. (보너스) 출석 현황
        print("\n[내 출석 현황]")
        my_attendance = data.attendance.get(course_id, {}).get(self.user_id, {})
        if not my_attendance:
            print("출석 정보가 없습니다.")
        else:
            for week, status in my_attendance.items():
                print(f"- {week}: {status}")
                
        common.pause()

    def view_grades(self):
        """(수정) 5. 성적 조회 (GPA 계산)"""
        common.clear_screen()
        print("--- 성적 조회 ---")
        
        my_grades = data.grades.get(self.user_id, {})
        if not my_grades:
            print("조회할 수 있는 성적이 없습니다."); common.pause(); return

        print(f"--- {self.info['name']}님 성적표 ---")
        
        total_credits = 0.0
        total_score_points = 0.0
        
        for course_id, grade in my_grades.items():
            course = data.courses.get(course_id)
            course_title = course.get('title', '삭제된 과목') if course else '삭제된 과목'
            credits = course.get('credits', 0.0) if course else 0.0
            
            score = common.GRADE_TO_SCORE.get(grade, 0.0)
            
            print(f"[{course_id}] {course_title} (학점: {credits}) - 성적: {grade}")
            
            if grade != 'F' and credits > 0: # F학점은 총 학점에 포함되나, GPA 계산에는 다를 수 있음. 여기선 F도 포함.
                total_credits += credits
                total_score_points += (score * credits)

        if total_credits > 0:
            gpa = total_score_points / total_credits
            print("\n------------------------------")
            print(f"총 이수 학점: {total_credits}")
            print(f"전체 평균 학점 (GPA): {gpa:.2f} / 4.5")
        else:
            print("\n이수 내역이 없어 GPA를 계산할 수 없습니다.")
            
        common.pause()

    def request_academic_change(self):
        """(신규) 6. 학적 변동 신청"""
        common.clear_screen()
        print("--- 학적 변동 신청 ---")
        print("1. 휴학 신청")
        print("2. 복학 신청")
        print("3. 자퇴 신청")
        print("0. 뒤로가기")
        choice = input("선택: ")

        req_type = ""
        if choice == '1': req_type = "휴학"
        elif choice == '2': req_type = "복학"
        elif choice == '3': req_type = "자퇴"
        else: return

        reason = input(f"{req_type} 사유를 입력하세요: ")
        
        # 새 요청 ID 생성 (간단하게 현재 시간 사용)
        req_id = f"R{int(datetime.now().timestamp())}"
        
        new_request = {
            'req_id': req_id,
            'student_user_id': self.user_id,
            'student_name': self.info['name'],
            'type': req_type,
            'reason': reason,
            'status': 'pending' # 'pending', 'approved', 'rejected'
        }
        
        data.academic_requests.append(new_request)
        common.save_academic_requests()
        
        print(f"{req_type} 신청이 완료되었습니다. (관리자 승인 대기)")
        common.pause()