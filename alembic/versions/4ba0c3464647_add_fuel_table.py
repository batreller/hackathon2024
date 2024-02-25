"""add fuel table

Revision ID: 4ba0c3464647
Revises: e4222f79264a
Create Date: 2024-02-25 07:53:03.178722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ba0c3464647'
down_revision: Union[str, None] = 'e4222f79264a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fuel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fuel_type', sa.String(), nullable=True),
    sa.Column('fuel_price_in_pounds', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fuel_type')
    )
    op.create_foreign_key(None, 'cars', 'fuel', ['fuel_type'], ['fuel_type'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cars', type_='foreignkey')
    op.drop_table('fuel')
    # ### end Alembic commands ###
