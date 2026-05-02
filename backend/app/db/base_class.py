from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
# pragma: no cover  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82VTJsbE1nPT06ODRjZjIwYmQ=


@as_declarative()
class Base:
    id: Any
    __name__: str
# type: ignore  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82VTJsbE1nPT06ODRjZjIwYmQ=
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
