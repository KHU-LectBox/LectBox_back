# LectBox
'22 봄학기 클라우드컴퓨팅 수업 프로젝트 (backend)

## 소개
LectBox는 대학생을 위한 강의용 공유 드라이브로, DropBox를 모티브로 개발된 SaaS입니다. 
강의자와 수강자가 강의자료, 과제 제출물 등에 해당하는 파일들을 공동으로 관리하며, 각 역할에 따라 폴더와 파일에 관한 접근 권한을 구분하여 편리하고 안전한 자료관리가 가능합니다. 이 리포지토리는 서비스 구성 중 백엔드를 관리합니다.

## 유저 스토리

- 강의자와 수강자로 나누어 회원가입
    
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/9e9ad354-6f74-4429-93bd-3ccf70722bef)
  
- 계정관리 및 로그아웃 가능
     
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/940557d7-24eb-4633-9eca-3ef58c06a9d5)
  
- 강의자 계정은 강의실 생성이 가능하다
  - 강의실 생성
    
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/21821b2b-8c4f-4038-91a7-56cfb36260bb)
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/a54dc549-8588-4b23-8287-ff3f7dc3cd9e)
  
  - 강의실 내부 강의, 폴더 섹션에 폴더 CRUD 및 파일 CRUD 및 업로드, 다운로드 가능
  - 현재 사용중인 용량을 표시하여 클라우드 리소스 관리가능
    
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/e1148821-109d-4060-b32a-d3f40bcf6329)
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/b67f5326-a1c4-489b-b556-a2645e901d41)
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/c3f79a24-c12c-4036-913d-460d05769184)
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/4d5c6c4a-7108-4b16-89ce-ccc971b8655c)
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/1f4c96a0-a910-4aef-b674-13904edc281c)



- 수강자 계정은 강의실 코드 입력하여 입장
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/d894f8a3-4b8a-4e82-a37a-3273df709f35)
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/00059d28-0d38-4c69-a65c-a5fd3eb8f837)

- 수강자는 강의자가 만든 파일 변경 불가, 다른 수강생이 제출한 파일도 변경 불가
  
![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/bf9357c5-48ac-4c3c-a788-a0366559c017)

![image](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/80f94ce5-f31d-4a58-92b6-2162efd61d9d)


## 기능
- 강의를 위한 공유 스토리지 제공
- 강의에 참여하는 강의자와 수강자가 이용 목적에 맞춘 UI를 제공
- 기본 구조: 강의실, 강의 폴더, 과제 폴더
- 역할별 권한 부여
  - 강의자: 강의실 생성 및 삭제, 폴더 관리, 파일 관리
  - 수강자: 강의실 입장, 본인이 생성한 파일 관리
- 기본적인 공유 스토리지 기능 제공
- 강의실 당 최대 용량, 사용 용량 제공
- 파일 관리
  - 업로드, 다운로드, 삭제
  - 폴더별 목록 출력
- 폴더 및 강의실 생성, 삭제
  - 디렉토리/강의실 생성
  - 디렉토리/강의실 이름, 공유 범위 등의 업데이트
  - 디렉토리/강의실 삭제
  - 강의실 회원 권한 설정
- 유저 정보 관리
  - 회원가입
  - 회원 정보 업데이트
  - 회원 탈퇴
  - 회원 권한 부여 및 확인
  
## 개발 환경
- Server: Django, DRF, Amazon EC2 (배포)
- Database: SQLite3
- Front-End: React, Amazon S3 & CloudFront (배포)
- Storage: Amazon S3


## 아키텍처
![LectBox_ Architecture](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/cd8db5e6-0304-44cb-b12d-661c9208ba73)


## 데모

[데모영상유튜브링크](https://youtu.be/aDn9ul5CLJE)

![LectBox_Demo-ezgif com-video-to-gif-converter](https://github.com/KHU-LectBox/LectBox_back/assets/92240138/2b5e78cf-2db2-4d6a-afcd-7cb7092381b4)




# 참여자
- [고병후](https://github.com/GoByeonghu): Backend 개발자
- [연동현](https://github.com/OUYA77): Backend 개발자
- [이재호](https://github.com/JH-LEE-KR): Backend 개발자
- [조민식](https://github.com/mongsik98): Frontend 개발자
- [손지원](https://github.com/jiwonsoong): Frontend 개발자