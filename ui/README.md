# Agent Dashboard

`agent-dashboard.html`은 서버 없이 여는 정적 상태판이다. 최신 run 상태와 `wiki/trade-ledger/positions/current.md`의 Alpaca paper 투자 현황을 함께 보여준다.

최신 run을 반영하려면 작업이 끝난 뒤 아래 명령을 실행한다.

```bash
python3 scripts/build-agent-dashboard.py
```

생성된 HTML은 브라우저에서 바로 열 수 있다. `Alpaca Paper` 영역은 평가금액, 총 수익, 투자 노출, 현금, 주요 보유 종목을 간단히 보여준다. Backtests 카드는 원본 Markdown 파일이 아니라 `ui/backtests/*.html`로 생성된 보기용 HTML 문서를 연다.
