<div align="center">

# 전주대학교 파이썬 기초 및 실습 기말 팀프로젝트
# 🎓 3중 학사관리시스템 
**Python / JSON Based Academic Platform** 

![js](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![js](https://img.shields.io/badge/JSON-3776AB?style=flat&logo=json&logoColor=white) 
      
</div>

---
# 👥 Team 와해(渦解) 소개
**구성원 : 나지수 임지후 정종빈 김재영 송제용 장현준 최혁**

---
# 📌 프로젝트 개요

본 프로젝트는 **학생(Student)**, **교수(Professor)**, **행정직원(Admin)**  
세 가지 역할을 기반으로 각각 다른 기능을 제공하는 **학사관리 시스템**입니다.

Python + JSON 데이터 구조를 활용하여  
동작하는 **학사관리 시스템**을 구현했습니다.

---
# 🧩 개발 목적

- 역할별로 다른 학사 기능을 제공하는 통합 시스템 제작  
- JSON 데이터를 통한 경량 스토리지 구조 실습  
- Python OOP 클래스 구조 기반 설계 능력 향상  
- 실제 학사관리 기능을 단순화하여 콘솔 기반으로 모델링  

---
# 🗂️ 시스템 주요 기능 및 구

## 👨‍🎓 **학생(Student) 기능**
- 수강신청 / 수강취소  
- 시간표 조회  
- 성적 조회  
- 공지사항 열람  
- 내 정보 수정  

## 👨‍🏫 **교수(Professor) 기능**
- 담당 강의 목록 조회  
- 수강생 명단 확인  
- 성적 입력  
- 공지사항 등록  

## 🧑‍💼 **행정직원(Admin) 기능**
- 강의 개설 / 삭제  
- 전체 사용자 조회  
- 기본 시스템 데이터 관리

## 🏗️ 시스템 구조
'''

academic_system/
│
├── main.py
├── data.py
│
├── user_base.py
├── student.py
├── professor.py
├── admin.py
│
├── unified_users.json
└── login_users.json

'''


# 🔍 개발 진행 과정 (4주차 팀 활동 기록)

## 📅 1주차 – 요구사항 분석 / 구조 설계

역할별 기능 정의(Student/Professor/Admin)

JSON 기반 저장 구조 확정

UML 개념 스케치 작성

팀 역할 분담 및 GitHub 초기 세팅

## 📅 2주차 – 클래스 · JSON 구조 설계

User → Student / Professor / Admin 상속 구조 완성

unified_users.json 설계

student.py, professor.py, admin.py 기본 코드 작성

## 📅 3주차 – 기능 구현 및 통합

로그인 기능 완성

JSON → 객체 자동 생성 로직 구현

학생/교수/행정직원 메뉴 기능 70% 개발 완료

수강신청, 공지등록 등 핵심 기능 작동 확인

## 📅 4주차 – 중간발표

JSON 기반 전체 로직 검증 완료

SD UML 다이어그램 제작

README(과제 제출용) 정리

PPT 발표자료 및 시연 흐름 정리

## 📅 5주차

## 📅 6주차

## 📅 7주차

# 성능 · 테스트(추후 결정)

프로젝트 특성상 다음처럼 테스트 가능:

JSON 로딩 시간 측정

메뉴 기능 반복 호출 테스트

공지사항/수강신청 대량 생성 스트레스 테스트

(프로그램 완성 후 시간이 남을시 테스트 해볼 예정)

<div align="center">

# 감사합니다.

</div> 

```

