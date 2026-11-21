<!-- 출처: https://github.com/multica-ai/andrej-karpathy-skills (CLAUDE.md) -->

# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 프로젝트 규칙

### 이력관리 (git)

- 커밋 메시지는 **한글**로 작성한다.
- 형식: 첫 줄에 `요약: 핵심 내용`을 쓰고, 필요하면 한 줄 띄운 뒤 상세 설명을 쓴다.
  - 예: `CLAUDE.md 추가: Karpathy 코딩 가이드라인 적용`

### 피드백 모드 (수정 요청 메모)

- **"피드백 모드"** 또는 **"메모 켜줘"** → `npm run memo` 를 실행해 켠다. 과목을 말하면 `npm run memo -- ds|algo|os`.
  끝나면 열린 주소 한 줄과 쓰는 법(글 드래그 또는 🎯 요소 고르기 → 📝 메모 → 요청 적기 → 📤 보내기 → "피드백 처리해줘")을 알린다.
- **"피드백 처리해줘"** → `.claude/feedback.md` 의 `[ ]` 항목을 `docs/feedback-mode.md` 4절 순서대로 처리한다(최소 diff, 끝나면 `[x]` + 한 줄).
- **세션 시작 때 `.claude/feedback.md` 에 `[ ]` 항목이 있으면 먼저 알린다.**
- 붙여넣은 `[수정 요청]` 글(GitHub Pages 에서 복사한 것)도 같은 순서로 처리한다.
- "메모 꺼줘" → 주소 끝을 `?memo=0` 으로 열게 안내한다(서버는 끌 필요 없다).
- 설명서: `docs/feedback-mode.md`

### 노트 원고 (Word → 노트 반영)

- 노트마다 Word 원고가 `노트 원고/<과목>/<번호> <이름>.docx` 에 있다(예: `노트 원고/운영체제/3-1-1 운영체제 목적, 역할.docx`). **git 에 올리지 않는다**(Word 작성자 이름이 들어감, `.gitignore`).
- 원고 서식(2026-11-21, 사용자가 만든 3.1.1 원고 기준): 제목(`번호 이름`) → 위치 줄(·#키워드·└ 세부내용) → **제목 1 = 칸 이름**(보통 내용요소 이름이나 주제) → 글머리 목록 하나(첫 단계 굵게 = 묶음, 그 아래 `**용어** : 설명`, 더 아래 설명) · 그림 · 표. 빈 원고는 글머리 한 줄 '아직 비어 있어요.'
- 사용자가 Word 를 고치고 **"3-1-1 노트 반영해줘"**(또는 "노트 반영해줘" + 과목·번호)라고 하면:
  1. `python -I scripts/note_sync.py "노트 원고/<과목>/<번호> ….docx" <과목id>/<번호>` 로 반영한다. 노트의 공부 칸만 바뀌고(머리·이전/다음 그대로), 그림은 노트 폴더 `fig-1.png …`, 분홍 `[원본과 다름 …]` → `<span class="fix">`, 굵게 → `<strong>`. 파일이 Word 에 열려 있어 읽기가 막히면 사본을 만들어 읽거나 닫아 달라고 한다.
  2. 그림 설명(alt)은 원고의 '대체 텍스트'를 쓰고, 없으면 그림을 보고 직접 적는다(기본값 '그림' 그대로 두지 않는다).
  3. 원고 제목이 노트 제목과 다르면 스크립트가 알린다 → 목차 이름도 바꿀지 사용자에게 묻고, 바꾸면 `scripts/index-data.json`·노트 머리·이웃 노트의 이전/다음 글자를 함께 고친다(엑셀 원본과 어긋남을 알림).
  4. `npm run index` 로 첫 화면을 다시 만든다(칸이 하나라도 채워진 노트는 자동 링크, '연결된 자료' 숫자와 왼쪽 목차 데이터 `assets/toc.js` 갱신). 미리보기(8090)로 확인하고 커밋. push 는 요청할 때만.
- 노트(HTML)를 직접 고친 경우 Word 원고와 어긋나므로, 고친 뒤 Word 도 맞춰 둘지 사용자에게 묻는다.
