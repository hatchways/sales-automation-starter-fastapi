from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse

from api import schemas
from api.dependencies.auth import get_current_user
from api.core.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from api.crud import CampaignCrud, ProspectCrud
from api.dependencies.db import get_db

router = APIRouter(prefix="/api", tags=["campaigns"])


@router.get("/campaigns", response_model=schemas.CampaignResponse)
def get_campaign_page(
    current_user: schemas.User = Depends(get_current_user),
    page: int = DEFAULT_PAGE,
    page_size: int = DEFAULT_PAGE_SIZE,
    db: Session = Depends(get_db),
):
    """Get a single page of campaigns"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in"
        )
    campaigns = CampaignCrud.get_users_campaign(db, current_user.id, page, page_size)
    total = CampaignCrud.get_user_campaign_total(db, current_user.id)
    return {"campaigns": campaigns, "size": len(campaigns), "total": total}


@router.get("/campaigns/search", response_model=schemas.CampaignSearchResponse)
def search_campaigns(
    query: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Search campaigns by name"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in"
        )
    campaigns = CampaignCrud.get_user_campaign_from_name_fragment(
        db, current_user.id, query
    )
    return {"campaigns": campaigns}


@router.post(
    "/campaigns/{campaign_id}/prospects", response_model=schemas.AddToCampaignsResponse
)
def add_prospects_to_campaign(
    data: schemas.AddToCampaigns,
    campaign_id: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Validate and add prospects to a campaign"""
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Please log in")

    campaign = CampaignCrud.get_by_id(db, campaign_id)
    if not campaign:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with id {campaign_id} does not exist",
        )

    if campaign.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"You do not have access to that campaign",
        )

    # Get existing prospects for this campaign
    existing_prospect_ids = CampaignCrud.get_existing_campaign_prospects(
        db, campaign_id
    )

    data.prospect_ids = ProspectCrud.validate_prospect_ids(
        db, current_user.id, data.prospect_ids
    )

    # Add only valid/non-duplicate prospects
    new_prospect_ids = data.prospect_ids - existing_prospect_ids
    CampaignCrud.add_prospects_to_campaign(db, campaign_id, new_prospect_ids)

    return JSONResponse({"prospect_ids": list(new_prospect_ids)}, 200)
