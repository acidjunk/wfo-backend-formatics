from collections.abc import Generator
from typing import Optional

from orchestrator import app_settings
from orchestrator.forms import FormPage
from orchestrator.forms.validators import Divider, Label, OrganisationId, MigrationSummary
from orchestrator.targets import Target
from orchestrator.types import FormGenerator, State, SubscriptionLifecycle, UUIDstr
from orchestrator.workflow import StepList, begin, step
from orchestrator.workflows.steps import store_process_subscription
from orchestrator.workflows.utils import create_workflow
from pydantic import EmailStr
from pydantic_forms.core import ReadOnlyField

from products.product_types.email import EmailInactive, EmailProvisioning

from orchestrator.domain import SubscriptionModel

from services.improviser import get_user_by_id


def subscription_description(subscription: EmailProvisioning) -> str:
    """The suggested pattern is to implement a subscription service that generates a subscription specific
       description, in case that is not present the description will just be set to the product name.
    """
    return f"{subscription.product.name} email {subscription.email.email_address}"


def initial_input_form_generator(product_name: str) -> FormGenerator:
    # TODO add additional fields to form if needed

    class CreateEmailForm(FormPage):
        class Config:
            title = product_name

        # label_email_settings: Label
        # divider_1: Divider

        user_id: UUIDstr = "4af1f7f5-4781-4607-bf6c-f0388f7f4527"
        # email_address: Optional[str]
        subject: Optional[str]
        # message: Optional[str]
        # first_name: Optional[str]
        # user_email_address: Optional[str]
        # is_paying_user: Optional[bool]
        
    user_input = yield CreateEmailForm

    user_input_dict = user_input.dict()
    yield from create_summary_form(user_input_dict, product_name)

    return user_input_dict


def create_summary_form(
    user_input: dict,
    product_name: str,
) -> Generator:
    product_summary_fields = [ "user_id", "subject" ]

    class ProductSummary(MigrationSummary):
        data = {
            "labels": product_summary_fields,
            "columns": [[str(user_input[nm]) for nm in product_summary_fields]],
        }

    class SummaryForm(FormPage):
        class Config:
            title = f"{product_name} Summary"

        product_summary: ProductSummary
        divider_1: Divider

        # TODO fill in additional details if needed

    yield SummaryForm


@step("Construct Initial Subscription model")
def construct_email_model(
    product: UUIDstr,
    subject: Optional,
    user_id: Optional,
    ) -> State:
    subscription = EmailInactive.from_product_id(
        product_id=product,
        customer_id=app_settings.DEFAULT_CUSTOMER_IDENTIFIER,
        status=SubscriptionLifecycle.INITIAL,
    )
    subscription.email.improviser.user_id = user_id
    subscription.email.subject = subject

    return {
        "subscription": subscription,
        "subscription_id": subscription.subscription_id,  # necessary to be able to use older generic step functions
    }


@step("Enrich worfklow with improviser info")
def fetch_improviser_info(subscription: EmailInactive) -> State:
    data = get_user_by_id(subscription.email.improviser.user_id)
    subscription.email.email_address = data["user_email_address"]
    subscription.email.improviser.user_email_address = data["user_email_address"]
    subscription.email.improviser.first_name = data["first_name"]
    subscription.email.improviser.is_paying_user = data["is_paying_user"]
    return {
        "subscription": subscription,
        "subscription_description": subscription.description,
    }

@step("Set email to provisioning")
def set_to_provisioning(subscription: EmailInactive) -> State:
    subscription = EmailProvisioning.from_other_lifecycle(subscription, SubscriptionLifecycle.PROVISIONING)
    # Todo: cook up nice mails, for now just hardcoded test
    subscription.email.message = "Nice cool test text"
    subscription.description = subscription_description(subscription)

    return {
        "subscription": subscription,
        "subscription_description": subscription.description,
    }


additional_steps = begin


@create_workflow("Create email", initial_input_form=initial_input_form_generator, additional_steps=additional_steps)
def create_email() -> StepList:
    return (
        begin
        >> construct_email_model
        >> fetch_improviser_info
        >> set_to_provisioning
        >> store_process_subscription(Target.CREATE)
        # TODO add provision step(s)
    )