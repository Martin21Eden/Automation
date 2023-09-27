from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_mixins.inspection import Base

from src.steps.db.models.base import BaseModel


class BaseDb:
    def __init__(self, db_url):
        self.engine = create_engine(db_url, pool_size=2, max_overflow=2)
        Base.metadata.bind = self.engine
        DBSession = scoped_session(sessionmaker(autocommit=True))
        DBSession.configure(bind=self.engine)
        self.session = DBSession()
        BaseModel.set_session(self.session)
