"""Add promotions, reservations and pricing breakdown."""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = "005_promotions_inventory"
down_revision = "004_add_stock_quantity"
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database schema."""
    op.add_column("orders", sa.Column("pricing_breakdown", sa.JSON(), nullable=True))

    op.create_table(
        "promotions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("promotion_type", sa.String(length=30), nullable=False),
        sa.Column("discount_percentage", sa.Float(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("active_from", sa.DateTime(), nullable=True),
        sa.Column("active_to", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_promotions_id", "promotions", ["id"], unique=False)
    op.create_index("ix_promotions_promotion_type", "promotions", ["promotion_type"], unique=False)
    op.create_index("ix_promotions_category_id", "promotions", ["category_id"], unique=False)

    op.create_table(
        "inventory_reservations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("reason", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("released_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_inventory_reservations_id", "inventory_reservations", ["id"], unique=False
    )
    op.create_index(
        "ix_inventory_reservations_status", "inventory_reservations", ["status"], unique=False
    )


def downgrade():
    """Downgrade database schema."""
    op.drop_index("ix_inventory_reservations_status", table_name="inventory_reservations")
    op.drop_index("ix_inventory_reservations_id", table_name="inventory_reservations")
    op.drop_table("inventory_reservations")

    op.drop_index("ix_promotions_category_id", table_name="promotions")
    op.drop_index("ix_promotions_promotion_type", table_name="promotions")
    op.drop_index("ix_promotions_id", table_name="promotions")
    op.drop_table("promotions")

    op.drop_column("orders", "pricing_breakdown")
