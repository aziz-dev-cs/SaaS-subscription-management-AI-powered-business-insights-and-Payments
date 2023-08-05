import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import get_db_session
from app.modules.subscriptions.repository import SubscriptionRepository
from app.modules.subscriptions.schemas import SubscriptionCreate, SubscriptionResponse
from app.modules.subscriptions.service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


def _get_service(session: AsyncSession = Depends(get_db_session)) -> SubscriptionService:
    return SubscriptionService(repo=SubscriptionRepository(session))


@router.post("/", response_model=SubscriptionResponse, status_code=201)
async def create_subscription(
    payload: SubscriptionCreate,
    service: SubscriptionService = Depends(_get_service),
):
    subscription = await service.create_subscription(payload)
    return subscription


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: uuid.UUID,
    service: SubscriptionService = Depends(_get_service),
):
    repo = service._repo
    subscription = await repo.get_subscription(subscription_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.post("/{subscription_id}/cancel", response_model=SubscriptionResponse)
async def cancel_subscription(
    subscription_id: uuid.UUID,
    service: SubscriptionService = Depends(_get_service),
):
    subscription = await service.cancel_subscription(subscription_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription
