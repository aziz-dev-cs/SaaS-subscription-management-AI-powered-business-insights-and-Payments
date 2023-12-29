from pydantic import BaseModel


class WebhookEventSchema(BaseModel):
    provider: str
    event_type: str
    external_id: str
    payload: dict
