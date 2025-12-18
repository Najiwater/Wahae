import tkinter as tk
from tkinter import messagebox, ttk
import data
import common_module as common

class StudentMenu: # 학생용 메뉴 화면 클래스
    def __init__(self, parent, user_id):
        self.user_id = user_id
        self.win = tk.Toplevel(parent)
        self.win.title(f"학생 정보 시스템 - {user_id}")
        self.win.geometry("1100x800")
        
        self.primary_color = "#0086c5"  # 테마 색상
        self.setup_ui()

    def setup_ui(self):# 학생 이름 및 학번 표시
        header = tk.Frame(self.win, bg=self.primary_color, height=60)
        header.pack(fill="x")
        s_info = data.students.get(self.user_id, {})
        tk.Label(header, text=f"🎓 {s_info.get('name', '학생')}님, 환영합니다 (학번: {s_info.get('student_id')})", 
                 fg="white", bg=self.primary_color, font=("맑은 고딕", 13, "bold")).pack(side="left", padx=20, pady=15)

        self.main_frame = tk.Frame(self.win, bg="#f4f7f6") # 메인 레이아웃
        self.main_frame.pack(fill="both", expand=True)

        sidebar = tk.Frame(self.main_frame, bg="white", width=220) # 왼쪽 메뉴 버튼
        sidebar.pack(side="left", fill="y", padx=1, pady=1)
        sidebar.pack_propagate(False)  # 고정 너비 유지
        
        menus = [
            ("🏠 마이 대시보드", self.show_dashboard),
            ("📢 공지사항 확인", self.show_notice_view),
            ("📊 성적 조회", self.show_grade_view),
            ("📅 출결 현황", self.show_attendance_view),
            ("📝 학적 변동 신청", self.show_request_view)
        ] # 메뉴 항목 정의
        
        # 메뉴 버튼 생성
        for text, cmd in menus:
            tk.Button(sidebar, text=text, font=("맑은 고딕", 11), bg="white", relief="flat",
                      anchor="w", padx=25, pady=18, command=cmd).pack(fill="x")

        # 오른쪽 주요 컨텐츠 표시 영역
        self.content_area = tk.Frame(self.main_frame, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # 기본으로 대시보드 표시
        self.show_dashboard()

    # 평균 학점 계산 추가
    def show_dashboard(self):
        """대시보드 화면 표시 - 학사 요약 정보 표시"""
        # 기존 컨텐츠 제거
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="🔔 학사 요약 현황", font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        # 학생 정보 가져오기
        s = data.students.get(self.user_id, {})
        
        # 학점 등급별 평균 학점 계산 로직
        grade_map = {
            "A+": 4.5, "A0": 4.0, "B+": 3.5, "B0": 3.0, 
            "C+": 2.5, "C0": 2.0, "D+": 1.5, "D0": 1.0, "F": 0.0
        }
        
        total_points = 0.0   # 총 학점 점수
        total_credits = 0    # 총 이수 학점
        my_grades = data.grades.get(self.user_id, {})
        
        # 모든 수강 과목 순회하며 평균 계산
        for cid, info in data.courses.items():
            if self.user_id in info.get('student_user_ids', []):
                letter_grade = my_grades.get(info['title'])
                if letter_grade and letter_grade in grade_map:
                    credit = info.get('credits', 0)
                    total_points += (grade_map[letter_grade] * credit)  # (학점 * 학점수)
                    total_credits += credit
        
        # 평균 학점 계산 (GPA)
        gpa = total_points / total_credits if total_credits > 0 else 0.0
        # ------------------------

        # 통계 카드 프레임
        stats_frame = tk.Frame(self.content_area, bg="white")
        stats_frame.pack(fill="x")

        # 카드 정보 (제목, 값, 색상)
        info_cards = [
            ("현재 학적", s.get('status', '재학'), "#0086c5"),
            ("평균 학점", f"{gpa:.2f} / 4.5", "#ff5722"), # 신규 추가
            ("이수 학점", f"{total_credits} / 130", "#28a745"),
            ("AHA 이수율", f"{s.get('aha_progress', 0)}%", "#6f42c1"),
        ]

        # 각 박스 생성
        for title, val, color in info_cards:
            card = tk.Frame(stats_frame, bg="#f8f9fa", highlightthickness=1, highlightbackground="#dee2e6", width=180, height=100)
            card.pack(side="left", padx=8); card.pack_propagate(False)
            tk.Label(card, text=title, bg="#f8f9fa", font=("맑은 고딕", 10)).pack(pady=(15, 5))
            tk.Label(card, text=val, bg="#f8f9fa", font=("맑은 고딕", 13, "bold"), fg=color).pack()

        # 최근 공지 요약 표시
        tk.Label(self.content_area, text="📢 최근 공지사항", font=("맑은 고딕", 13, "bold"), bg="white").pack(anchor="w", pady=(30, 10))
        n_box = tk.Frame(self.content_area, bg="#fffbe6", padx=15, pady=15, highlightthickness=1, highlightbackground="#ffe58f")
        n_box.pack(fill="x")
        
        # 공지사항 표시 (최대 3개)
        if not data.notices:
            tk.Label(n_box, text="등록된 공지가 없습니다.", bg="#fffbe6").pack()
        else:
            for n in data.notices[:3]:
                tk.Label(n_box, text=f"• {n}", bg="#fffbe6", font=("맑은 고딕", 10)).pack(anchor="w", pady=2)

    # 공지사항, 성적조회, 출결현황, 학적신청 로직 기존 유지
    def show_notice_view(self):
        """공지사항 전체 목록 표시 - Treeview로 공지 목록 표시"""
        # 기존 컨텐츠 제거
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="📢 전체 공지사항", font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        tk.Label(self.content_area, text="* 제목을 더블 클릭하면 상세 내용을 볼 수 있습니다.", font=("맑은 고딕", 9), bg="white", fg="gray").pack(anchor="w")

        # 공지사항 목록 Treeview 생성
        self.notice_tree = ttk.Treeview(self.content_area, columns=("번호", "제목"), show="headings", height=15)
        self.notice_tree.heading("번호", text="No."); self.notice_tree.column("번호", width=60, anchor="center")
        self.notice_tree.heading("제목", text="공지 제목"); self.notice_tree.column("제목", width=700, anchor="w")
        self.notice_tree.pack(fill="both", expand=True)

        # 데이터 삽입 (제목만 추출)
        for i, n in enumerate(data.notices):
            title = n.split('] ')[0].replace('[', '') if '] ' in n else n
            self.notice_tree.insert("", "end", values=(len(data.notices)-i, title), tags=(n,))

        # 더블 클릭 이벤트 바인딩 - 상세보기 기능
        self.notice_tree.bind("<Double-1>", self.open_notice_detail)

    def open_notice_detail(self, event):
        # 선택된 항목 가져오기
        selected_item = self.notice_tree.selection()
        if not selected_item: return
        
        # 전체 텍스트 추출
        full_text = self.notice_tree.item(selected_item, "tags")[0]
        title = full_text.split('] ')[0].replace('[', '') if '] ' in full_text else "공지사항"
        content = full_text.split('] ')[1] if '] ' in full_text else full_text

        # 상세 보기 팝업
        detail_win = tk.Toplevel(self.win)
        detail_win.title("공지사항 상세보기")
        detail_win.geometry("500x400")
        detail_win.configure(bg="white")

        # 제목 표시
        tk.Label(detail_win, text=f"📌 {title}", font=("맑은 고딕", 14, "bold"), bg="white", wraplength=450).pack(pady=20)
        
        # 내용 표시 (읽기 전용)
        txt_area = tk.Text(detail_win, font=("맑은 고딕", 11), bg="#f8f9fa", relief="flat", padx=10, pady=10)
        txt_area.insert("1.0", content)
        txt_area.config(state="disabled") # 읽기 전용
        txt_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def show_grade_view(self):
        """성적 조회 화면 표시 - 과목별 성적 등급 표시"""
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="📊 과목별 성적 조회", font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        # 성적 Treeview 생성
        tree = ttk.Treeview(self.content_area, columns=("과목명", "이수학점", "성적등급"), show="headings")
        for col in ("과목명", "이수학점", "성적등급"):
            tree.heading(col, text=col); tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)
        
        # 내 성적 데이터 가져오기
        my_grades = data.grades.get(self.user_id, {})
        
        # 수강 과목 목록 표시
        for cid, info in data.courses.items():
            if self.user_id in info.get('student_user_ids', []):
                grade = my_grades.get(info['title'], "미입력")
                tree.insert("", "end", values=(info['title'], info['credits'], grade))

    def show_attendance_view(self):
        """출결 현황 화면 표시 - 과목별 출석/지각/결석 통계 표시"""
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="📅 과목별 출결 현황", font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        # 출결 Treeview 생성
        cols = ("과목명", "출석", "지각", "결석")
        tree = ttk.Treeview(self.content_area, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150 if col == "과목명" else 100, anchor="center")
        tree.pack(fill="both", expand=True)
        
        # 과목별 출결 통계
        for cid, info in data.courses.items():
            if self.user_id in info.get('student_user_ids', []):
                att_record = data.attendance.get(cid, {}).get(self.user_id, [])
                p, t, a = att_record.count("출석"), att_record.count("지각"), att_record.count("결석")
                tree.insert("", "end", values=(info['title'], f"{p}회", f"{t}회", f"{a}회"))

    def show_request_view(self):
        """학적 변동 신청 화면 표시 - 휴학/복학/자퇴 신청 및 현황 확인"""
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="📝 학적 변동 신청", font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        
        # 신청 폼 영역
        form_f = tk.LabelFrame(self.content_area, text="신규 신청", bg="white", padx=15, pady=15)
        form_f.pack(fill="x", pady=(0, 20))
        
        tk.Label(form_f, text="신청 유형 선택:", bg="white").pack(side="left", padx=10)
        type_var = tk.StringVar(value="휴학")
        ttk.Combobox(form_f, textvariable=type_var, values=["휴학", "복학", "자퇴"], state="readonly").pack(side="left", padx=10)
        
        # 신청 제출 버튼
        tk.Button(form_f, text="신청 제출", bg=self.primary_color, fg="white", padx=20,
                  command=lambda: self.submit_request(type_var.get())).pack(side="left", padx=20)
        
        # 신청 현황 Treeview
        self.req_tree = ttk.Treeview(self.content_area, columns=("유형", "상태"), show="headings")
        for col in ("유형", "상태"):
            self.req_tree.heading(col, text=col); self.req_tree.column(col, anchor="center")
        self.req_tree.pack(fill="both", expand=True)
        
        # 신청 목록 표시
        self.refresh_requests()

    def submit_request(self, req_type):
        """학적 변동 신청 제출
        
        Args:
            req_type: 신청 유형 (휴학/복학/자퇴)
        """
        # 신청 데이터 추가
        data.academic_requests.append({"student_id": self.user_id, "type": req_type, "status": "대기"})
        # 파일에 저장
        common.save_data("academic_requests.json", data.academic_requests)
        
        messagebox.showinfo("완료", f"{req_type} 신청이 완료되었습니다.")
        # 화면 새로고침
        self.refresh_requests()

    def refresh_requests(self):
        """학적 변동 신청 목록 새로고침"""
        # 기존 목록 제거
        self.req_tree.delete(*self.req_tree.get_children())
        
        # 내 신청만 표시
        for req in data.academic_requests:
            if req['student_id'] == self.user_id:
                self.req_tree.insert("", "end", values=(req['type'], req['status']))