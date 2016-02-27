import spotify
import time

from .services import service_registry
from .configs import get_config

import credentials


class ErrorLoggingIn(Exception):
    pass


class Player:

    def __init__(self):
        self._session = spotify.Session()
        self._session.volume_normalization = True
        self._loop = spotify.EventLoop(self._session)
        self._audio = get_config().audio_class(self._session)
        self._track_repository = service_registry.get("track_repository")
        self._current_track_notifier = service_registry.get("current_track_notifier")
        self._current_track = None
        self._plugins = self.register_plugins()

    def _login(self):
        self._session.login(credentials.username, credentials.password)
        self._wait_for_login()

    def _wait_for_login(self):
        i = 0
        while i < 300:
            self._session.process_events()
            if self._is_ready:
                break
            time.sleep(0.1)
        else:
            raise ErrorLoggingIn()

    def _start(self):
        self._session.on(
            spotify.SessionEvent.END_OF_TRACK,
            self._play_next
        )
        self._loop.start()

    @property
    def _is_ready(self):
        return self._session.connection.state is spotify.ConnectionState.LOGGED_IN

    def _run_loop(self):
        """ Keeps the application running continuously """
        while True:
            if not self._current_track:
                self._play_next()
            for plugin in self._plugins:
                plugin()
            time.sleep(0.05)

    def _play(self):
        self._session.player.play()

    def _pause(self):
        self._session.player.pause()

    def _load_track(self, track):
        track = self._session.get_track(track.uri).load()
        self._session.player.load(track)

    def _play_next(self, *args, **kwargs):
        next_track = self._track_repository.get_next_track()
        if not next_track:
            return
        self._load_track(next_track)

        self._current_track = next_track
        self._current_track_notifier.notify(next_track)

        self._play()
        print("next", self._current_track.title)

    def skip(self):
        self._current_track.skip_count += 1
        self._track_repository.update(self._current_track)
        self._play_next()

    def register_plugins(self):
        plugins = set()
        for plugin_class in get_config().plugins:
            plugins.add(plugin_class(self))
        return plugins

    def run(self):
        self._login()
        self._start()
        self._run_loop()

    def play_pause(self):
        if self._session.player.state == spotify.player.PlayerState.PLAYING:
            self._pause()
        else:
            self._play()
