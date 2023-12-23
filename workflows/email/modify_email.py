from collections.abc import Generator
from pydantic_forms.core import ReadOnlyField
from typing import Optional

import structlog

from orchestrator.forms import FormPage
from orchestrator.forms.validators import OrganisationId, Divider, MigrationSummary
from orchestrator.types import FormGenerator, State, UUIDstr, SubscriptionLifecycle
from orchestrator.workflow import StepList, begin, step
from orchestrator.workflows.utils import modify_workflow
from orchestrator.workflows.steps import set_status

from products.product_types.email import Email, EmailProvisioning


from orchestrator.domain import SubscriptionModel


def subscription_description(subscription: SubscriptionModel) -> str:
    """The suggested pattern is to implement a subscription service that generates a subscription specific
       description, in case that is not present the description will just be set to the product name.
    """
    return f"{subscription.product.name} subscription"

logger = structlog.get_logger(__name__)


def initial_input_form_generator(subscription_id: UUIDstr) -> FormGenerator:
    subscription = Email.from_subscription(subscription_id)
    email = subscription.email

    # TODO fill in additional fields if needed

    class ModifyEmailForm(FormPage):
        organisation: OrganisationId = subscription.customer_id  # type: ignore


        divider_1: Divider

        email_address: Optional[str] = email.email_address
        subject: Optional[str] = email.subject
        message: Optional[str] = email.message
        first_name: str = email.first_name
        user_id: str = email.user_id
        user_email_address: str = email.user_email_address
        is_paying_user: bool = email.is_paying_user
        

    user_input = yield ModifyEmailForm
    user_input_dict = user_input.dict()

    yield from create_summary_form(user_input_dict, subscription)

    return user_input_dict | {"subscription": subscription}


def create_summary_form(user_input: dict, subscription: Email) -> Generator:
    product_summary_fields = [ "email_address", "subject", "message", "first_name", "user_id", "user_email_address", "is_paying_user",]

    before = [str(getattr(subscription.email, nm)) for nm in product_summary_fields]
    after = [str(user_input[nm]) for nm in product_summary_fields]

    class ProductSummary(MigrationSummary):
        data = {
            "labels": product_summary_fields,
            "headers": ["Before", "After"],
            "columns": [before, after],
        }

    class SummaryForm(FormPage):
        class Config:
            title = f"{subscription.product.name} Summary"

        product_summary: ProductSummary
        divider_1: Divider

    # TODO fill in additional details if needed

    yield SummaryForm


@step("Update subscription")
def update_subscription(
    subscription: EmailProvisioning,
    email_address: Optional[str],
    subject: Optional[str],
    message: Optional[str],
    first_name: str,
    user_id: str,
    user_email_address: str,
    is_paying_user: bool,
    ) -> State:
    # TODO: get all modified fields
    subscription.email.email_address = email_address
    subscription.email.subject = subject
    subscription.email.message = message
    subscription.email.first_name = first_name
    subscription.email.user_id = user_id
    subscription.email.user_email_address = user_email_address
    subscription.email.is_paying_user = is_paying_user
    return {"subscription": subscription}


@step("Update subscription description")
def update_subscription_description(subscription: Email) -> State:
    subscription.description = subscription_description(subscription)
    return {"subscription": subscription}


additional_steps = begin


@modify_workflow("Modify email", initial_input_form=initial_input_form_generator, additional_steps=additional_steps)
def modify_email() -> StepList:
    return (
        begin
        >> set_status(SubscriptionLifecycle.PROVISIONING)
        >> update_subscription
        >> update_subscription_description
        # TODO add additional steps if needed
        >> set_status(SubscriptionLifecycle.ACTIVE)
    )