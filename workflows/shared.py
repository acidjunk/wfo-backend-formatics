# Copyright 2019-2023 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pprint import pformat
from typing import Generator, List

from deepdiff import DeepDiff
from orchestrator.db import (
    ProductTable,
    ResourceTypeTable,
    SubscriptionInstanceTable,
    SubscriptionInstanceValueTable,
    SubscriptionTable,
)
from orchestrator.domain.base import ProductBlockModel
from orchestrator.forms import FormPage
from orchestrator.forms.validators import Choice, MigrationSummary
from orchestrator.types import SubscriptionLifecycle, SummaryData, UUIDstr


def subscriptions_by_product_type(product_type: str, status: List[SubscriptionLifecycle]) -> List[SubscriptionTable]:
    """
    retrieve_subscription_list_by_product This function lets you retreive a
    list of all subscriptions of a given product type. For example, you could
    call this like so:

    >>> subscriptions_by_product_type("Node", [SubscriptionLifecycle.ACTIVE, SubscriptionLifecycle.PROVISIONING])
    [SubscriptionTable(su...note=None), SubscriptionTable(su...note=None)]

    You now have a list of all active Node subscription instances and can then
    use them in your workflow.

    Args:
        product_type (str): The prouduct type in the DB (i.e. Node, User, etc.)
        status (List[SubscriptionLifecycle]): The lifecycle states you want returned (i.e.
        SubscriptionLifecycle.ACTIVE)

    Returns:
        List[SubscriptionTable]: A list of all the subscriptions that match
        your criteria.
    """
    subscriptions = (
        SubscriptionTable.query.join(ProductTable)
        .filter(ProductTable.product_type == product_type)
        .filter(SubscriptionTable.status.in_(status))
        .all()
    )
    return subscriptions


def subscriptions_by_product_type_and_instance_value(
    product_type: str, resource_type: str, value: str, status: List[SubscriptionLifecycle]
) -> List[SubscriptionTable]:
    """Retrieve a list of Subscriptions by product_type, resource_type and value.

    Args:
        product_type: type of subscriptions
        resource_type: name of the resource type
        value: value of the resource type
        status: lifecycle status of the subscriptions

    Returns: Subscription or None

    """
    return (
        SubscriptionTable.query.join(ProductTable)
        .join(SubscriptionInstanceTable)
        .join(SubscriptionInstanceValueTable)
        .join(ResourceTypeTable)
        .filter(ProductTable.product_type == product_type)
        .filter(SubscriptionInstanceValueTable.value == value)
        .filter(ResourceTypeTable.resource_type == resource_type)
        .filter(SubscriptionTable.status.in_(status))
        .all()
    )


def node_selector(enum: str = "NodesEnum") -> Choice:
    node_subscriptions = subscriptions_by_product_type("Node", [SubscriptionLifecycle.ACTIVE])
    nodes = {
        str(subscription.subscription_id): subscription.description
        for subscription in sorted(node_subscriptions, key=lambda node: node.description)
    }
    return Choice(enum, zip(nodes.keys(), nodes.items()))  # type:ignore


# def free_port_selector(node_subscription_id: UUIDstr, speed: int, enum: str = "PortsEnum") -> Choice:
#     node = Node.from_subscription(node_subscription_id)
#     interfaces = {
#         str(interface.id): interface.name
#         for interface in netbox.get_interfaces(
#             device=netbox.get_device(id=node.node.ims_id), speed=speed * 1000, enabled=False
#         )
#     }
#     return Choice(enum, zip(interfaces.keys(), interfaces.items()))  # type:ignore
#

def summary_form(product_name: str, summary_data: dict) -> Generator:
    class ProductSummary(MigrationSummary):
        data = SummaryData(**summary_data)

    class SummaryForm(FormPage):
        class Config:
            title = f"{product_name} summary"

        product_summary: ProductSummary

    yield SummaryForm


def create_summary_form(user_input: dict, product_name: str, fields: List[str]) -> Generator:
    columns = [[str(user_input[nm]) for nm in fields]]
    yield from summary_form(product_name, {"labels": fields, "columns": columns})


def modify_summary_form(user_input: dict, block: ProductBlockModel, fields: List[str]) -> Generator:
    before = [str(getattr(block, nm)) for nm in fields]  # type: ignore[attr-defined]
    after = [str(user_input[nm]) for nm in fields]
    yield from summary_form(
        block.subscription.product.name,
        {
            "labels": fields,
            "headers": ["Before", "After"],
            "columns": [before, after],
        },
    )


def pretty_print_deepdiff(diff: DeepDiff) -> str:
    return pformat(diff.to_dict(), indent=2, compact=False)
