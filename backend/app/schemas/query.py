from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# fmt: off  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82YmxsclZRPT06NWY4MzE0YmE=

class QueryRequest(BaseModel):
    connection_id: int
    natural_language_query: str
# pragma: no cover  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82YmxsclZRPT06NWY4MzE0YmE=


class QueryResponse(BaseModel):
    sql: str
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    context: Optional[Dict[str, Any]] = None  # For debugging/explanation
