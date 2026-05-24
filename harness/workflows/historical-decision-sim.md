# Workflow: 과거 시점 추천 시뮬레이션

사용자가 `2026-05-22 기준으로 추천 시뮬레이션해줘`, `과거 시점 추천해줘`, `YYYY-MM-DD 기준 매수/매도 추천해줘`처럼 특정 과거 기준일의 추천을 요청할 때 사용한다.

## 목표

과거 특정 시점으로 돌아가 그때 알 수 있었던 정보만으로 종목별 `매수`, `보유`, `축소`, `매도`, `관망` 판단과 수량을 추천한다. 이 워크플로우는 학습용 시뮬레이션이며 실제 주문을 제출하지 않는다.

## 핵심 원칙

- 미래 정보 누출을 금지한다. 추천 문서와 raw source에는 기준 시점 이후 가격, 뉴스, 체결 결과를 넣지 않는다.
- 날짜만 주어지면 해당 미국 정규 거래일 종가 기준으로 해석한다.
- 정확한 시각이 주어지면 그 시각 이전 데이터만 사용한다.
- 후보군 기본값은 기준 시점 위키, raw source, order plan, portfolio 기록에 등장한 보유 종목과 watchlist/후보 종목이다.
- 현재 watchlist는 기준 시점에 기록되어 있지 않으면 strict mode 후보군에 넣지 않는다.
- 주문 계획은 항상 `dry_run`으로만 만들고, Alpaca MCP 주문 제출 도구를 호출하지 않는다.

## 필수 입력

- `AGENTS.md`, `harness/risk-policy.md`, `wiki/index.md`, 최근 `wiki/log.md`.
- 기준 시점 이전 또는 기준 시점에 생성된 daily report, ticker pages, order plans, portfolio snapshots, raw source notes.
- 기준 시점 이전 Alpaca MCP stock bars, news, account/order/activity data. MCP가 특정 과거 데이터를 제공하지 못하면 로컬 raw source와 위키 기록을 우선 사용한다.
- 기준 시점 이전 research MCP 데이터. `harness/mcp-source-map.md`에 따라 SEC filings, 실적 캘린더, macro series, IR/press release 캡처를 사용하되 기준 시점 이후 정보는 제외한다.
- 기준 시점 당시 적용 가능했던 `wiki/policy-book/recommendation-policy.md`.

## 필수 산출물

- `wiki/backtest-runs/decisions/YYYY-MM-DD-historical-decision.md`
- `wiki/evidence-store/sources/YYYY-MM-DD-historical-asof.md`
- `wiki/trade-ledger/orders/YYYY-MM-DD-historical-decision.json`
- `wiki/index.md` 업데이트
- `wiki/log.md` append-only 항목 추가

## 절차

1. 기준 시점을 확정한다.
   - 날짜만 있으면 미국 정규장 종가 기준으로 기록한다.
   - 기준일이 휴장일이면 가장 가까운 직전 미국 정규 거래일을 기준으로 삼고 이유를 기록한다.
2. 기준 시점에 사용 가능한 후보군을 복원한다.
   - 당시 보유 종목.
   - 당시 order plan, ticker page, daily report, raw source에 등장한 후보 종목.
   - 당시 watchlist가 raw source에 기록되어 있으면 포함한다.
   - 비교용 벤치마크로 SPY, QQQ, 관련 섹터 ETF를 추가하되 주문 후보와 구분한다.
3. 과거 기준 원천 자료를 캡처한다.
   - Alpaca MCP `get_stock_bars`로 기준 시점 이전 1D, 5D, 20D, 60D 가격 흐름을 수집한다.
   - Alpaca MCP `get_news`로 기준 시점 이전 뉴스만 수집한다.
   - `sec-edgar`로 기준 시점 이전 filings와 insider/form 이벤트만 확인한다.
   - `alpha-vantage`로 기준 시점 이전에 알려진 실적 캘린더/earnings 정보를 확인한다. 키가 없으면 공백을 기록한다.
   - `fred`로 기준 시점 이전에 공개된 매크로 지표만 확인한다. 발표일이 기준 시점 이후인 값은 제외한다.
   - `firecrawl`로 기준 시점 이전 회사 IR/보도자료/earnings presentation URL만 캡처한다. 키가 없으면 공백을 기록한다.
   - `yahoo-finance`로 기준 시점 이전 Yahoo 뉴스/analyst 보조 정보를 확인한다.
   - 당시 portfolio/order/activity 정보는 위키 기록과 Alpaca MCP 가능한 범위에서 복원한다.
   - 캡처 결과를 `wiki/evidence-store/sources/YYYY-MM-DD-historical-asof.md`에 저장한다.
4. 각 후보를 점수화한다.
   - 추세와 상대강도: 35점.
   - 뉴스/촉매/펀더멘털 맥락: 25점.
   - 리스크/유동성/변동성 품질: 20점.
   - 포트폴리오 적합성/테마 분산: 20점.
   - 당시 추천 정책과 충돌하면 점수와 비중을 낮춘다.
   - 뉴스-가격 선후관계를 기준 시점 정보만으로 분류한다.
     - 기준 시점 이전 뉴스는 `news_type`, `pre_news_3d_return`, `pre_news_5d_return`, `event_day_return`을 기록한다.
     - 기준 시점 이후 `post_news_1d_return`, `post_news_5d_return`은 추천 문서에 넣지 않고 회고 문서에서만 계산한다.
     - 좋은 뉴스 전 이미 3D/5D 급등한 후보는 `price-led` 또는 `sell-the-news-risk`로 감점한다.
     - 정책/테마 뉴스는 당일 급등만으로 매수 승격하지 않고, 기준 시점에서 후속 유지가 확인되지 않으면 소액 또는 관망 처리한다.
5. 판단과 수량을 만든다.
   - 라벨은 `매수`, `보유`, `축소`, `매도`, `관망` 중 하나만 사용한다.
   - 수량은 당시 portfolio value, cash, 보유 수량, medium risk policy 기준으로 whole-share로 계산한다.
   - `매수`와 `축소/매도`만 dry-run order plan에 넣는다.
6. 주문 계획 JSON을 만든다.
   - `mode`는 항상 `dry_run`.
   - `paper`는 `true`.
   - `schema_version`, `risk_policy_version`, `recommendation_policy_sha`, `created_at`, root `source_refs`를 포함한다.
   - 각 주문에는 `decision_id`, `historical_asof`, `review_horizons`, `rationale`, `quote_captured_at`, `asset_checked_at`, `source_refs`를 포함한다.
   - `scripts/check-risk-policy.py --json`로 검증한다.
   - 추천 문서와 주문 계획을 `scripts/check-leakage.py --asof <기준시점>`로 점검한다.
7. 추천 문서를 작성한다.
   - 기준 시점, 후보군 복원 근거, 사용 가능한 데이터와 누락 데이터.
   - 후보별 점수, 판단, 수량, 목표 비중, 리스크.
   - 1D/5D/20D 회고 예정일.
   - 미래 정보 미사용 선언.
8. `wiki/index.md`와 `wiki/log.md`를 업데이트한다.

## 금지 사항

- `place_stock_order`, `replace_order_by_id`, `cancel_order_by_id`, `close_position`, `close_all_positions` 등 실제 계좌 상태를 바꾸는 Alpaca 도구를 호출하지 않는다.
- 기준 시점 이후 가격을 추천 문서에 넣지 않는다.
- 과거 raw source나 당시 thesis를 수정해 사후적으로 더 좋아 보이게 만들지 않는다.

## 검증 기준

- 추천 문서에 기준 시점 이후 날짜의 가격/뉴스가 없어야 한다.
- dry-run order plan이 `scripts/check-risk-policy.py`를 통과하거나 실패 사유를 명확히 기록해야 한다.
- 가능한 경우 `scripts/check-leakage.py`를 통과해야 하며, 실패하면 추천 문서를 확정하지 않는다.
- 후보군에 포함된 종목은 기준 시점 위키 또는 raw source에서 등장 근거가 있어야 한다.
