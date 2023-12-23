from typing import Optional



from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle




class ImproviserBlockInactive(ProductBlockModel, product_block_name="Improviser"):
    first_name: Optional[str] = None 
    user_id: Optional[str] = None 
    user_email_address: Optional[str] = None 
    is_paying_user: Optional[bool] = None 
    

class ImproviserBlockProvisioning(ImproviserBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    first_name: str 
    user_id: str 
    user_email_address: str 
    is_paying_user: bool 
    
    @serializable_property
    def title(self) -> str:
        # TODO: format correct title string
        return f"{self.name}"


class ImproviserBlock(ImproviserBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    first_name: str 
    user_id: str 
    user_email_address: str 
    is_paying_user: bool 
    