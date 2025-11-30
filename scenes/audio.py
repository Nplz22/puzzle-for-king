import pygame, os

class AudioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.current_path = None
        self.music_volume = 1.0
        self.sfx_volume = 0.3
        self.playing = False

    def play_music(self, path, volume=1.0, loop=-1):
        if path is None:
            self.stop_music()
            return
        path = os.path.normpath(path)
        needs_load = self.current_path != path
        self.music_volume = max(0.0, min(1.0, volume))
        if needs_load:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loop)
                self.current_path = path
                self.playing = True
            except Exception:
                self.current_path = None
                self.playing = False
        else:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception:
                pass
            if not pygame.mixer.music.get_busy() and self.music_volume > 0:
                try:
                    pygame.mixer.music.play(loop)
                    self.playing = True
                except Exception:
                    self.playing = False

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self.playing = False
        self.current_path = None

    def pause_music(self):
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass
        self.playing = False

    def unpause_music(self):
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass
        if pygame.mixer.music.get_busy():
            self.playing = True

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception:
            pass
        if self.music_volume == 0:
            try:
                pygame.mixer.music.pause()
            except Exception:
                pass
            self.playing = False
        else:
            try:
                if not pygame.mixer.music.get_busy() and self.current_path:
                    pygame.mixer.music.play(-1)
                    self.playing = True
                else:
                    pygame.mixer.music.set_volume(self.music_volume)
            except Exception:
                pass

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))

def get_audio_manager():
    return AudioManager()
