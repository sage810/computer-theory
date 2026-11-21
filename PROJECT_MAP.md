# PROJECT_MAP

이 저장소에 어떤 파일이 있고 무엇이 달라졌는지 적는 지도입니다.

## 파일 목록

| 파일 | 설명 |
|---|---|
| index.html | 첫 화면(GitHub Pages). info-lesson 첫 화면과 레트로 창 겉모습은 같으나, 단원 세로 칸 대신 맨 위 과목 탭 + 영역별 트리 개요(`1.1.1`, `#키워드`) + 세부내용 접고 펴기 |
| (index.html 목차 링크) | 노트 칸이 하나라도 채워진 내용요소는 이름이 노트 링크가 되고 '준비 중'이 빠짐, 제목줄 '연결된 자료' 숫자에 셈 |
| ds/·algo/·os/ `번호/index.html` | 내용요소 공부 노트 템플릿 58장(예: `ds/1-2-4/`). 머리(번호·이름·키워드·세부내용) + 빈 칸 4개(핵심 개념·예제·코드·기출·예상 문제·참고 자료) + 이전·목차·다음. 첫 화면 목차에는 아직 링크 안 함 |
| os/3-1-1·3-1-2·3-1-3·3-1-5·3-1-6·3-2-1·3-2-2·3-2-5·3-2-6 | 위 템플릿과 같으나 '핵심 개념' 칸을 사용자의 `운영체제.hwp` 정리로 채움. 원본과 다르게 고친 곳은 `.fix` 꼬리표. 3-2-6 폴더에 HRN 손글씨 공식 그림 `hrn-aging.jpeg` |
| assets/note.css | 노트 58장이 같이 쓰는 모양. 첫 화면과 같은 레트로 창·색·글꼴, 과목 색은 `body.s-ds/s-algo/s-os` |
| .github/workflows/pages.yml | main에 push하면 index.html·fonts·tools/memo.js·assets·노트 폴더만 Pages에 배포. info-lesson의 같은 파일과 달리 빌드 없이 복사만 |
| tools/memo.js | 피드백 모드 화면 쪽(`?memo=1`). middle school info의 `msi-memo.js`와 같으나 위치를 '과목 › 영역 › 내용요소'로 적음 |
| scripts/serve.mjs | 미리보기 서버(8090) + `/__feedback`. info-lesson 쪽(8080)과 달리 빌드 결과가 아니라 저장소를 직접 보여 주되 index.html·fonts·tools·assets·노트 폴더만 |
| scripts/memo.mjs | `npm run memo` — 서버 켜고 `?memo=1`로 열기. info-lesson 쪽과 달리 빌드 단계 없음 |
| scripts/gen_index.py · scripts/index-data.json | 첫 화면 만들기(`npm run index`). 전에는 세션 임시 폴더에만 있던 생성기를 옮김. 칸이 채워진 노트는 자동 링크 |
| 노트 원고/ (git 제외) | 노트 58개의 Word 원고. 노트 HTML 과 같은 순서(머리 → 핵심 개념·예제·코드·기출·예상 문제·참고 자료). 고친 뒤 "노트 반영해줘" |
| package.json | `npm run serve`, `npm run memo`, `npm run index` (외부 패키지 없음) |
| docs/feedback-mode.md | 피드백 모드 켜기·쓰는 법·기록 형식·처리 순서 |
| fonts/ | 쿠키런 700, 메이플스토리 300·700 (middle school info에서 복사), 넥슨 Lv2 고딕 400 서브셋 (사용자가 받은 TTF 에서 2350자만 추림) |
| .design/style-lock.md | 확정한 색·글꼴·배치 값 |
| .design/decisions.log | 디자인 판단 이유와 반려한 대안 |
| .impeccable/config.json | 디자인 점검 훅이 일부러 둔 모양(굵은 테두리+둥근 모서리, 창 속 상자)을 다시 지적하지 않게 하는 예외 목록. `.design/` 과 달리 사람용 기록이 아니라 점검 도구 설정 |
| README.md | 저장소 소개 + 내용요소에 자료 링크 붙이는 방법 |
| CLAUDE.md | Karpathy 코딩 가이드라인 + 프로젝트 규칙(한글 커밋 메시지) |
| .gitignore | 운영체제·편집기·Python·Node 부산물과 키·비밀번호·토큰 파일 제외 |
| PROJECT_MAP.md | 이 지도 문서 |
| .claude/AGENTS_MAP.md | 이 프로젝트에서 쓴 스킬·에이전트 기록 |
