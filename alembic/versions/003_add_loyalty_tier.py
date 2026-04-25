"""Add loyalty_tier to customers table migration."""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "003_add_loyalty_tier"
down_revision = "002_add_customer_order_schema"
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database schema."""
    op.add_column(
        "customers",
        sa.Column("loyalty_tier", sa.String(20), nullable=False, server_default="bronze"),
    )


def downgrade():
    """Downgrade database schema."""
    op.drop_column("customers", "loyalty_tier")
