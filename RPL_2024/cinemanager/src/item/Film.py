from src.item.WatchItem import WatchItem
import datetime
from typing import Optional, List


class Film(WatchItem):
    # Static variable list of film, menyimpan seluruh film yang ada
    listFilm: List['Film'] = []

    # Constructor
    def __init__(self, ID:int,
                 title: str,
                 posterPath: Optional[str] = None,
                 status: Optional[str] = None,
                 synopsis: Optional[str] = None,
                 genre: Optional[List[str] | str] = None,
                 rating: Optional[float] = None,
                 comments: Optional[str] = None,
                 reviewDate: Optional[datetime] = None,
                 lastWatch: Optional[datetime] = None,
                 duration: int = 0,
                 progress: Optional[int] = None):
        """
        Type kelas Film
        :param ID: ID dari WatchItem. Didapatkan dari database
        :param title: judul dari film
        :param posterPath: path dari poster film, nama file saja tidak perlu dengan path lainnya
        :param status: status dari film, string
        :param synopsis: simopsis dari film
        :param genre: genre dari film, list of string (list of genre)
        :param rating: rating dari series, float, 0-5
        :param comments: komentar dari film, string
        :param reviewDate: tanggal review dari film, datetime
        :param lastWatch: terakhir kali menonton film, datetime
        :param duration: durasi film dalam sekon
        :param progress: progress menonton film dalam sekon
        """
        super().__init__(ID, title, posterPath, status, synopsis, genre, rating, comments, reviewDate, lastWatch)
        assert duration > 0, "Durasi harus lebih dari 0"
        self.duration = duration
        assert progress is None or progress >= 0, "Progress harus lebih dari 0"
        self.progress = progress
        if progress is None:
            self.status = "Unwatched"
        else:
            self.status = status
        self.type = "Film"
        Film.listFilm.append(self)

    # GETTER
    def getDuration(self): return self.duration
    def getProgress(self): return self.progress
    def getType(self): return self.type

    # SETTER
    def setDuration(self, duration: int): self.duration = duration
    def setProgress(self, progress: int | None):
        if progress is not None:
            assert progress > 0, "Progress harus lebih dari 0"
            self.progress = progress
            if progress == self.duration:
                self.status = "Finished"
    def setType(self, tipe: str): self.type = tipe

    @staticmethod
    def cast_to_film(item : WatchItem):
        if isinstance(item, Film):
            return item
        else:
            return None

    @staticmethod
    def get_film_by_id(film_id: int):
        for item in Film.listFilm:
            if item.getID() == film_id:
                return item
        return None
