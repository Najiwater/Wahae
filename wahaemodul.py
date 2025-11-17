# academic_manager.py

class User:
    """
    모든 사용자의 기본이 되는 부모 클래스
    (공통 기능: 공지 게시판 조회, 내 정보 관리)
    """
    def __init__(self, user_id, name, user_type):
        self.user_id = user_id
        self.name = name
        self.user_type = user_type
        print(f"[{self.user_type}] {self.name}님, 시스템에 오신 것을 환영합니다.")

    def view_notice_board(self):
        """ 공지 게시판 조회 """
        print(f"\n--- {self.name}님이 [공지 게시판]을 조회합니다 ---")
        print("  [공지] 1. 2025학년도 2학기 수강신청 안내")
        print("  [공지] 2. 도서관 이용 시간 변경")
        print("----------------------------------------")

    def manage_my_info(self):
        """ 내 정보 관리 """
        print(f"\n--- {self.name}님의 [내 정보 관리] ---")
        print(f"  ID: {self.user_id}")
        print(f"  이름: {self.name}")
        print(f"  유형: {self.user_type}")
        print("  (정보 수정 기능은 여기에 구현...)")
        print("----------------------------------------")


class Student(User):
    """
    학생 클래스 (User 클래스 상속)
    (고유 기능: 수강 조회, 성적 확인, 시간표/공지)
    """
    def __init__(self, user_id, name, major):
        super().__init__(user_id, name, "학생")
        self.major = major
        self.courses = {"CS101": "자료구조", "MATH101": "미적분학"}
        self.grades = {"CS101": "A+", "MATH101": "B0"}

    def check_enrollment(self):
        """ 수강 조회 """
        print(f"\n--- {self.name} 학생의 [수강 조회] ---")
        if not self.courses:
            print("  수강 중인 과목이 없습니다.")
        else:
            for course_id, title in self.courses.items():
                print(f"  - {course_id}: {title}")
        print("----------------------------------------")

    def check_grades(self):
        """ 성적 확인 """
        print(f"\n--- {self.name} 학생의 [성적 확인] ---")
        if not self.grades:
            print("  입력된 성적이 없습니다.")
        else:
            for course_id, grade in self.grades.items():
                title = self.courses.get(course_id, "과목명 불명")
                print(f"  - [{title}] 성적: {grade}")
        print("----------------------------------------")

    def check_timetable(self):
        """ 시간표/공지 확인 (다이어그램상 '시간표/공지') """
        print(f"\n--- {self.name} 학생의 [시간표 확인] ---")
        # 실제로는 self.courses를 기반으로 시간표 데이터를 조회
        print("  [월 1-2교시] 자료구조 (CS101)")
        print("  [화 3-4교시] 미적분학 (MATH101)")
        print("  (공지사항은 '공지 게시판 조회' 기능을 사용하세요.)")
        print("----------------------------------------")


class Professor(User):
    """
    교수 클래스 (User 클래스 상속)
    (고유 기능: 강의 관리)
    """
    def __init__(self, user_id, name, department):
        super().__init__(user_id, name, "교수")
        self.department = department
        self.teaching_courses = ["CS101"]

    def manage_lecture(self):
        """ 강의 관리 """
        print(f"\n--- {self.name} 교수님의 [강의 관리] ---")
        print(f"  담당 학과: {self.department}")
        print(f"  담당 강의: {self.teaching_courses}")
        print("  1. 출결 관리")
        print("  2. 성적 입력")
        print("  3. 과제 관리")
        print("  (세부 기능은 여기에 구현...)")
        print("----------------------------------------")


class AdminAssistant(User):
    """
    행정 조교 클래스 (User 클래스 상속)
    (고유 기능: 학적 처리)
    """
    def __init__(self, user_id, name, office):
        super().__init__(user_id, name, "행정 조교")
        self.office = office

    def process_academic_record(self, student_name, action):
        """ 학적 처리 """
        print(f"\n--- {self.name} 조교의 [학적 처리] ---")
        print(f"  소속: {self.office}")
        print(f"  처리 대상: {student_name}")
        print(f"  처리 내용: {action}")
        print(f"  > '{student_name}' 학생의 '{action}' 처리가 완료되었습니다.")
        print("----------------------------------------")