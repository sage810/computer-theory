# PROJECT_MAP

이 저장소에 어떤 파일이 있고 무엇이 달라졌는지 적는 지도입니다.

## 파일 목록

| 파일 | 설명 |
|---|---|
| index.html | 첫 화면(GitHub Pages). info-lesson 첫 화면과 레트로 창 겉모습은 같으나, 단원 세로 칸 대신 맨 위 과목 탭 + 영역 상자마다 `번호 | 내용요소 | 세부내용` 표(시안 D) + 왼쪽 고정 목차. `npm run index` 로 만듦 |
| (index.html 목차 링크) | 노트 칸이 하나라도 채워진 내용요소는 이름이 영역 노트의 그 자리(`#n-…`) 링크가 되고 '준비 중'이 빠짐, 제목줄 '연결된 자료' 숫자에 셈. 그런 내용요소가 있는 영역은 영역 이름도 영역 노트 링크 |
| ds/·algo/·os/ `영역번호/index.html` | 영역 노트 14장(예: `os/3-1/`). 영역 머리 + 내용요소마다 `<article id="n-3-1-1">`(번호·이름 띠, 키워드·세부내용, 공부 칸)이 쭉 이어짐 + 이전·목차·다음 영역. 그림은 영역 폴더 `3-1-1-fig-1.png` 처럼 내용요소 번호를 붙임. 칸이 채워진 내용요소는 첫 화면 '연결된 자료'에서 셈(2026-11-22 기준 25 / 58) |
| ds/·algo/·os/ `내용요소번호/index.html` | 예전 내용요소 노트 주소 58개. 이제는 영역 노트의 그 자리(`../3-1/index.html#n-3-1-1`)로 바로 넘겨 주는 페이지만 |
| assets/sidebar.css · assets/sidebar.js | 왼쪽 고정 목차. 첫 화면과 영역 노트 14장이 같은 파일을 불러 씀(`data-root`, 노트는 `data-current`=영역번호). 과목 › 영역 드롭다운, 영역 노트에서는 지금 화면의 내용요소를 표시, 목차 자체 접기, 좁은 화면은 서랍 |
| assets/toc.js | 왼쪽 목차 데이터(과목·영역·내용요소·노트 있음 여부). `scripts/gen_index.py` 가 index.html 과 함께 만듦, 손으로 고치지 않음 |
| assets/note.css | 영역 노트 14장이 같이 쓰는 모양. 첫 화면과 같은 창·제목줄·과목 탭·머리 상자, 과목 색은 `body.s-ds/s-algo/s-os`. 첫 화면과 달리 공부 칸은 세로 안내선 없이 여백·들여쓰기로 묶음 |
| .github/workflows/pages.yml | main에 push하면 index.html·fonts·tools/memo.js·assets·노트 폴더만 Pages에 배포. info-lesson의 같은 파일과 달리 빌드 없이 복사만 |
| tools/memo.js | 피드백 모드 화면 쪽(`?memo=1`). middle school info의 `msi-memo.js`와 같으나 위치를 '과목 › 영역 › 내용요소'로 적음 |
| scripts/serve.mjs | 미리보기 서버(8090) + `/__feedback`. info-lesson 쪽(8080)과 달리 빌드 결과가 아니라 저장소를 직접 보여 주되 index.html·fonts·tools·assets·노트 폴더만 |
| scripts/memo.mjs | `npm run memo` — 서버 켜고 `?memo=1`로 열기. info-lesson 쪽과 달리 빌드 단계 없음 |
| scripts/gen_index.py · scripts/index-data.json | 첫 화면 만들기(`npm run index`). 전에는 세션 임시 폴더에만 있던 생성기를 옮김. 칸이 채워진 내용요소는 영역 노트의 그 자리로 자동 링크 |
| 노트 원고/ (git 제외) | 영역 14개의 Word 원고(`3-1 운영체제 개요.docx` …, 안에 내용요소가 쭉 이어짐). 사용자가 만든 3.1.1 원고 서식(제목 → 위치 줄 → 제목 1 칸 이름 → 굵은 묶음 글머리 목록). 고친 뒤 "노트 반영해줘" |
| scripts/note_sync.py | 영역 Word 원고 → 영역 노트의 내용요소별 공부 칸 반영(목록 단계·굵게·고친 곳 표시·Word 수식·그림·표). gen_index.py 와 달리 영역 노트 한 장의 칸만 바꿈 |
| package.json | `npm run serve`, `npm run memo`, `npm run index` (외부 패키지 없음) |
| docs/feedback-mode.md | 피드백 모드 켜기·쓰는 법·기록 형식·처리 순서 |
| fonts/ | 쿠키런 700, 메이플스토리 300·700 (middle school info에서 복사), 넥슨 Lv2 고딕 400·500·700 서브셋 (사용자가 받은 TTF 에서 2350자만 추림, 700 은 노트만, 500 은 지금 안 씀), KoPub World 돋움 Medium 서브셋 (노트 목록 본문) |
| .design/style-lock.md | 확정한 색·글꼴·배치 값 |
| .design/decisions.log | 디자인 판단 이유와 반려한 대안 |
| .impeccable/config.json | 디자인 점검 훅이 일부러 둔 모양(굵은 테두리+둥근 모서리, 창 속 상자)을 다시 지적하지 않게 하는 예외 목록. `.design/` 과 달리 사람용 기록이 아니라 점검 도구 설정 |
| README.md | 저장소 소개 + 내용요소에 자료 링크 붙이는 방법 |
| CLAUDE.md | Karpathy 코딩 가이드라인 + 프로젝트 규칙(한글 커밋 메시지) |
| .gitignore | 운영체제·편집기·Python·Node 부산물과 키·비밀번호·토큰 파일 제외 |
| PROJECT_MAP.md | 이 지도 문서 |
| .claude/AGENTS_MAP.md | 이 프로젝트에서 쓴 스킬·에이전트 기록 |
