import tkinter as tk  # GUI 생성을 위한 tkinter 메인 모듈
from tkinter import messagebox  # 메시지 박스 (알림, 확인, 오류 창) 표시용
import data  # 전역 데이터 저장소 (users, students, courses 등)
import common_module as common  # 공통 기능 모듈 (데이터 로드/저장)
from student_najisoo import StudentMenu  # 학생용 메뉴 화면
from professor_jungjongbin import ProfessorMenu  # 교수용 메뉴 화면
from admin_imjihoo import AdminMenu  # 행정관리자용 메뉴 화면

# 로그인 창 클래스
class LoginWin: #사용자 역할별 로그인 창을 생성하고 관리하는 클래스
    def __init__(self, parent, role, theme_color):
        self.root = parent #parent: 부모 윈도우
        self.role = role #role: 사용자 역할 (student/professor/admin)
        self.theme_color = theme_color #theme_color: 역할별 테마 색상
        self.win = tk.Toplevel(parent)  # 새 창 생성
        self.win.title(f"{role.capitalize()} Login")
        self.win.geometry("400x400")
        self.win.configure(bg="white")

        header = tk.Frame(self.win, bg=self.theme_color, height=90) # 상단 헤더
        header.pack(fill="x")
        role_text = {"student": "학생", "professor": "교수", "admin": "행정"}.get(role, role)
        tk.Label(header, text=f"🔐 {role_text} 로그인", font=("맑은 고딕", 18, "bold"), 
                 bg=self.theme_color, fg="white").pack(expand=True)

        form_frame = tk.Frame(self.win, bg="white", padx=50, pady=30) # 로그인 폼
        form_frame.pack(fill="both", expand=True)
        # 아이디 입력 필드
        tk.Label(form_frame, text="아이디(ID)", bg="white", font=("맑은 고딕", 10, "bold"), fg="#555").pack(pady=(0, 5)) 
        self.ent_id = tk.Entry(form_frame, font=("맑은 고딕", 12), bg="#f0f2f5", relief="flat", justify="center")
        self.ent_id.pack(fill="x", ipady=8, pady=(0, 15))

        # 비밀번호 입력 필드
        tk.Label(form_frame, text="비밀번호(Password)", bg="white", font=("맑은 고딕", 10, "bold"), fg="#555").pack(pady=(0, 5))
        self.ent_pw = tk.Entry(form_frame, show="*", font=("맑은 고딕", 12), bg="#f0f2f5", relief="flat", justify="center")
        self.ent_pw.pack(fill="x", ipady=8, pady=(0, 25))

        # 로그인 버튼
        btn_login = tk.Button(form_frame, text="로그인", command=self.check_login,
                              bg=self.theme_color, fg="white", font=("맑은 고딕", 12, "bold"), 
                              relief="flat", cursor="hand2")
        btn_login.pack(fill="x", ipady=10)
        
        self.ent_id.focus() # 아이디 입력 필드에 포커스 설정
        self.win.bind("<Return>", lambda event: self.check_login()) # Enter 키로 로그인 가능하도록 설정

    def check_login(self):
        """로그인 정보 검증 및 해당 역할의 메뉴 화면으로 이동"""
        # 입력된 아이디와 비밀번호 가져오기
        uid = self.ent_id.get().strip()
        pw = self.ent_pw.get().strip()
        
        # 아이디 존재 여부 확인
        if uid not in data.users:
            messagebox.showerror("오류", "존재하지 않는 아이디입니다.")
            return
        
        # 사용자 정보 가져오기
        user = data.users[uid]
        
        # 역할 권한 확인
        if user["role"] != self.role:
            messagebox.showerror("오류", "접근 권한이 없습니다.")
            return
        
        # 비밀번호 일치 확인
        if str(user["password"]) != pw:
            messagebox.showerror("오류", "비밀번호가 일치하지 않습니다.")
            return
        
        # 로그인 성공: 로그인 창 닫고 해당 역할의 메뉴 화면 열기
        self.win.destroy()
        if self.role == "student": StudentMenu(self.root, uid)
        elif self.role == "professor": ProfessorMenu(self.root, uid)
        elif self.role == "admin": AdminMenu(self.root, uid)

# 메인 윈도우 클래스
class MainWin:
    """프로그램의 메인 화면을 생성하고 관리하는 클래스"""
    
    def __init__(self):
        """메인 윈도우 초기화"""
        # 메인 윈도우 생성 및 설정
        self.win = tk.Tk()
        self.win.title("대학 종합정보시스템")
        self.win.geometry("900x550")
        self.win.configure(bg="#f8f9fa")

        # 모든 데이터 파일 로드
        common.load_all_data()
        # UI 구성
        self.setup_ui()

    def setup_ui(self):
        """메인 화면 UI 구성"""
        # 상단 타이틀 영역
        title_frame = tk.Frame(self.win, bg="white", pady=40, highlightthickness=1, highlightbackground="#eee")
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="🏛️ 대학 종합정보시스템", font=("맑은 고딕", 26, "bold"), 
                 bg="white", fg="#222").pack()
        tk.Label(title_frame, text="                        JJU INFORMATION SYSTEM", 
                 font=("맑은 고딕", 10, "bold"), bg="white", fg="#999").pack(pady=(5, 0))

        # 버튼 영역
        self.btn_frame = tk.Frame(self.win, bg="#f8f9fa")
        self.btn_frame.pack(expand=True)

        # 역할별 박스 정보 정의 (역할, 제목, 설명, 색상)
        roles = [
            ("student", "👨‍🎓 학생 서비스", "수강신청 / 성적조회\n학적현황 확인", "#0086c5"),
            ("professor", "👩‍🏫 교수 서비스", "강의 정보 관리\n학생 성적 및 출결", "#003366"),
            ("admin", "🏛️ 행정 서비스", "전체 학사 행정\n시스템 통합 관리", "#0056b3")
        ]

        # 각 역할별 박스 생성
        for role, title, desc, color in roles:
            self.create_role_card(self.btn_frame, role, title, desc, color)

    def create_role_card(self, parent, role, title, desc, color):
        # 박스 프레임 생성
        card = tk.Frame(parent, bg="white", width=250, height=220, padx=20, pady=25, 
                        highlightthickness=1, highlightbackground="#dee2e6")
        card.pack(side="left", padx=15)
        card.pack_propagate(False)  # 고정 크기 유지

        # 박스 제목
        tk.Label(card, text=title, font=("맑은 고딕", 15, "bold"), 
                 bg="white", fg=color).pack(pady=(0, 15))
        
        # 박스 설명
        tk.Label(card, text=desc, font=("맑은 고딕", 10), bg="white", fg="#666", 
                 justify="center", wraplength=200).pack(expand=True)

        # 로그인 버튼
        btn = tk.Button(card, text="로그인하기", font=("맑은 고딕", 10, "bold"), 
                        bg=color, fg="white", relief="flat", cursor="hand2", width=15,
                        command=lambda r=role, c=color: self.open_login(r, c))
        btn.pack(pady=(15, 0), ipady=5)
        
        # 마우스 효과
        card.bind("<Enter>", lambda e: card.config(bg="#f1f3f5"))  # 마우스 올렸을 때
        card.bind("<Leave>", lambda e: card.config(bg="white"))    # 마우스 뗐을 때

    def open_login(self, role, color):
        LoginWin(self.win, role, color)

# 프로그램 실행
if __name__ == "__main__":
    app = MainWin()  # 메인 윈도우 생성
    app.win.mainloop()  # 이벤트 루프 시작