# Agent Dashboard

`agent-dashboard.html`은 서버 없이 여는 정적 상태판이다.

최신 run을 반영하려면 작업이 끝난 뒤 아래 명령을 실행한다.

```bash
python3 scripts/build-agent-dashboard.py
```

생성된 HTML은 브라우저에서 바로 열 수 있다. Backtests 카드는 원본 Markdown 파일이 아니라 `ui/backtests/*.html`로 생성된 보기용 HTML 문서를 연다.
