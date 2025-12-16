import re
from pathlib import Path

path = Path(r"D:\b2bplatform\api-contracts.yaml")
src = path.read_text(encoding="utf-8")


# 1) Ensure paths exist
def ensure_path_block(yaml_text: str, path_key: str, block: str) -> str:
    if re.search(rf"(?m)^{re.escape(path_key)}:\s*$", yaml_text):
        return yaml_text
    # insert after "paths:" line
    m = re.search(r"(?m)^paths:\s*$", yaml_text)
    if not m:
        raise SystemExit("Cannot find top-level 'paths:' in api-contracts.yaml")
    insert_at = m.end()
    return yaml_text[:insert_at] + "\n\n" + block.strip() + "\n" + yaml_text[insert_at:]


start_parsing_path = r"""/moderator/requests/{requestId}/start-parsing:
  post:
    tags:
    - ModeratorTasks
    summary: Start Parsing
    operationId: start_parsing_apiv1_moderator_requests__requestId__start_parsing_post
    parameters:
    - name: requestId
      in: path
      required: true
      schema:
        type: integer
        title: Requestid
    requestBody:
      required: false
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/StartParsingRequestDTO'
    responses:
      '200':
        description: Successful Response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StartParsingResponseDTO'
      '422':
        description: Validation Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HTTPValidationError'
"""

status_path = r"""/moderator/requests/{requestId}/parsing-status:
  get:
    tags:
    - ModeratorTasks
    summary: Get Parsing Status
    operationId: get_parsing_status_apiv1_moderator_requests__requestId__parsing_status_get
    parameters:
    - name: requestId
      in: path
      required: true
      schema:
        type: integer
        title: Requestid
    responses:
      '200':
        description: Successful Response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ParsingStatusResponseDTO'
      '422':
        description: Validation Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HTTPValidationError'
"""

results_path = r"""/moderator/requests/{requestId}/parsing-results:
  get:
    tags:
    - ModeratorTasks
    summary: Get Parsing Results
    operationId: get_parsing_results_apiv1_moderator_requests__requestId__parsing_results_get
    parameters:
    - name: requestId
      in: path
      required: true
      schema:
        type: integer
        title: Requestid
    responses:
      '200':
        description: Successful Response
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ParsingResultsResponseDTO'
      '422':
        description: Validation Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HTTPValidationError'
"""

src = ensure_path_block(
    src, "/moderator/requests/{requestId}/start-parsing", start_parsing_path
)
src = ensure_path_block(
    src, "/moderator/requests/{requestId}/parsing-status", status_path
)
src = ensure_path_block(
    src, "/moderator/requests/{requestId}/parsing-results", results_path
)


# 2) Ensure component schemas exist (append if missing)
def ensure_schema(yaml_text: str, name: str, schema_block: str) -> str:
    if re.search(rf"(?m)^\s{{2}}{re.escape(name)}:\s*$", yaml_text):
        return yaml_text
    m = re.search(r"(?m)^components:\s*$", yaml_text)
    if not m:
        raise SystemExit("Cannot find top-level 'components:' in api-contracts.yaml")
    # find components/schemas:
    # safest: just ensure "  schemas:" exists, else create it at end of file
    if not re.search(r"(?m)^\s{2}schemas:\s*$", yaml_text):
        yaml_text = yaml_text.rstrip() + "\n\ncomponents:\n  schemas:\n"
    # append under schemas at end (simple but deterministic)
    return yaml_text.rstrip() + "\n\n" + schema_block.strip() + "\n"


schemas_to_add = r"""
  StartParsingRequestDTO:
    type: object
    additionalProperties: false
    properties:
      keys:
        type: array
        description: Optional filter. If omitted, parse all keys of the request.
        items:
          type: integer
    required: []

  StartParsingResponseDTO:
    type: object
    additionalProperties: false
    properties:
      requestId:
        type: integer
      started:
        type: boolean
      runId:
        type: string
        description: Parser run identifier (opaque).
    required: [requestId, started, runId]

  ParsingRunStatus:
    type: string
    enum: [queued, running, succeeded, failed]

  ParsingKeyStatusDTO:
    type: object
    additionalProperties: false
    properties:
      keyId:
        type: integer
      status:
        $ref: '#/components/schemas/ParsingRunStatus'
      itemsFound:
        type: integer
        minimum: 0
      error:
        type: string
        nullable: true
    required: [keyId, status, itemsFound, error]

  ParsingStatusResponseDTO:
    type: object
    additionalProperties: false
    properties:
      requestId:
        type: integer
      runId:
        type: string
      status:
        $ref: '#/components/schemas/ParsingRunStatus'
      keys:
        type: array
        items:
          $ref: '#/components/schemas/ParsingKeyStatusDTO'
    required: [requestId, runId, status, keys]

  ParsingResultItemDTO:
    type: object
    additionalProperties: false
    properties:
      url:
        type: string
      domain:
        type: string
      source:
        type: string
        enum: [google, yandex]
      title:
        type: string
        nullable: true
    required: [url, domain, source, title]

  ParsingResultsByKeyDTO:
    type: object
    additionalProperties: false
    properties:
      keyId:
        type: integer
      items:
        type: array
        items:
          $ref: '#/components/schemas/ParsingResultItemDTO'
    required: [keyId, items]

  ParsingResultsResponseDTO:
    type: object
    additionalProperties: false
    properties:
      requestId:
        type: integer
      runId:
        type: string
      results:
        type: array
        items:
          $ref: '#/components/schemas/ParsingResultsByKeyDTO'
    required: [requestId, runId, results]
"""

for schema_name in [
    "StartParsingRequestDTO",
    "StartParsingResponseDTO",
    "ParsingRunStatus",
    "ParsingKeyStatusDTO",
    "ParsingStatusResponseDTO",
    "ParsingResultItemDTO",
    "ParsingResultsByKeyDTO",
    "ParsingResultsResponseDTO",
]:
    pass

src = ensure_schema(src, "StartParsingRequestDTO", schemas_to_add)

path.write_text(src, encoding="utf-8")
print("Patched api-contracts.yaml OK")
