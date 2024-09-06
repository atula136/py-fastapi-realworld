from app.db.session import Base, engine
from app.db.models import User

# Optional: Function to initialize the database
def init_db():
    """Initialize the database by creating all tables."""
    # Base.metadata.create_all(bind=engine)
