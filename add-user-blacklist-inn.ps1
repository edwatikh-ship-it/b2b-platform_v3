# add-user-blacklist-inn.ps1
# Adds user blacklist by INN to api-contracts.yaml (SSoT).
# Writes UTF-8 without BOM.

$contractPath = "D:\b2bplatform\api-contracts.yaml"

if (-not (Test-Path $contractPath)) {
  throw "api-contracts.yaml not found at: $contractPath"
}

$content = Get-Content -Path $contractPath -Raw -Encoding UTF8

if ($content -match "/user/blacklist-inn:") {
  Write-Host "SKIP: /user/blacklist-inn already exists in api-contracts.yaml" -ForegroundColor Yellow
  exit 0
}

$newPaths = @'

  /user/blacklist-inn:
    get:
      tags:
      - UserBlacklist
      summary: List User Blacklist Inn
      operationId: list_user_blacklist_inn_apiv1_user_blacklist_inn_get
      parameters:
      - name: limit
        in: query
        required: false
        schema:
          type: integer
          default: 200
          title: Limit
      - name: offset
        in: query
        required: false
        schema:
          type: integer
          default: 0
          title: Offset
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserBlacklistInnListResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
    post:
      tags:
      - UserBlacklist
      summary: Add User Blacklist Inn
      operationId: add_user_blacklist_inn_apiv1_user_blacklist_inn_post
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AddUserBlacklistInnRequest'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GenericOkResponseDTO'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
  /user/blacklist-inn/{inn}:
    delete:
      tags:
      - UserBlacklist
      summary: Delete User Blacklist Inn
      operationId: delete_user_blacklist_inn_apiv1_user_blacklist_inn__inn__delete
      parameters:
      - name: inn
        in: path
        required: true
        schema:
          type: string
          title: Inn
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GenericOkResponseDTO'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'

'@

$newSchemas = @'
    AddUserBlacklistInnRequest:
      type: object
      properties:
        inn:
          type: string
          minLength: 10
          maxLength: 12
          title: Inn
        comment:
          anyOf:
          - type: string
          - type: null
          title: Comment
      required:
      - inn
      additionalProperties: false
    UserBlacklistInnItem:
      type: object
      properties:
        inn:
          type: string
          title: Inn
        comment:
          anyOf:
          - type: string
          - type: null
          title: Comment
        created_at:
          type: string
          title: Created At
      required:
      - inn
      - created_at
      additionalProperties: false
    UserBlacklistInnListResponse:
      type: object
      properties:
        items:
          type: array
          items:
            $ref: '#/components/schemas/UserBlacklistInnItem'
          title: Items
        limit:
          type: integer
          title: Limit
        offset:
          type: integer
          title: Offset
        total:
          type: integer
          title: Total
      required:
      - items
      - limit
      - offset
      - total
      additionalProperties: false
'@

if ($content -notmatch "(?m)^\s*/auth/otp/request:") { throw "Anchor '/auth/otp/request:' not found." }
$content = $content -replace "(?m)^\s*/auth/otp/request:", "$newPaths
  /auth/otp/request:"

if ($content -notmatch "(?m)^\s*ValidationError:") { throw "Anchor 'ValidationError:' not found." }
$content = $content -replace "(?m)^\s*ValidationError:", "$newSchemas
    ValidationError:"

[System.IO.File]::WriteAllText($contractPath, $content, (New-Object System.Text.UTF8Encoding $false))
Write-Host "OK: api-contracts.yaml updated with user blacklist by INN." -ForegroundColor Green