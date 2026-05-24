# 증거 저장소

이 디렉터리는 다른 wiki 문서가 근거로 삼는 원천 자료와 실행 provenance를 저장한다.

- `sources/`: 수정하지 않는 원천 캡처 자료.
- `run-manifests/`: machine-readable 실행 manifest.

Raw source notes are immutable records of evidence used by the trading wiki. Each source should be captured once in `wiki/evidence-store/sources/` with source metadata, summary, and ticker references.

Do not edit raw source notes after capture except to fix formatting that prevents parsing.
