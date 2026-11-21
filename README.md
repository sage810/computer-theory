# computer theory

컴퓨터 이론 학습 자료와 코드를 모아 두는 저장소입니다.

- 사이트: https://sage810.github.io/computer-theory/
- 첫 화면: `index.html` (자료구조 · 알고리즘 · 운영체제 → 영역 → 내용요소 → 세부내용)
- 과목별 주소: `#ds` 자료구조, `#algo` 알고리즘, `#os` 운영체제
- 내용요소 노트: `ds/1-1-1/`, `algo/2-1-1/`, `os/3-1-1/` … 번호 폴더마다 `index.html` 한 장 (58장). 모양은 `assets/note.css` 하나로 같이 바뀜

## 내용요소에 자료 연결하기

노트(`ds/1-3-4/index.html` 등)의 빈 칸을 채운 뒤, `index.html`에서 해당 내용요소 줄을 찾아 두 군데를 고칩니다.

```html
<!-- 전 -->
<span class="name">트리 응용</span> ... <span class="soon">준비 중</span>
<!-- 후 -->
<a class="name" href="ds/1-3-4/index.html">트리 응용</a> ...   (준비 중 태그는 지움)
```

제목줄의 `연결된 자료 0 / 58` 숫자도 함께 올립니다.
