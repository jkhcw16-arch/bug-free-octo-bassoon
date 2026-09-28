"""FastAPI adapter for the ontology engine."""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from ontology.projection import ProtectionProjector, RiskAnalyzer

app = FastAPI(title="Rotational Prime Ontology API", version="0.1.0")
_analyzer = RiskAnalyzer()
_projector = ProtectionProjector()


class EvaluationRequest(BaseModel):
    domain: str = Field(min_length=1)
    factors: list[dict] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/evaluate")
def evaluate(request: EvaluationRequest) -> dict:
    result = _analyzer.analyze(request.factors)
    return {"domain": request.domain, "risk": result.__dict__, "projection": _projector.project(result, request.constraints)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
