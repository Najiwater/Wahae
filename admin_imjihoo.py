import tkinter as tk
from tkinter import messagebox, ttk
import data
import common_module as common

class AdminMenu: # 행정 관리자용 메뉴 화면 클래스
    def __init__(self, parent, user_id):
        self.user_id = user_id
        self.win = tk.Toplevel(parent)
        self.win.title("행정 관리 시스템 - 관리자 모드")
        self.win.geometry("1100x850")
        
        self.primary_color = "#0056b3"  # 테마 색상
        self.setup_ui()

    def setup_ui(self): # 관리자 메뉴 UI 구성
        # 상단 헤더
        header = tk.Frame(self.win, bg=self.primary_color, height=60)
        header.pack(fill="x")
        tk.Label(header, text="🏛️ 대학 행정 관리 포털", fg="white", bg=self.primary_color, 
                 font=("맑은 고딕", 15, "bold")).pack(side="left", padx=20, pady=15)
        # 메인 레이아웃
        self.main_frame = tk.Frame(self.win, bg="#f4f7f6")
        self.main_frame.pack(fill="both", expand=True)
        # 왼쪽 메뉴 버튼
        sidebar = tk.Frame(self.main_frame, bg="white", width=220)
        sidebar.pack(side="left", fill="y", padx=1, pady=1)
        sidebar.pack_propagate(False)  # 고정 너비 유지
        
        # 메뉴 항목 정의
        menus = [
            ("🏠 관리 대시보드", self.show_dashboard),
            ("👥 학생 명단 관리", self.show_student_mgmt),
            ("📝 학적 변동 승인", self.show_request_mgmt),
            ("📢 공지사항 관리", self.show_notice_mgmt)
        ]
        
        # 메뉴 버튼 생성
        for text, cmd in menus:
            tk.Button(sidebar, text=text, font=("맑은 고딕", 11), bg="white", relief="flat",
                      anchor="w", padx=25, pady=18, command=cmd).pack(fill="x")

        # 주요 컨텐츠 표시 영역
        self.content_area = tk.Frame(self.main_frame, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True, padx=25, pady=25)
        
        # 기본으로 표시
        self.show_dashboard()

    # 관리
    def show_dashboard(self):
        for widget in self.content_area.winfo_children(): widget.destroy()
        tk.Label(self.content_area, text="📊 학사 통계 요약", font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 20))
        total = len(data.students)
        on = sum(1 for s in data.students.values() if s.get('status') == '재학')
        stats_f = tk.Frame(self.content_area, bg=self.primary_color, padx=20, pady=20)
        stats_f.pack(fill="x")
        tk.Label(stats_f, text=f"🏛️ 등록 학생: {total}명  |  재학 상태: {on}명", 
                 fg="white", bg=self.primary_color, font=("맑은 고딕", 12, "bold")).pack()

    # 학생 명단 관리
    def show_student_mgmt(self):
        for widget in self.content_area.winfo_children(): widget.destroy()
        top_f = tk.Frame(self.content_area, bg="white")
        top_f.pack(fill="x", pady=(0, 15))
        tk.Label(top_f, text="👥 학생 명단 관리", font=("맑은 고딕", 18, "bold"), bg="white").pack(side="left")
        
        btn_f = tk.Frame(top_f, bg="white")
        btn_f.pack(side="right")
        tk.Button(btn_f, text="👤 학생 추가", bg="#28a745", fg="white", font=("맑은 고딕", 9, "bold"), 
                  padx=10, command=self.open_add_student_form).pack(side="left", padx=5)
        tk.Button(btn_f, text="🗑️ 학생 삭제", bg="#dc3545", fg="white", font=("맑은 고딕", 9, "bold"), 
                  padx=10, command=self.delete_student).pack(side="left")

        self.student_tree = ttk.Treeview(self.content_area, columns=("학번", "이름", "전공", "상태"), show="headings")
        for col in ("학번", "이름", "전공", "상태"):
            self.student_tree.heading(col, text=col); self.student_tree.column(col, anchor="center")
        self.student_tree.pack(fill="both", expand=True)
        self.refresh_student_list()

    def refresh_student_list(self):
        self.student_tree.delete(*self.student_tree.get_children())
        for sid, info in data.students.items():
            self.student_tree.insert("", "end", values=(sid, info['name'], info['major'], info['status']))

    def open_add_student_form(self):
        form = tk.Toplevel(self.win); form.title("신규 학생 등록"); form.geometry("400x450"); form.grab_set()
        fields = [("학번(ID)", ""), ("이름", ""), ("학과", "")]
        ents = {}
        for label, _ in fields:
            tk.Label(form, text=label, font=("맑은 고딕", 10, "bold")).pack(pady=(10, 0))
            e = tk.Entry(form, font=("맑은 고딕", 11), justify="center"); e.pack(fill="x", padx=50, ipady=5); ents[label] = e
        def submit():
            sid, name, major = ents["학번(ID)"].get(), ents["이름"].get(), ents["학과"].get()
            if not sid or sid in data.students: return messagebox.showerror("오류", "학번을 확인하세요.")
            data.students[sid] = {"name": name, "major": major, "status": "재학"}; data.users[sid] = {"password": sid, "role": "student"}
            common.save_data("students.json", data.students); common.save_data("users.json", data.users); self.refresh_student_list(); form.destroy()
        tk.Button(form, text="등록 완료", bg=self.primary_color, fg="white", command=submit).pack(pady=30)

    def delete_student(self):
        sel = self.student_tree.selection()
        if not sel: return
        sid = str(self.student_tree.item(sel)['values'][0])
        if messagebox.askyesno("삭제", f"학번 {sid} 학생을 삭제하시겠습니까?"):
            del data.students[sid]; del data.users[sid]
            common.save_data("students.json", data.students); common.save_data("users.json", data.users); self.refresh_student_list()

    # 3. 학적 변동 승인
    def show_request_mgmt(self):
        for widget in self.content_area.winfo_children(): widget.destroy()
        tk.Label(self.content_area, text="📝 학적 변동 신청 처리", font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w", pady=(0, 20))

        self.req_tree = ttk.Treeview(self.content_area, columns=("학번", "이름", "신청유형", "상태"), show="headings")
        for col in ("학번", "이름", "신청유형", "상태"):
            self.req_tree.heading(col, text=col); self.req_tree.column(col, anchor="center")
        self.req_tree.pack(fill="both", expand=True, pady=(0, 20))

        # 버튼들을 담은 프레임을 중앙으로 정렬
        btn_container = tk.Frame(self.content_area, bg="white")
        btn_container.pack(fill="x")
        
        # 실제 버튼들이 담길 내부 프레임
        btn_inner = tk.Frame(btn_container, bg="white")
        btn_inner.pack(anchor="center") # 이 부분이 핵심입니다.

        tk.Button(btn_inner, text="✅ 신청 승인", bg="#28a745", fg="white", font=("맑은 고딕", 10, "bold"), 
                  padx=30, pady=12, relief="flat", command=lambda: self.process_request("승인완료")).pack(side="left", padx=10)
        
        tk.Button(btn_inner, text="❌ 신청 반려", bg="#dc3545", fg="white", font=("맑은 고딕", 10, "bold"), 
                  padx=30, pady=12, relief="flat", command=lambda: self.process_request("반려")).pack(side="left", padx=10)

        self.refresh_requests()

    def refresh_requests(self):
        self.req_tree.delete(*self.req_tree.get_children())
        for req in data.academic_requests:
            s_name = data.students.get(req['student_id'], {}).get('name', '알수없음')
            self.req_tree.insert("", "end", values=(req['student_id'], s_name, req['type'], req['status']))

    def process_request(self, new_status):
        sel = self.req_tree.selection()
        if not sel: return messagebox.showwarning("알림", "항목을 선택하세요.")
        vals = self.req_tree.item(sel)['values']
        sid, r_type = str(vals[0]), vals[2]
        for req in data.academic_requests:
            if req['student_id'] == sid and req['type'] == r_type and req['status'] == "대기":
                req['status'] = new_status
                if new_status == "승인완료":
                    m = {"휴학": "휴학", "복학": "재학", "자퇴": "제적"}
                    if r_type in m: data.students[sid]['status'] = m[r_type]
                break
        common.save_data("academic_requests.json", data.academic_requests); common.save_data("students.json", data.students); self.refresh_requests()

    # 4. 공지사항 관리
    def show_notice_mgmt(self):
        for widget in self.content_area.winfo_children(): widget.destroy()
        top_f = tk.Frame(self.content_area, bg="white"); top_f.pack(fill="x", pady=(0, 10))
        tk.Label(top_f, text="📢 공지사항 관리", font=("맑은 고딕", 18, "bold"), bg="white").pack(side="left")
        tk.Button(top_f, text="➕ 새 공지 작성", bg=self.primary_color, fg="white", font=("맑은 고딕", 10, "bold"), 
                  padx=15, pady=5, command=self.open_notice_form).pack(side="right")
        
        self.notice_tree = ttk.Treeview(self.content_area, columns=("No", "제목"), show="headings")
        self.notice_tree.heading("No", text="No."); self.notice_tree.column("No", width=50, anchor="center")
        self.notice_tree.heading("제목", text="공지 제목"); self.notice_tree.column("제목", width=700, anchor="w")
        self.notice_tree.pack(fill="both", expand=True)
        self.notice_tree.bind("<Double-1>", self.open_notice_detail)
        self.refresh_notices()

    def refresh_notices(self):
        self.notice_tree.delete(*self.notice_tree.get_children())
        for i, n in enumerate(data.notices):
            p = n.split('] ', 1)
            t = p[0].replace('[', '') if len(p) > 1 else n
            self.notice_tree.insert("", "end", values=(len(data.notices)-i, t), tags=(n,))

    def open_notice_form(self):
        f = tk.Toplevel(self.win); f.geometry("500x500"); f.grab_set()
        tk.Label(f, text="제목").pack(pady=5); t_ent = tk.Entry(f, width=50); t_ent.pack()
        tk.Label(f, text="내용").pack(pady=5); c_txt = tk.Text(f, height=15); c_txt.pack()
        def save():
            data.notices.insert(0, f"[{t_ent.get()}] {c_txt.get('1.0', tk.END).strip()}")
            common.save_data("notices.json", data.notices); f.destroy(); self.refresh_notices()
        tk.Button(f, text="등록", command=save, bg=self.primary_color, fg="white").pack(pady=20)

    def open_notice_detail(self, event):
        sel = self.notice_tree.selection()
        if not sel: return
        full = self.notice_tree.item(sel, "tags")[0]
        p = full.split('] ', 1)
        d = tk.Toplevel(self.win); d.geometry("450x350")
        tk.Label(d, text=p[0].replace('[',''), font=("맑은 고딕", 12, "bold")).pack(pady=10)
        txt = tk.Text(d); txt.insert("1.0", p[1] if len(p)>1 else full); txt.config(state="disabled"); txt.pack()