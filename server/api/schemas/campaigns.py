from datetime import datetime
from typing import List, Optional, Set

from pydantic import BaseModel


class Campaign(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    prospects_count: Optional[int]

    class Config:
        orm_mode = True


class CampaignCreate(BaseModel):
    name: str


class CampaignSearch(BaseModel):
    name: str


class CampaignSearchResponse(BaseModel):
    campaigns: List[Campaign]


class CampaignResponse(BaseModel):
    """One page of campaigns"""

    campaigns: List[Campaign]
    size: int
    total: int


class AddToCampaigns(BaseModel):
    prospect_ids: Set[int]


class AddToCampaignsResponse(BaseModel):
    prospect_ids: List[int]
