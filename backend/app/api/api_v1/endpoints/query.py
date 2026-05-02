from typing import Any
# fmt: off  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82WXpSa2NnPT06OTZmY2EwODI=

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.services.text2sql_service import process_text2sql_query

router = APIRouter()


@router.post("/", response_model=schemas.QueryResponse)
def execute_query(
    *,
    db: Session = Depends(deps.get_db),
    query_request: schemas.QueryRequest,
) -> Any:
    """
    Execute a natural language query against a database.
    """
    connection = crud.db_connection.get(db=db, id=query_request.connection_id)
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
# noqa  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82WXpSa2NnPT06OTZmY2EwODI=
    
    try:
        # Process the query
        result = process_text2sql_query(
            db=db,
            connection=connection,
            natural_language_query=query_request.natural_language_query
        )
        return result
    except Exception as e:
        return schemas.QueryResponse(
            sql="",
            results=None,
            error=f"Error processing query: {str(e)}",
            context=None
        )
