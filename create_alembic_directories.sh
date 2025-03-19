#!/bin/bash

# Create the alembic directory if it doesn't exist
mkdir -p alembic/versions

# If script.py.mako doesn't exist, create it
if [ ! -f alembic/script.py.mako ]; then
    echo "Creating script.py.mako template..."
    cat > alembic/script.py.mako << 'EOF'
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
EOF
fi

echo "Alembic directory structure created. You can now run:"
echo "alembic revision --autogenerate -m 'Initial migration'"
