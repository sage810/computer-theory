# PROJECT_MAP

이 저장소에 어떤 파일이 있고 무엇이 달라졌는지 적는 지도입니다.

## 파일 목록

| 파일 | 설명 |
|---|---|
| index.html | 첫 화면(GitHub Pages). info-lesson 첫 화면과 레트로 창 겉모습은 같으나, 단원 세로 칸 대신 맨 위 과목 탭 + 영역별 트리 개요(`1.1.1`, `#키워드`) + 세부내용 접고 펴기 |
| .github/workflows/pages.yml | main에 push하면 index.html·fonts·tools/memo.js만 Pages에 배포. info-lesson의 같은 파일과 달리 빌드 없이 복사만 |
| tools/memo.js | 피드백 모드 화면 쪽(`?memo=1`). middle school info의 `msi-memo.js`와 같으나 위치를 '과목 › 영역 › 내용요소'로 적음 |
| scripts/serve.mjs | 미리보기 서버(8090) + `/__feedback`. info-lesson 쪽(8080)과 달리 빌드 결과가 아니라 저장소를 직접 보여 주되 index.html·fonts·tools만 |
| scripts/memo.mjs | `npm run memo` — 서버 켜고 `?memo=1`로 열기. info-lesson 쪽과 달리 빌드 단계 없음 |
| package.json | `npm run serve`, `npm run memo` (외부 패키지 없음) |
| docs/feedback-mode.md | 피드백 모드 켜기·쓰는 법·기록 형식·처리 순서 |
| fonts/ | 쿠키런 700, 메이플스토리 300·700 글꼴. middle school info의 `shared/fonts/`에서 복사 |
| .design/style-lock.md | 확정한 색·글꼴·배치 값 |
| .design/decisions.log | 디자인 판단 이유와 반려한 대안 |
| README.md | 저장소 소개 + 내용요소에 자료 링크 붙이는 방법 |
| CLAUDE.md | Karpathy 코딩 가이드라인 + 프로젝트 규칙(한글 커밋 메시지) |
| .gitignore | 운영체제·편집기·Python·Node 부산물과 키·비밀번호·토큰 파일 제외 |
| PROJECT_MAP.md | 이 지도 문서 |
| .claude/AGENTS_MAP.md | 이 프로젝트에서 쓴 스킬·에이전트 기록 |
