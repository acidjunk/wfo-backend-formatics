from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle, strEnum

from products.product_blocks.email import (
    EmailBlock,
    EmailBlockInactive,
    EmailBlockProvisioning,
)

class Email_Type(strEnum):
    Marketing = "Marketing"
    Reminder = "Reminder"
    Reactivation = "Reactivation"
    Platform = "Platform"
    
class EmailInactive(SubscriptionModel, is_base=True):
    email_type: Email_Type
    email: EmailBlockInactive


class EmailProvisioning(EmailInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    email_type: Email_Type
    email: EmailBlockProvisioning


class Email(EmailProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    email_type: Email_Type
    email: EmailBlock
