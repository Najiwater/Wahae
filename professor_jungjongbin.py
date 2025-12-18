import tkinter as tk
from tkinter import messagebox, ttk
import data
import common_module as common

class ProfessorMenu: #교수용 메뉴 화면 클래스
    def __init__(self, parent, user_id):
        self.user_id = user_id
        self.win = tk.Toplevel(parent)
        self.win.title(f"교수 정보 시스템 - {user_id}")
        self.win.geometry("1050x750")
        
        self.primary_color = "#003366"
        # 담당 강의 목록 추출
        self.my_courses = {cid: c for cid, c in data.courses.items() if c['professor_user_id'] == user_id}
        self.current_cid = None  # 현재 선택된 과목 ID
        
        self.setup_ui()

    def setup_ui(self): #교수 메뉴 UI 구성
        # 교수 이름 표시
        header = tk.Frame(self.win, bg=self.primary_color, height=60)
        header.pack(fill="x")
        p_info = data.professors.get(self.user_id, {})
        tk.Label(header, text=f"👨‍🏫 {p_info.get('name')} 교수님 업무 포털", 
                 fg="white", bg=self.primary_color, font=("맑은 고딕", 12, "bold")).pack(side="left", padx=20, pady=15)

        # 메인 레이아웃
        self.main_frame = tk.Frame(self.win, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)

        # 왼쪽 메뉴 버튼
        sidebar = tk.Frame(self.main_frame, bg="white", width=200)
        sidebar.pack(side="left", fill="y", padx=1, pady=1)
        
        # 메뉴 항목 정의
        menus = [
            ("🏠 강의 대시보드", self.show_dashboard), 
            ("📅 주차별 출결 관리", self.show_attendance_manage),
            ("📊 성적 기입/수정", self.show_grade_manage)
        ]
        
        # 메뉴 버튼 생성
        for text, cmd in menus:
            tk.Button(sidebar, text=text, font=("맑은 고딕", 10), bg="white", relief="flat",
                      anchor="w", padx=20, pady=15, command=cmd).pack(fill="x")

        # 주요 컨텐츠 표시 영역
        self.content_area = tk.Frame(self.main_frame, bg="white")
        self.content_area.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        # 기본으로 대시보드 표시
        self.show_dashboard()

    def show_dashboard(self): # 강의 대시보드 화면 표시 - 담당 강의 목록 표시
        # 기존 컨텐츠 제거
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="📢 담당 강의 요약", font=("맑은 고딕", 16, "bold"), bg="white").pack(anchor="w", pady=10)
        
        # 각 강의별 표시
        for cid, c in self.my_courses.items():
            f = tk.Frame(self.content_area, bg="#f8f9fa", pady=10, padx=15, highlightthickness=1, highlightbackground="#dee2e6")
            f.pack(fill="x", pady=5)
            # 과목 코드와 제목
            tk.Label(f, text=f"[{cid}] {c['title']}", font=("맑은 고딕", 11, "bold"), bg="#f8f9fa").pack(side="left")
            # 수강생 수
            tk.Label(f, text=f"수강생: {len(c.get('student_user_ids', []))}명", bg="#f8f9fa", fg=self.primary_color).pack(side="right")

    # 주차별 출결 관리 (일괄 적용 추가) ---
    def show_attendance_manage(self):
        """출결 관리 화면 표시 - 주차별 학생 출결 관리"""
        # 기존 컨텐츠 제거
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="📅 주차별 출결 관리", font=("맑은 고딕", 16, "bold"), bg="white").pack(anchor="w", pady=10)
        
        # [제어 영역] - 과목 및 주차 선택
        ctrl_frame = tk.Frame(self.content_area, bg="white")
        ctrl_frame.pack(fill="x", pady=5)
        
        # 과목 선택
        tk.Label(ctrl_frame, text="과목:", bg="white").pack(side="left")
        self.att_course_combo = ttk.Combobox(ctrl_frame, values=[c['title'] for c in self.my_courses.values()], width=20)
        self.att_course_combo.pack(side="left", padx=5)
        
        # 주차 선택
        tk.Label(ctrl_frame, text="주차:", bg="white").pack(side="left", padx=5)
        self.week_combo = ttk.Combobox(ctrl_frame, values=[f"{i}주차" for i in range(1, 17)], width=10)
        self.week_combo.current(0)  # 기본 1주차
        self.week_combo.pack(side="left", padx=5)
        
        # 명단 조회 버튼
        tk.Button(ctrl_frame, text="명단 조회", command=self.load_attendance_list, bg=self.primary_color, fg="white").pack(side="left", padx=10)

        # [출결 Treeview] - 학생 목록 및 출결 현황
        self.att_tree = ttk.Treeview(self.content_area, columns=("학번", "이름", "해당주차상태", "누적결석"), show="headings")
        for col in ("학번", "이름", "해당주차상태", "누적결석"): self.att_tree.heading(col, text=col)
        self.att_tree.pack(fill="both", expand=True, pady=10)

        # [입력 영역] - 출결 상태 선택 및 저장
        input_f = tk.Frame(self.content_area, bg="#f8f9fa", pady=10)
        input_f.pack(fill="x")
        
        # 상태 선택 라디오 버튼
        tk.Label(input_f, text="상태 선택:", bg="#f8f9fa").pack(side="left", padx=10)
        self.status_var = tk.StringVar(value="출석")
        for s in ["출석", "결석", "지각"]:
            tk.Radiobutton(input_f, text=s, variable=self.status_var, value=s, bg="#f8f9fa").pack(side="left", padx=5)
        
        # 버튼 2개: 선택 저장 / 일괄 적용
        tk.Button(input_f, text="선택 저장", command=self.save_attendance, bg="#28a745", fg="white", width=10).pack(side="right", padx=5)
        tk.Button(input_f, text="전체 일괄 적용", command=self.batch_save_attendance, bg="#ffc107", fg="black", width=15).pack(side="right", padx=10)

    def load_attendance_list(self):
        """선택한 과목과 주차의 학생 출결 명단 로드"""
        course_name = self.att_course_combo.get()
        if not course_name: return
        
        # 과목 ID 찾기
        cid = [k for k, v in self.my_courses.items() if v['title'] == course_name][0]
        self.current_cid = cid
        week_idx = self.week_combo.current()  # 선택된 주차 인덱스
        
        # 기존 목록 제거
        self.att_tree.delete(*self.att_tree.get_children())
        
        # 수강생 목록 표시
        for sid in self.my_courses[cid].get('student_user_ids', []):
            name = data.students.get(sid, {}).get("name", "미등록")
            att_list = data.attendance.get(cid, {}).get(sid, ["-"] * 16)  # 16주차 기본값
            current_status = att_list[week_idx] if week_idx < len(att_list) else "-"
            absent_count = att_list.count("결석")  # 누적 결석 횟수
            self.att_tree.insert("", "end", values=(sid, name, current_status, f"{absent_count}회"))

    def save_attendance(self):
        """선택한 학생의 출결 정보 저장"""
        selected = self.att_tree.selection()
        if not selected: 
            messagebox.showwarning("알림", "학생을 선택하세요.")
            return
        
        # 선택된 학생 ID 가져오기
        sid = self.att_tree.item(selected[0])['values'][0]
        self._update_attendance(sid)
        messagebox.showinfo("완료", "저장되었습니다.")
        self.load_attendance_list()  # 목록 새로고침

    def batch_save_attendance(self):#전체 학생의 출결을 선택한 상태로 일괄 적용
        if not self.current_cid: return
        
        # 확인 메시지
        if not messagebox.askyesno("확인", f"현재 명단의 모든 학생을 '{self.status_var.get()}'(으)로 일괄 처리하시겠습니까?"): 
            return
        
        # 모든 수강생에게 적용
        for sid in self.my_courses[self.current_cid].get('student_user_ids', []):
            self._update_attendance(sid)
        
        common.save_data("attendance.json", data.attendance)
        messagebox.showinfo("완료", "모든 학생의 출결이 일괄 적용되었습니다.")
        self.load_attendance_list()  # 목록 새로고침

    def _update_attendance(self, sid):#"""출결 데이터 업데이트 
        week_idx = self.week_combo.current()  # 현재 선택된 주차
        
        # 출석 데이터 초기화 (과목별, 학생별)
        if self.current_cid not in data.attendance: 
            data.attendance[self.current_cid] = {}
        if sid not in data.attendance[self.current_cid]: 
            data.attendance[self.current_cid][sid] = ["-"] * 16
        
        # 해당 주차에 선택된 상태 저장
        data.attendance[self.current_cid][sid][week_idx] = self.status_var.get()
        common.save_data("attendance.json", data.attendance)

    # --- [기능 2] 성적 관리 (일괄 적용 추가) ---
    def show_grade_manage(self):
        """성적 관리 화면 표시 - 학생별 성적 기입 및 수정"""
        # 기존 컨텐츠 제거
        for widget in self.content_area.winfo_children(): widget.destroy()
        
        tk.Label(self.content_area, text="📊 성적 기입/수정", font=("맑은 고딕", 16, "bold"), bg="white").pack(anchor="w", pady=10)

        # [제어 영역] - 과목 선택
        ctrl_frame = tk.Frame(self.content_area, bg="white")
        ctrl_frame.pack(fill="x", pady=5)
        self.grd_course_combo = ttk.Combobox(ctrl_frame, values=[c['title'] for c in self.my_courses.values()], width=25)
        self.grd_course_combo.pack(side="left")
        tk.Button(ctrl_frame, text="명단 조회", command=self.load_grade_list, bg=self.primary_color, fg="white").pack(side="left", padx=10)

        # [성적 Treeview] - 학생 목록 및 현재 성적
        self.grd_tree = ttk.Treeview(self.content_area, columns=("학번", "이름", "현재성적"), show="headings")
        for col in ("학번", "이름", "현재성적"): 
            self.grd_tree.heading(col, text=col)
        self.grd_tree.pack(fill="both", expand=True, pady=10)

        # [입력 영역] - 성적 선택 및 저장
        edit_f = tk.Frame(self.content_area, bg="#f8f9fa", pady=10)
        edit_f.pack(fill="x")
        
        tk.Label(edit_f, text="성적 선택:", bg="#f8f9fa").pack(side="left", padx=10)
        grade_list = ["A+", "A0", "B+", "B0", "C+", "C0", "D+", "D0", "F", "P", "NP"]
        self.combo_score = ttk.Combobox(edit_f, values=grade_list, width=10, state="readonly")
        self.combo_score.pack(side="left", padx=5)
        
        # 버튼 2개: 선택 저장 / 일괄 적용
        tk.Button(edit_f, text="선택 저장", command=self.save_grade, bg="#007bff", fg="white", width=10).pack(side="right", padx=5)
        tk.Button(edit_f, text="전체 일괄 적용", command=self.batch_save_grade, bg="#ffc107", fg="black", width=15).pack(side="right", padx=10)

    def load_grade_list(self):
        """선택한 과목의 학생 성적 명단 로드"""
        course_name = self.grd_course_combo.get()
        if not course_name: return
        
        # 과목 ID 찾기
        self.current_grd_cid = [k for k, v in self.my_courses.items() if v['title'] == course_name][0]
        
        # 기존 목록 제거
        self.grd_tree.delete(*self.grd_tree.get_children())
        
        # 수강생 목록 표시
        for sid in self.my_courses[self.current_grd_cid].get('student_user_ids', []):
            name = data.students.get(sid, {}).get("name", "미등록")
            grade = data.grades.get(sid, {}).get(course_name, "미입력")
            self.grd_tree.insert("", "end", values=(sid, name, grade))

    def save_grade(self):
        """선택한 학생의 성적 저장"""
        selected = self.grd_tree.selection()
        if not selected: 
            messagebox.showwarning("알림", "학생을 선택하세요.")
            return
        
        # 선택된 학생 ID 가져오기
        sid = self.grd_tree.item(selected[0])['values'][0]
        self._update_grade(sid)
        messagebox.showinfo("완료", "성적이 반영되었습니다.")
        self.load_grade_list()  # 목록 새로고침

    def batch_save_grade(self):
        """전체 학생의 성적을 선택한 등급으로 일괄 적용"""
        course_name = self.grd_course_combo.get()
        new_grade = self.combo_score.get()
        
        if not course_name or not new_grade: 
            messagebox.showwarning("알림", "과목과 성적 등급을 먼저 선택하세요.")
            return
        
        # 확인 메시지
        if not messagebox.askyesno("확인", f"모든 수강생의 성적을 '{new_grade}'(으)로 일괄 입력하시겠습니까?"): 
            return

        # 모든 수강생에게 적용
        for sid in self.my_courses[self.current_grd_cid].get('student_user_ids', []):
            self._update_grade(sid)
        
        common.save_data("grades.json", data.grades)
        messagebox.showinfo("완료", "모든 학생의 성적이 일괄 적용되었습니다.")
        self.load_grade_list()  # 목록 새로고침

    def _update_grade(self, sid):
        """성적 데이터 업데이트 (내부 헬퍼 메서드)
        
        Args:
            sid: 학생 ID
        """
        course_name = self.grd_course_combo.get()
        new_grade = self.combo_score.get()
        if not new_grade: return
        
        # 성적 데이터 초기화 (학생별)
        if sid not in data.grades: 
            data.grades[sid] = {}
        
        # 과목명을 키로 성적 저장
        data.grades[sid][course_name] = new_grade
        common.save_data("grades.json", data.grades)