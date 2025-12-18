# 이미지를 .ico 파일로 변환하는 스크립트
from PIL import Image
import os

# 현재 디렉토리 확인
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"현재 디렉토리: {current_dir}")

# 이미지 파일 경로 (사용자가 저장한 파일명에 맞게 수정하세요)
image_path = os.path.join(current_dir, "icon.png")

if not os.path.exists(image_path):
    print(f"오류: {image_path} 파일을 찾을 수 없습니다.")
    print("첨부하신 이미지를 'icon.png' 이름으로 이 폴더에 저장해주세요.")
    input("엔터를 눌러 종료...")
    exit()

# 이미지 열기
img = Image.open(image_path)

# RGBA 모드로 변환 (투명도 지원)
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# 아이콘 크기로 리사이즈 (256x256)
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

# .ico 파일로 저장
ico_path = os.path.join(current_dir, "icon.ico")
img.save(ico_path, format='ICO', sizes=icon_sizes)

print(f"성공! {ico_path} 파일이 생성되었습니다.")
input("엔터를 눌러 종료...")
