class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Student(User):
    def __init__(self, user_id, name, major, status="재학"):
        super().__init__(user_id, name)
        self.major = major
        self.status = status

class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def update_student_status(self, student: Student, new_status: str):
        allowed = ["재학", "휴학", "복학", "자퇴", "졸업"]
        if new_status not in allowed:
            print(f"오류 '{new_status}' 는 허용되지 않는 학적 상태입니다.")
            return

        old_status = student.status
        student.status = new_status

        print(f"학적 처리 완료")
        print(f"학생: {student.name} ({student.user_id})")
        print(f"이전 학적: {old_status} → 변경된 학적: {new_status}")

    def change_student_major(self, student: Student, new_major: str):
        old_major = student.major
        student.major = new_major

        print(f"전공 변경 완료")
        print(f"{student.name} 학생 전공: {old_major} → {new_major}")

    def delete_student(self, student_list: dict, student_id: str):
        if student_id in student_list:
            del student_list[student_id]
            print(f"삭제 완료 {student_id} 학생 정보가 삭제되었습니다.")
        else:
            print("오류 해당 학생 ID가 존재하지 않습니다.")

    def register_student(self, student_list: dict, student: Student):
        if student.user_id in student_list:
            print("오류 이미 존재하는 학생 ID입니다.")
            return
        
        student_list[student.user_id] = student
        print(f"등록 완료 {student.name} 학생이 학사에 등록되었습니다.")



#실행 확인

student_db = {}

admin = Admin("admin01", "행정조교 정종빈")

s1 = Student("2025001", "임지후", "컴퓨터공학")
s2 = Student("2025002", "최혁", "전자공학")

admin.register_student(student_db, s1)
admin.register_student(student_db, s2)

admin.update_student_status(s1, "휴학")
admin.update_student_status(s2, "졸업")

admin.change_student_major(s1, "AI학과")

admin.delete_student(student_db, "2025002")
