from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.domain.ports_auth import OtpRepositoryPort, OtpSenderPort


@dataclass(frozen=True)
class RequestOtpConfig:
    ttl_minutes: int = 10
    max_attempts: int = 5


@dataclass(frozen=True)
class RequestOtpUseCase:
    otp_repo: OtpRepositoryPort
    otp_sender: OtpSenderPort
    cfg: RequestOtpConfig = RequestOtpConfig()

    async def execute(self, email: str) -> None:
        code = f"{secrets.randbelow(1_000_000):06d}"
        codehash = hashlib.sha256(code.encode("utf-8")).hexdigest()
        expiresat = datetime.now(timezone.utc) + timedelta(minutes=int(self.cfg.ttl_minutes))
        await self.otp_repo.create(email=email, codehash=codehash, expiresat=expiresat, maxattempts=int(self.cfg.max_attempts))
        await self.otp_sender.send_code(email=email, code=code)