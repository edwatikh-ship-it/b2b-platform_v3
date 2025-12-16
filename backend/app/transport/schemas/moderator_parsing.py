"""
Moderator parsing DTOs.
SSoT: api-contracts.yaml (StartParsingResponseDTO, ParsingStatusResponseDTO, ParsingResultsResponseDTO).
"""

from enum import Enum

from pydantic import BaseModel, Field


class ParsingRunStatus(str, Enum):
    """SSoT: api-contracts.yaml#/components/schemas/ParsingRunStatus"""

    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"


class StartParsingResponseDTO(BaseModel):
    """SSoT: api-contracts.yaml#/components/schemas/StartParsingResponseDTO"""

    requestId: int = Field(..., alias="requestId")
    runId: str = Field(..., alias="runId")
    status: ParsingRunStatus

    class Config:
        populate_by_name = True


class StartParsingRequestDTO(BaseModel):
    depth: int = Field(10, ge=1, le=50)
    resume: bool = Field(True)


class ParsingKeyStatusDTO(BaseModel):
    """SSoT: api-contracts.yaml#/components/schemas/ParsingKeyStatusDTO"""

    keyId: int = Field(..., alias="keyId")
    status: ParsingRunStatus
    itemsFound: int = Field(..., ge=0, alias="itemsFound")
    error: str | None = None

    class Config:
        populate_by_name = True


class ParsingStatusResponseDTO(BaseModel):
    """SSoT: api-contracts.yaml#/components/schemas/ParsingStatusResponseDTO"""

    requestId: int = Field(..., alias="requestId")
    runId: str = Field(..., alias="runId")
    status: ParsingRunStatus
    keys: list[ParsingKeyStatusDTO]

    class Config:
        populate_by_name = True


class ParsingSource(str, Enum):
    """SSoT: api-contracts.yaml#/components/schemas/ParsingSource"""

    google = "google"
    yandex = "yandex"


class ParsingDomainGroupDTO(BaseModel):
    """SSoT: api-contracts.yaml#/components/schemas/ParsingDomainGroupDTO"""

    domain: str
    urls: list[str]
    source: ParsingSource | None = None
    title: str | None = None

    class Config:
        populate_by_name = True


class ParsingResultsByKeyDTO(BaseModel):
    """SSoT: api-contracts.yaml#/components/schemas/ParsingResultsByKeyDTO"""

    keyId: int = Field(..., alias="keyId")
    groups: list[ParsingDomainGroupDTO]

    class Config:
        populate_by_name = True


class ParsingResultsResponseDTO(BaseModel):
    """SSoT: api-contracts.yaml#/components/schemas/ParsingResultsResponseDTO"""

    requestId: int = Field(..., alias="requestId")
    runId: str = Field(..., alias="runId")
    results: list[ParsingResultsByKeyDTO]

    class Config:
        populate_by_name = True
