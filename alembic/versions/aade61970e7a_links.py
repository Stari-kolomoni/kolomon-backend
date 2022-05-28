"""Links

Revision ID: aade61970e7a
Revises: 5f4dd9ce74f4
Create Date: 2022-02-15 18:41:24.928738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aade61970e7a'
down_revision = '5f4dd9ce74f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link_to_entry')
    op.add_column('links', sa.Column('entry', sa.Integer(), nullable=True))
    op.drop_index('ix_links_url', table_name='links')
    op.create_index(op.f('ix_links_url'), 'links', ['url'], unique=False)
    op.create_foreign_key(None, 'links', 'entries', ['entry'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'links', type_='foreignkey')
    op.drop_index(op.f('ix_links_url'), table_name='links')
    op.create_index('ix_links_url', 'links', ['url'], unique=False)
    op.drop_column('links', 'entry')
    op.create_table('link_to_entry',
    sa.Column('entry_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('link_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['entry_id'], ['entries.id'], name='link_to_entry_entry_id_fkey'),
    sa.ForeignKeyConstraint(['link_id'], ['links.id'], name='link_to_entry_link_id_fkey'),
    sa.PrimaryKeyConstraint('entry_id', 'link_id', name='link_to_entry_pkey')
    )
    # ### end Alembic commands ###