# computer theory

컴퓨터 이론 학습 자료와 코드를 모아 두는 저장소입니다.

- 사이트: https://sage810.github.io/computer-theory/
- 첫 화면: `index.html` (자료구조 · 알고리즘 · 운영체제 → 영역 → 내용요소 → 세부내용)
- 과목별 주소: `#ds` 자료구조, `#algo` 알고리즘, `#os` 운영체제
- 내용요소 노트: `ds/1-1-1/`, `algo/2-1-1/`, `os/3-1-1/` … 번호 폴더마다 `index.html` 한 장 (58장). 모양은 `assets/note.css` 하나로 같이 바뀜

## 노트 쓰기와 목차 연결

1. 노트마다 Word 원고가 `노트 원고/<과목>/<번호> <이름>.docx` 에 있습니다(이 PC·OneDrive 에만, GitHub 에는 올리지 않음).
2. Word 를 고친 뒤 Claude 에게 "3-1-1 노트 반영해줘"라고 하면 `scripts/note_sync.py` 로 노트(`os/3-1-1/index.html` 등)를 고칩니다.
3. `npm run index` 로 첫 화면을 다시 만들면, 칸이 하나라도 채워진 노트는 목차에서 자동으로 링크되고 '연결된 자료' 숫자와 왼쪽 고정 목차(`assets/toc.js`)도 맞춰집니다. 목차 원본 데이터는 `scripts/index-data.json` 입니다.
