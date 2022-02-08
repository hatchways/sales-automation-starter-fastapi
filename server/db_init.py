import sys
from typing import List
from sqlalchemy import MetaData
from sqlalchemy.sql.schema import Table

from api.database import Base, engine
from api.models import User, Prospect, Campaign, CampaignProspect


if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1 and args[1] == "drop":
        ordered_drop: List[Table] = [
            CampaignProspect.__table__,
            Campaign.__table__,
            Prospect.__table__,
            User.__table__,
        ]
        print("\n-- Dropping All Tables --")
        for t in ordered_drop:
            print(f"...{t.name}")
        Base.metadata.drop_all(bind=engine, tables=ordered_drop)

    print("\n-- Creating Tables --")
    metadata: MetaData = Base.metadata
    metadata.create_all(bind=engine)
    # Note: order of table creation depends on import order in api/models/__init__.py
    for t in metadata.tables:
        print(f"...{t}")
