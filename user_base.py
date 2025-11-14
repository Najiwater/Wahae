# user_base.py
class User:
    def __init__(self, user_id, pw, name, role):
        self.id = user_id
        self.pw = pw
        self.name = name
        self.role = role

    def edit_profile(self):
        print("\n=== 내 정보 수정 ===")
        new_name = input(f"새 이름(현재: {self.name}, 엔터 유지): ")
        if new_name.strip():
            self.name = new_name

        new_pw = input(f"새 비밀번호(현재: {self.pw}, 엔터 유지): ")
        if new_pw.strip():
            self.pw = new_pw

        print("정보 수정 완료!\n")
