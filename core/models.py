
class Track:

    def __init__(self, title, artists, uri, skip_count=0, is_queued=False, cover_url="", duration="",):
        self.title = title
        self.artists = artists
        self.uri = uri
        self.cover_url = cover_url
        self.duration = duration
        self.skip_count = skip_count
        self.is_queued = is_queued
