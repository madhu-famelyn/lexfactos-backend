from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '8605e2a49da9'
down_revision = 'd01a7ba12c3c'
branch_labels = None
depends_on = None

# Define ENUM type
rating_enum = sa.Enum(
    'GOOD_FIT', 'MAYBE', 'NOT_A_FIT', 'NOT_DECIDED',
    name='ratingenum'
)

def upgrade():
    bind = op.get_bind()

    # ✅ Create ENUM type before adding column
    rating_enum.create(bind, checkfirst=True)

    # ✅ Add column with default value
    op.add_column(
        'job_applications',
        sa.Column('rate', rating_enum, nullable=False, server_default='NOT_DECIDED')
    )

def downgrade():
    bind = op.get_bind()

    # ✅ Drop column first
    op.drop_column('job_applications', 'rate')

    # ✅ Then drop ENUM type
    rating_enum.drop(bind, checkfirst=True)
