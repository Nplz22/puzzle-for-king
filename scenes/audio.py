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
        self.paused = False
        self._sfx_list = []

    def play_music(self, path, loop=-1):
        if path is None:
            self.stop_music()
            return
        path = os.path.normpath(path)
        needs_load = self.current_path != path
        self.current_path = path
        try:
            if needs_load:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                pygame.mixer.music.load(path)
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception:
                pass
            if self.music_volume == 0:
                try:
                    pygame.mixer.music.pause()
                    self.paused = True
                    self.playing = False
                except Exception:
                    self.paused = True
                    self.playing = False
            else:
                try:
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play(loop)
                    else:
                        pygame.mixer.music.unpause()
                    self.paused = False
                    self.playing = True
                except Exception:
                    self.playing = False
                    self.paused = False
        except Exception:
            self.current_path = None
            self.playing = False
            self.paused = False

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        self.playing = False
        self.paused = False
        self.current_path = None

    def pause_music(self):
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass
        self.paused = True
        self.playing = False

    def unpause_music(self):
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass
        if pygame.mixer.music.get_busy():
            self.paused = False
            self.playing = True
        else:
            if self.current_path and self.music_volume > 0:
                try:
                    pygame.mixer.music.play(-1)
                    self.paused = False
                    self.playing = True
                except Exception:
                    self.playing = False

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
            self.paused = True
            self.playing = False
        else:
            if self.paused:
                try:
                    pygame.mixer.music.unpause()
                    self.paused = False
                    self.playing = True
                except Exception:
                    try:
                        if self.current_path:
                            pygame.mixer.music.play(-1)
                            self.playing = True
                            self.paused = False
                    except Exception:
                        self.playing = False
            else:
                try:
                    if not pygame.mixer.music.get_busy() and self.current_path:
                        pygame.mixer.music.play(-1)
                        self.playing = True
                        self.paused = False
                except Exception:
                    pass

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        remove_list = []
        for s in self._sfx_list:
            try:
                if s: s.set_volume(self.sfx_volume)
            except Exception:
                remove_list.append(s)
        for s in remove_list:
            try: self._sfx_list.remove(s)
            except Exception: pass

    def register_sfx(self, sound):
        try:
            if sound and sound not in self._sfx_list:
                self._sfx_list.append(sound)
                try: sound.set_volume(self.sfx_volume)
                except Exception: pass
        except Exception:
            pass

def get_audio_manager():
    return AudioManager()
