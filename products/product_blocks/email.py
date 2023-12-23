from typing import Optional



from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle

from products.product_blocks.improviser import ImproviserBlockInactive, ImproviserBlockProvisioning, ImproviserBlock


class EmailBlockInactive(ProductBlockModel, product_block_name="Email"):
    improviser: ImproviserBlockInactive
    email_address: Optional[str] = None
    subject: Optional[str] = None 
    message: Optional[str] = None 
    

class EmailBlockProvisioning(EmailBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    improviser: ImproviserBlockProvisioning
    email_address: Optional[str] = None
    subject: Optional[str] = None 
    message: Optional[str] = None 
    
    @serializable_property
    def title(self) -> str:
        # TODO: format correct title string
        return f"{self.name}"


class EmailBlock(EmailBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    improviser: ImproviserBlock
    email_address: str
    subject: str 
    message: str 
    