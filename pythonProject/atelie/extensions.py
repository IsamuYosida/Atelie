from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(metadata=MetaData())  # Явное указание MetaData
migrate = Migrate()