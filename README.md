# Rotational Prime Ontology

A deterministic, auditable decision architecture for public safety, child welfare, risk management, and AI governance.

## Structure

- `ontology/` — prime encoding, rotational operators, temporal memory, state transitions, and risk projection
- `api/` — FastAPI integration (`/health` and `/evaluate`)
- `docs/` — specification and API documentation
- `examples/` — representative input scenarios
- `tests/` — deterministic unit tests

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn api.server:app --reload
```

Then open `http://localhost:8000/docs` for the interactive API documentation.

Run tests with:

```bash
pytest
```

## API example

```bash
curl -X POST http://localhost:8000/evaluate \
  -H 'content-type: application/json' \
  -d '{"domain":"public_safety","factors":[{"name":"threat","value":0.8,"weight":1}],"constraints":["legal_compliance"]}'
```

This scaffold is a development foundation, not an automated decision-maker. Production use requires domain validation, human oversight, security controls, privacy review, and documented governance.

## License

MIT. See `LICENSE`.
