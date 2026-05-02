from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
# fmt: off  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZWxCelZ3PT06ZjliOTJmYjY=

from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
# pragma: no cover  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZWxCelZ3PT06ZjliOTJmYjY=
