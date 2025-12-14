from pydantic import BaseModel, Field


class AddUserBlacklistInnRequestDTO(BaseModel):
    inn: str = Field(min_length=10, max_length=12)
    reason: str | None = None


class UserBlacklistInnItemDTO(BaseModel):
    id: int
    inn: str
    supplierid: int | None = None
    suppliername: str | None = None
    checkodata: dict | None = None
    reason: str | None = None
    createdat: str


class UserBlacklistInnListResponseDTO(BaseModel):
    items: list[UserBlacklistInnItemDTO]