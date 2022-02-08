from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, Integer

from api.database import Base


class CampaignProspect(Base):
    """Links Prospects to Campaigns"""

    __tablename__ = "campaigns_prospects"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    campaign_id = Column(BigInteger, ForeignKey("campaigns.id"))
    prospect_id = Column(BigInteger, ForeignKey("prospects.id"))

    prospect = relationship("Prospect", foreign_keys=[prospect_id])
    campaign = relationship("Campaign", foreign_keys=[campaign_id])
