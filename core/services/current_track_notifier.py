from socket import create_connection

class CurrentTrackNotifier:

    @classmethod
    def create(cls):
        return cls()

    def notify(self, new_track):
        with create_connection(("localhost", 3403)) as sock:
            sock.send("{} - {}".format(new_track.artists, new_track.title).encode())
