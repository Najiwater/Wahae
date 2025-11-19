class Professor:
    def __init__(self, name):
        self.name = name
        self.courses = {}
        self.students = {}
        self.announcements = []

    # 강의 개설 및 관리 기능
    def create_course(self, course_id, course_info):
        self.courses[course_id] = {
            "info": course_info,
            "grades": {},
            "attendance": {},
            "syllabus": None,
        }

    # 학생 성적 입력 및 수정
    def set_grade(self, course_id, student_id, grade):
        if course_id in self.courses:
            self.courses[course_id]["grades"][student_id] = grade

    # 강의 계획서 관리
    def set_syllabus(self, course_id, syllabus_text):
        if course_id in self.courses:
            self.courses[course_id]["syllabus"] = syllabus_text

    # 출석 관리 시스템
    def record_attendance(self, course_id, student_id, status):
        if course_id in self.courses:
            self.courses[course_id]["attendance"].setdefault(student_id, []).append(status)

    # 학생 정보 조회 기능
    def get_student_info(self, student_id):
        return self.students.get(student_id, "No data available")

    # 공지사항 등록 기능
    def add_announcement(self, message):
        self.announcements.append(message)

# Example usage
if __name__ == "__main__":
    prof = Professor("장현준")
    prof.create_course("CS101", "기초 프로그래밍 강의")
    prof.set_syllabus("CS101", "1주차: Python 기본 문법 ...")
    prof.add_announcement("중간고사 공지: 10월 20일")