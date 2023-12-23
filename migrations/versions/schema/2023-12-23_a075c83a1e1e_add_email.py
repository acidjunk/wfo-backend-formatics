"""Add email product.

Revision ID: a075c83a1e1e
Revises: a77227fe5455
Create Date: 2023-12-23 17:03:33.576969

"""
from uuid import uuid4

from alembic import op

from orchestrator.migrations.helpers import create, create_workflow, delete, delete_workflow, ensure_default_workflows
from orchestrator.targets import Target

# revision identifiers, used by Alembic.
revision = "a075c83a1e1e"
down_revision = "a77227fe5455"
branch_labels = None
depends_on = None

new_products = {
    "products": {
        "email Marketing": {
            "product_id": uuid4(),
            "product_type": "Email",
            "description": "Email",
            "tag": "EMAIL",
            "status": "active",
            "product_blocks": [ "Email", "Improviser",],
            "fixed_inputs": {
                "email_type": "Marketing",
            },
        },
        "email Reminder": {
            "product_id": uuid4(),
            "product_type": "Email",
            "description": "Email",
            "tag": "EMAIL",
            "status": "active",
            "product_blocks": [ "Email", "Improviser",],
            "fixed_inputs": {
                "email_type": "Reminder",
            },
        },
        "email Reactivation": {
            "product_id": uuid4(),
            "product_type": "Email",
            "description": "Email",
            "tag": "EMAIL",
            "status": "active",
            "product_blocks": [ "Email", "Improviser",],
            "fixed_inputs": {
                "email_type": "Reactivation",
            },
        },
        "email Platform": {
            "product_id": uuid4(),
            "product_type": "Email",
            "description": "Email",
            "tag": "EMAIL",
            "status": "active",
            "product_blocks": [ "Email", "Improviser",],
            "fixed_inputs": {
                "email_type": "Platform",
            },
        },
        },
    "product_blocks": {
    "Email": {
            "product_block_id": uuid4(),
            "description": "email product block",
            "tag": "EMAIL",
            "status": "active",
            "resources": {
                "email_address": "Email address",
                "subject": "Subject",
                "message": "Message",
            },
            "depends_on_block_relations": [],
        },
    "Improviser": {
            "product_block_id": uuid4(),
            "description": "Improviser block",
            "tag": "IMPROVISER",
            "status": "active",
            "resources": {
                "first_name": "First name of user in improviser",
                "user_id": "Improviser user_id for this user",
                "user_email_address": "Improviser email address for this user",
                "is_paying_user": "Indicates if this is an user with an active improviser license",
            },
            "depends_on_block_relations": [],
        },
    },
    "workflows": {},
}

new_workflows = [
    {
        "name": "create_email",
        "target": Target.CREATE,
        "description": "Create email",
        "product_type": "Email",
    },
    {
        "name": "modify_email",
        "target": Target.MODIFY,
        "description": "Modify email",
        "product_type": "Email",
    },
    {
        "name": "terminate_email",
        "target": Target.TERMINATE,
        "description": "Terminate email",
        "product_type": "Email",
    },
    {
        "name": "validate_email",
        "target": Target.SYSTEM,
        "description": "Validate email",
        "product_type": "Email",
    },
]


def upgrade() -> None:
    conn = op.get_bind()
    create(conn, new_products)
    for workflow in new_workflows:
        create_workflow(conn, workflow)
    ensure_default_workflows(conn)


def downgrade() -> None:
    conn = op.get_bind()
    for workflow in new_workflows:
        delete_workflow(conn, workflow["name"])

    delete(conn, new_products)