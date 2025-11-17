# common_module.py
import os
import json
import data
from datetime import datetime

GRADE_TO_SCORE = {
    'A+': 4.5, 'A0': 4.0, 'B+': 3.5, 'B0': 3.0,
    'C+': 2.5, 'C0': 2.0, 'D+': 1.5, 'D0': 1.0, 'F': 0.0
}

# --- 데이터 파일 경로 설정 ---
DATA_DIR = 'system_data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
PROFESSORS_FILE = os.path.join(DATA_DIR, 'professors.json')
ADMINS_FILE = os.path.join(DATA_DIR, 'admins.json')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')
GRADES_FILE = os.path.join(DATA_DIR, 'grades.json')
# 새로 추가된 파일 경로
NOTICES_FILE = os.path.join(DATA_DIR, 'notices.json')
ACADEMIC_REQUESTS_FILE = os.path.join(DATA_DIR, 'academic_requests.json')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.json')

def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def _load_json_file(filename, default_value):
    _ensure_data_dir()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _save_json_file(filename, default_value)
        return default_value

def _save_json_file(filename, data_content):
    _ensure_data_dir()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_content, f, indent=4, ensure_ascii=False)

# --- 각 데이터별 저장 함수 ---
def save_users(): _save_json_file(USERS_FILE, data.users)
def save_students(): _save_json_file(STUDENTS_FILE, data.students)
def save_professors(): _save_json_file(PROFESSORS_FILE, data.professors)
def save_admins(): _save_json_file(ADMINS_FILE, data.admins)
def save_courses(): _save_json_file(COURSES_FILE, data.courses)
def save_grades(): _save_json_file(GRADES_FILE, data.grades)
def save_notices(): _save_json_file(NOTICES_FILE, data.notices)
def save_academic_requests(): _save_json_file(ACADEMIC_REQUESTS_FILE, data.academic_requests)
def save_attendance(): _save_json_file(ATTENDANCE_FILE, data.attendance)

# --- 프로그램 시작 시 모든 데이터 로드 ---
def load_all_data():
    data.users = _load_json_file(USERS_FILE, {})
    data.students = _load_json_file(STUDENTS_FILE, {})
    data.professors = _load_json_file(PROFESSORS_FILE, {})
    data.admins = _load_json_file(ADMINS_FILE, {})
    data.courses = _load_json_file(COURSES_FILE, {})
    data.grades = _load_json_file(GRADES_FILE, {})
    # 새 데이터 로드
    data.notices = _load_json_file(NOTICES_FILE, [])
    data.academic_requests = _load_json_file(ACADEMIC_REQUESTS_FILE, [])
    data.attendance = _load_json_file(ATTENDANCE_FILE, {})
    print("시스템 데이터 로드 완료.")

# --- 공통 유틸리티 ---
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')
def pause(): input("\n계속하려면 Enter 키를 누르세요...")

# --- (신규) 시간표 충돌 감지 로직 ---
def check_time_conflict(student_course_ids, new_course_id):
    """
    학생의 기존 시간표와 새 과목의 시간표가 겹치는지 확인합니다.
    겹치면 True, 아니면 False를 반환합니다.
    """
    new_course = data.courses.get(new_course_id)
    if not new_course or 'time' not in new_course:
        return False # 시간 정보가 없는 과목은 충돌 검사 통과

    new_time = new_course['time'] # 예: {'day': '월', 'start': 10, 'end': 12}

    for course_id in student_course_ids:
        existing_course = data.courses.get(course_id)
        if not existing_course or 'time' not in existing_course:
            continue
        
        existing_time = existing_course['time']
        
        # 1. 요일이 다르면 충돌 아님
        if new_time['day'] != existing_time['day']:
            continue
            
        # 2. 요일이 같으면 시간 비교 (A: new, B: existing)
        # (A_start < B_end) and (B_start < A_end) -> 겹침
        if (new_time['start'] < existing_time['end'] and 
            existing_time['start'] < new_time['end']):
            
            print(f"[충돌 감지] {new_course['title']} ({new_time['day']} {new_time['start']}-{new_time['end']}) 과목이")
            print(f"  -> {existing_course['title']} ({existing_time['day']} {existing_time['start']}-{existing_time['end']}) 과목과 겹칩니다.")
            return True # 충돌 발생
            
    return False # 충돌 없음

# --- 공통 기능 (로그인/회원가입/공지/비번변경) ---

def login(role):
    """역할에 맞는 사용자인지 확인하여 로그인 (이름 표시로 수정)"""
    clear_screen()
    print(f"--- {role.upper()} 로그인 ---")
    user_id = input("아이디: ")
    password = input("비밀번호: ")

    # 1. data.users에서 아이디, 비밀번호, 역할 확인
    user_info = data.users.get(user_id)

    if user_info and user_info['password'] == password and user_info['role'] == role:
        
        # --- [수정된 부분 시작] ---
        # 2. 로그인이 성공하면, 역할(role)에 맞는 딕셔너리에서 'name'을 가져옵니다.
        name = user_id  # 기본값은 ID로 설정 (혹시 이름 정보가 없을 경우 대비)
        
        if role == 'student':
            student_info = data.students.get(user_id)
            if student_info:
                name = student_info.get('name', user_id) # 'name' 키가 있으면 이름으로, 없으면 ID로
        
        elif role == 'professor':
            professor_info = data.professors.get(user_id)
            if professor_info:
                name = professor_info.get('name', user_id)
                
        elif role == 'admin':
            admin_info = data.admins.get(user_id)
            if admin_info:
                name = admin_info.get('name', user_id)
        
        # 3. 'name' 변수를 사용하여 환영 메시지 출력
        print(f"\n로그인 성공. {name}님 환영합니다.") # <-- 수정된 환영 메시지
        # --- [수정된 부분 끝] ---
        
        pause()
        return user_id
    else:
        print("\n로그인 실패. 아이디, 비밀번호 또는 역할이 일치하지 않습니다.")
        pause()
        return None

def view_notices():
    """(신규) 공통 공지사항 조회 기능"""
    clear_screen()
    print("--- 📢 공지사항 ---")
    if not data.notices:
        print("등록된 공지사항이 없습니다.")
    else:
        # 최신 공지가 위로 오도록 정렬 (id가 문자열 숫자라고 가정)
        sorted_notices = sorted(data.notices, key=lambda x: int(x.get('id', '0')), reverse=True)
        for notice in sorted_notices:
            print("-" * 20)
            print(f"[ID: {notice['id']}] {notice['title']} (작성자: {notice['author']})")
            print(f"내용: {notice['content']}")
    pause()

def change_password(user_id):
    """(신규) 공통 비밀번호 변경 기능"""
    clear_screen()
    print("--- 비밀번호 변경 ---")
    current_password = input("현재 비밀번호: ")
    
    if data.users[user_id]['password'] != current_password:
        print("현재 비밀번호가 일치하지 않습니다.")
        pause()
        return

    new_password = input("새 비밀번호: ")
    new_password_confirm = input("새 비밀번호 확인: ")

    if new_password != new_password_confirm:
        print("새 비밀번호가 일치하지 않습니다.")
    else:
        data.users[user_id]['password'] = new_password
        save_users()
        print("비밀번호가 성공적으로 변경되었습니다.")
    pause()