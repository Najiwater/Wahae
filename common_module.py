import json, os, data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 스크립트의 디렉토리 경로
DATA_DIR = os.path.join(BASE_DIR, "system_data")       # 데이터 파일이 저장될 디렉토리

def load_data(name, default):# JSON 파일에서 데이터 로드
    if not os.path.exists(DATA_DIR): # 데이터 디렉토리가 없으면 생성
        os.makedirs(DATA_DIR)
    
    path = os.path.join(DATA_DIR, name) # 파일 전체 경로 생성
    
    
    if not os.path.exists(path): # 파일이 존재하지 않으면 기본값 반환
        return default
    
    try: # JSON 파일 읽기 시도
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        # 오류 발생 시 기본값 반환
        return default

def load_all_data(): #프로그램 시작 시 호출되어 모든 JSON 파일의 데이터를 전역 변수에 로드
    # 사용자 인증 정보 로드
    data.users = load_data("users.json", {})

    # 학생/교수/관리자 정보 로드
    data.students = load_data("students.json", {})
    data.professors = load_data("professors.json", {})
    data.admins = load_data("admins.json", {})
    
    # 강의 관련 정보 로드
    data.courses = load_data("courses.json", {})
    data.grades = load_data("grades.json", {})
    data.attendance = load_data("attendance.json", {})
    
    # 공지사항 및 기타 정보 로드
    data.notices = load_data("notices.json", [])
    data.graduation_requirements = load_data("graduation_requirements.json", {})
    data.academic_requests = load_data("academic_requests.json", [])

def save_data(name, obj): # 데이터를 JSON 파일로 저장
    path = os.path.join(DATA_DIR, name)  # 파일 전체 경로 생성
    with open(path, "w", encoding="utf-8") as f: # JSON 형식으로 파일에 저장 (한글 유지, 들여쓰기 적용)
        json.dump(obj, f, ensure_ascii=False, indent=4)