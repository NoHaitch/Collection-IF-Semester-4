from typing import Optional
class Episode:
    def __init__(self, episodeNumber, title: str, duration: int, episodeProgress: Optional[int] = None):
        """
        Kelas episode
        :param episodeNumber: nomor episode pada series
        :param title: judul episode
        :param duration: durasi episode, integer dalam satuan detik
        :param episodeProgress: progress tonton episode, integer detik, optional saat construct
        """
        assert duration is not None, "Durasi tidak boleh kosong"
        assert duration > 0, "Durasi harus lebih dari 0"
        self.episodeNumber = episodeNumber
        self.title = title
        self.duration = duration
        self.episodeProgress = episodeProgress
        self.type = "Episode"

    # GETTER
    def get_episodeNumber(self): return self.episodeNumber
    def get_title(self): return self.title
    def get_duration(self): return self.duration
    def get_episodeProgress(self): return self.episodeProgress
    def getType(self): return self.type

    # SETTER
    def set_episodeNumber(self, episodeNumber): self.episodeNumber = episodeNumber
    def set_title(self, title): self.title = title
    def set_duration(self, duration):
        assert duration is not None, "Durasi tidak boleh kosong"
        assert duration > 0, "Durasi harus lebih dari 0"
        self.duration = duration
    def set_episodeProgress(self, episodeProgress: int | None): self.episodeProgress = episodeProgress


    def update_episode(self, title=None, duration=None, episodeProgress=None):
        if title is not None:
            self.title = title
        if duration is not None:
            self.duration = duration
        if episodeProgress is not None:
            self.episodeProgress = episodeProgress
