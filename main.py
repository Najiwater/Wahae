# main.py
from student import Student
from professor import Professor
from admin import Admin
from data import users, courses, notices, next_notice_id


# ------------------------------
# 초기 데이터 생성
# ------------------------------
def init_data():
    # 학생
    s1 = Student("s1001", "1234", "홍길동", "AI학과", 1)
    s2 = Student("s1002", "1111", "김학생", "AI학과", 1)

    # 교수
    p1 = Professor("p2001", "abcd", "김교수", "AI학과")

    # 조교
    a1 = Admin("a3001", "9999", "행정조교", "학사팀")

    # 저장
    users[s1.id] = s1
    users[s2.id] = s2
    users[p1.id] = p1
    users[a1.id] = a1

    # 강의 샘플
    courses["C001"] = {
        "name": "파이썬기초",
        "professor_id": "p2001",
        "max_students": 30,
        "time": "월3,4",
        "students": ["s1001"]
    }

    s1.courses.append("C001")
    s1.grades["C001"] = "A+"
    p1.courses.append("C001")


# ------------------------------
# 공지 조회 (학생/교수에서 사용)
# ------------------------------
def show_notices():
    if not notices:
        print("\n공지 없음\n")
        return

    print("\n=== 공지사항 ===")
    for n in notices:
        writer = users[n["writer_id"]].name
        print(f"[{n['id']}] {n['title']} - {writer}")
    print()


# ------------------------------
# 로그인
# ------------------------------
def login():
    uid = input("ID: ")
    pw = input("PW: ")

    user = users.get(uid)
    if not user or user.pw != pw:
        print("로그인 실패\n")
        return None

    print(f"\n{user.name}님 환영합니다!\n")
    return user


# ------------------------------
# 메인 루프
# ------------------------------
def main():
    init_data()

    while True:
        print("============================")
        print("  역할 기반 학사관리 시스템")
        print("============================")
        print("1. 로그인")
        print("0. 종료")
        cmd = input(">> ")

        if cmd == "0":
            print("프로그램 종료.")
            break

        if cmd == "1":
            user = login()
            if not user:
                continue

            user.menu()   # 🔥 핵심: 역할별 menu() 자동 실행


if __name__ == "__main__":
    main()
