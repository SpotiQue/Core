from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine, Boolean
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql.expression import func, select
from core.models import Track
import random
from ..configs import get_config

metadata = MetaData()

mapper(
    Track,
    Table(
        'track',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String(255)),
        Column('artists', String(255)),
        Column('uri', String(255), unique=True),
        Column('skip_count', Integer),
        Column('is_queued', Boolean),
    )
)

engine = create_engine(get_config().database_uri)
Session = sessionmaker(bind=engine)

metadata.create_all(engine)


class TrackRepository:

    def __init__(self):
        self.session = Session()

    def _get_random_track(self, queued):
        query_filter = {}
        if queued:
            query_filter = {'is_queued': True}
        query = self.session.query(Track).filter_by(**query_filter)
        tracks_count = int(query.count())
        return query.offset(int(tracks_count*random.random())).first()

    def _unqueue_track(self, track):
        track.is_queued = False
        self.update(track)

    def get_next_track(self):
        queued_track = self._get_random_track(True)
        if queued_track:
            self._unqueue_track(queued_track)
            return queued_track
        else:
            return self._get_random_track(False)

    def update(self, track):
        self.session.add(track)
        self.session.commit()
