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
        self.music_volume = 0.3
        self.sfx_volume = 0.3
        self.master_volume = 0.25
        self.playing = False
        self.paused = False
        self._sfx_list = []

    def _apply_music_volume(self):
        try:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        except Exception:
            pass

    def _apply_sfx_volume_to_sound(self, sound):
        try:
            sound.set_volume(self.sfx_volume * self.master_volume)
        except Exception:
            pass

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
            self._apply_music_volume()
            if self.music_volume == 0 or self.master_volume == 0:
                try: pygame.mixer.music.pause()
                except Exception: pass
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
        except Exception:
            self.current_path = None
            self.playing = False
            self.paused = False

    def stop_music(self):
        try: pygame.mixer.music.stop()
        except Exception: pass
        self.playing = False
        self.paused = False
        self.current_path = None

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        self._apply_music_volume()
        if self.music_volume == 0 or self.master_volume == 0:
            try: pygame.mixer.music.pause()
            except Exception: pass
            self.paused = True
            self.playing = False
        else:
            if self.paused:
                try:
                    pygame.mixer.music.unpause()
                    self.paused = False
                    self.playing = True
                except Exception:
                    if self.current_path:
                        try:
                            pygame.mixer.music.play(-1)
                            self.playing = True
                            self.paused = False
                        except Exception:
                            self.playing = False


    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        remove_list = []
        for s in self._sfx_list:
            try:
                if s:
                    self._apply_sfx_volume_to_sound(s)
            except Exception:
                remove_list.append(s)
        for s in remove_list:
            try: self._sfx_list.remove(s)
            except Exception: pass

    def register_sfx(self, sound):
        try:
            if sound and sound not in self._sfx_list:
                self._sfx_list.append(sound)
                try: self._apply_sfx_volume_to_sound(sound)
                except Exception: pass
        except Exception: pass

def get_audio_manager():
    return AudioManager()
