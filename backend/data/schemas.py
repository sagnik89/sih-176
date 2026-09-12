from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DataRecord(BaseModel):
    """Generic normalized marine observation."""

    id: int
    region: str

    latitude: float
    longitude: float

    timestamp: str

    data_source: str = "SYNTHETIC_DEMO_DATA"


class AgentEvidence(BaseModel):
    """Evidence returned by a specialized ORCA agent."""

    agent: str
    status: str = "success"

    region: Optional[str] = None

    findings: List[str] = Field(default_factory=list)

    metrics: Dict[str, Any] = Field(
        default_factory=dict
    )

    evidence: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    confidence: float = 0.0

    data_source: str = "SYNTHETIC_DEMO_DATA"


class RiskAssessment(BaseModel):
    """Ecological risk assessment."""

    level: str
    score: float

    explanation: str = ""

    contributing_factors: List[str] = Field(
        default_factory=list
    )


class ORCAResponse(BaseModel):
    """Final structured response returned by ORCA."""

    query: str

    region: Optional[str] = None

    answer: str = ""

    risk: Optional[RiskAssessment] = None

    findings: List[str] = Field(
        default_factory=list
    )

    evidence: List[AgentEvidence] = Field(
        default_factory=list
    )

    agents_used: List[str] = Field(
        default_factory=list
    )

    model_used: Optional[str] = None

    data_mode: str = "SYNTHETIC_DEMO_DATA"