"""Add stock_quantity to products table migration."""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = "004_add_stock_quantity"
down_revision = "003_add_loyalty_tier"
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database schema."""
    op.add_column(
        "products",
        sa.Column("stock_quantity", sa.Integer(), nullable=True),
    )


def downgrade():
    """Downgrade database schema."""
    op.drop_column("products", "stock_quantity")