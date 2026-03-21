"""seed body parts

Revision ID: 3ec3cf30bfe6
Revises: f598a6d17dd0
Create Date: 2026-03-21 15:17:15.008611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ec3cf30bfe6'
down_revision: Union[str, Sequence[str], None] = 'f598a6d17dd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.table('body_part',
                 sa.column('name', sa.String)
                 ),
        [
            {'name': 'Chest'},
            {'name': 'Back'},
            {'name': 'Legs'},
            {'name': 'Arms'},
            {'name': 'Shoulders'},
            {'name': 'Core'},
            {'name': 'Glutes'},
            {'name': 'Calves'},
            {'name': 'Traps'}

        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM body_part WHERE name IN ('Chest','Back','Legs','Arms','Shoulders','Core','Glutes','Calves','Traps')")
