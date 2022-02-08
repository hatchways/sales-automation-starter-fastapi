from typing import List, Set, Union
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from api import schemas
from api.models import Campaign, CampaignProspect
from api.core.constants import DEFAULT_PAGE_SIZE, DEFAULT_PAGE, MIN_PAGE, MAX_PAGE_SIZE

MAX_SEARCH_RESULTS = 10


class CampaignCrud:
    @classmethod
    def get_users_campaign(
        cls,
        db: Session,
        user_id: int,
        page: int = DEFAULT_PAGE,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Union[List[schemas.Campaign], None]:
        """Get user's campaigns"""
        if page < MIN_PAGE:
            page = MIN_PAGE
        if page_size > MAX_PAGE_SIZE:
            page_size = MAX_PAGE_SIZE
        res = (
            db.query(Campaign)
            .filter(
                Campaign.user_id == user_id,
            )
            .offset(page * page_size)
            .limit(page_size)
            .all()
        )
        return res

    @classmethod
    def get_user_campaign_total(cls, db: Session, user_id: int) -> int:
        return db.query(Campaign).filter(Campaign.user_id == user_id).count()

    @classmethod
    def get_user_campaign_from_name_fragment(
        cls, db: Session, user_id: int, name_fragment: str
    ) -> Union[List[Campaign], None]:
        return (
            db.query(Campaign)
            .filter(
                Campaign.user_id == user_id, Campaign.name.ilike(f"%{name_fragment}%")
            )
            .limit(MAX_SEARCH_RESULTS)
            .all()
        )

    @classmethod
    def create_campaign(
        cls, db: Session, user_id: int, data: schemas.CampaignCreate
    ) -> Campaign:
        """Create a user"""
        campaign = Campaign(name=data.name, user_id=user_id)
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign

    @classmethod
    def get_existing_campaign_prospects(cls, db: Session, campaign_id: int) -> Set[int]:
        res = (
            db.query(CampaignProspect.prospect_id)
            .filter(CampaignProspect.campaign_id == campaign_id)
            .all()
        )
        return {row.prospect_id for row in res}

    @classmethod
    def add_prospects_to_campaign(
        cls, db: Session, campaign_id: int, prospect_ids: Set[int]
    ):
        links = [
            CampaignProspect(campaign_id=campaign_id, prospect_id=prospect_id)
            for prospect_id in prospect_ids
        ]
        db.add_all(links)
        db.commit()

    @classmethod
    def get_by_id(cls, db: Session, campaign_id: int) -> Union[Campaign, None]:
        """Get a single user by id"""
        return db.query(Campaign).filter(Campaign.id == campaign_id).one_or_none()
