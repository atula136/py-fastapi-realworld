## Prj
```
realworld_api/
├── alembic/                 # Database migrations
├── app/
│   ├── __init__.py          # Initialization for the app
│   ├── main.py              # Application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Application configurations
│   │   ├── security.py      # Authentication, JWT handling, password hashing
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py          # Base model and session management
│   │   ├── models.py        # Database models
│   │   ├── session.py       # Database session creation
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py          # CRUD operations for users
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic schemas for users
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injections
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── user.py      # User-related endpoints
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── profile.py   # Profile-related endpoints
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_user.py     # Tests for user routes
│   │   ├── test_auth.py     # Tests for authentication routes
│   │   ├── test_profile.py  # Tests for profile routes
├── .env                     # Environment variables
├── .gitignore
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
```

## ENV
create .env
```
database_url = "sqlite:///database.db"

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## Alembic Setup
pip install alembic

### Initialize Alembic
Navigate to your project directory and initialize Alembic:

```bash
alembic init alembic
```
This will create an alembic directory with a configuration file alembic.ini.

3. Configure Alembic (alembic/env.py)
Modify the alembic/env.py file to work with your SQLAlchemy models and the database configuration.

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from alembic import context

from app.models import Base  # Import your Base from the models
from app.config import settings  # Import your settings for the database URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired here, e.g., as config.get_main_option("some_option")
# or overridden with, e.g., config.set_main_option("some_option", "value")

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_engine(settings.database_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

4. Create an Initial Migration
Once you've configured Alembic, you can create an initial migration that reflects the current state of your models.

```bash
alembic revision --autogenerate -m "Initial migration"
```
This command will generate a new migration script under the alembic/versions/ directory. The script will contain SQL commands to create the tables defined in your models.py.

5. Apply the Migration
To apply the migration and create the tables in your database, run:

```bash
alembic upgrade head
```
This will execute the migration and update your database schema to match your models.

6. Alembic Configuration (alembic.ini)
Make sure your alembic.ini file points to the correct database:

```ini
# In alembic.ini
sqlalchemy.url = <your_database_url>
```
Or, better yet, use the settings from your FastAPI configuration by modifying the env.py file to dynamically read the database_url from your configuration module, as shown above.

Example of a Migration Script
Here’s what a generated migration script might look like:

```python
"""Initial migration

Revision ID: e7a1b0c3b9f1
Revises: 
Create Date: 2024-08-23 14:32:42.567829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7a1b0c3b9f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article_tags',
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_tags')
    op.drop_table('comments')
    op.drop_table('articles')
    op.drop_table('tags')
    op.drop_table('users')
    # ### end Alembic commands ###
```
This script will create all the necessary tables based on your SQLAlchemy models.

Summary
Alembic is used for database migrations, ensuring your database schema stays in sync with your models.
alembic.ini configures the connection to your database.
alembic/env.py is customized to integrate with your application's configuration and models.
Migration scripts are generated using alembic revision --autogenerate, and applied with alembic upgrade head.
This setup enables smooth database schema management as your project evolves.