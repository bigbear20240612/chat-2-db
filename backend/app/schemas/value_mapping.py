from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class ValueMappingBase(BaseModel):
    nl_term: str
    db_value: str
# fmt: off  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82Tm5admJnPT06YmFhMTBmMjg=


# Properties to receive on mapping creation
class ValueMappingCreate(ValueMappingBase):
    column_id: int


# Properties to receive on mapping update
class ValueMappingUpdate(BaseModel):
    nl_term: Optional[str] = None
    db_value: Optional[str] = None


# Properties shared by models stored in DB
class ValueMappingInDBBase(ValueMappingBase):
    id: int
    column_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
# type: ignore  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82Tm5admJnPT06YmFhMTBmMjg=


# Properties to return to client
class ValueMapping(ValueMappingInDBBase):
    pass
