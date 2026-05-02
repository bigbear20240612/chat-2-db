from typing import List, Optional
# fmt: off  MC8zOmFIVnBZMlhucUx2b2pZbmt1cm82VkU4d1N3PT06Y2M3NDY5M2Y=

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.schema_relationship import SchemaRelationship
from app.schemas.schema_relationship import SchemaRelationshipCreate, SchemaRelationshipUpdate


class CRUDSchemaRelationship(CRUDBase[SchemaRelationship, SchemaRelationshipCreate, SchemaRelationshipUpdate]):
    def get_by_connection(
        self, db: Session, *, connection_id: int, skip: int = 0, limit: int = 100
    ) -> List[SchemaRelationship]:
        return (
            db.query(SchemaRelationship)
            .filter(SchemaRelationship.connection_id == connection_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
# fmt: off  MS8zOmFIVnBZMlhucUx2b2pZbmt1cm82VkU4d1N3PT06Y2M3NDY5M2Y=

    def get_by_source_table(
        self, db: Session, *, source_table_id: int
    ) -> List[SchemaRelationship]:
        return (
            db.query(SchemaRelationship)
            .filter(SchemaRelationship.source_table_id == source_table_id)
            .all()
        )

    def get_by_target_table(
        self, db: Session, *, target_table_id: int
    ) -> List[SchemaRelationship]:
        return (
            db.query(SchemaRelationship)
            .filter(SchemaRelationship.target_table_id == target_table_id)
            .all()
        )

    def get_by_columns(
        self, db: Session, *, source_column_id: int, target_column_id: int
    ) -> Optional[SchemaRelationship]:
        return (
            db.query(SchemaRelationship)
            .filter(
                SchemaRelationship.source_column_id == source_column_id,
                SchemaRelationship.target_column_id == target_column_id
            )
            .first()
        )

# noqa  Mi8zOmFIVnBZMlhucUx2b2pZbmt1cm82VkU4d1N3PT06Y2M3NDY5M2Y=

schema_relationship = CRUDSchemaRelationship(SchemaRelationship)
