input
보드 url

output
폴더 생성하고 해당 보드 내의 사진 저장

logic

url 입력
실행
보드 내의 사진 url 리스트화
url에 requests로 다운로드 요청
이 때 차단을 막기 위해 requests 요청하여 다운로드가 다 되면 다음 요청 수행
tqdm으로 진행도 표시

패키징
playwright, requests 라이브러리 포함
ui -> url 입력
창, 저장 경로 설정, 실행 버튼
아래에는 진행도 표시

할 일

1. GUI로 패키징
2. 보드 스크래핑 과정 안정성 향상할 수 있는 방법 모색(완료)
3. 상호작용하는 UI 모듈 만들기(CLI 구현)
4. 로거 구현 - GUI에 로깅된 그대로 출력하기
