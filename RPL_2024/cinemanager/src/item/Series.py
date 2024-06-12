from src.item.WatchItem import WatchItem
import datetime
from typing import Optional, Union, List
from src.item.Episode import Episode


class Series(WatchItem):
    # Static variable list of series, menyimpan seluruh series yang ada
    listSeries: List['Series'] = []

    # Constructor
    def __init__(self, ID,
                 title: str,
                 posterPath: Optional[str] = None,
                 status: Optional[str] = None,
                 synopsis: Optional[str] = None,
                 genre: Optional[List[str] | str] = None,
                 rating: Optional[float] = None,
                 comments: Optional[str] = None,
                 reviewDate: Optional[datetime] = None,
                 lastWatch: Optional[datetime] = None,
                 totalEpisode: int = 0,
                 currentEpisode: Optional[int] = None,
                 episodes: Optional[List[Episode]] = None):
        """
        Kelas series
        :param ID: ID dari WatchItem. Didapatkan dari database
        :param title: judul dari series
        :param posterPath: path dari poster series, nama file saja tidak perlu dengan path lainnya
        :param status: status dari series, string
        :param synopsis: simopsis dari series
        :param genre: genre dari series, list of string (list of genre)
        :param rating: rating dari series, float, 0-5
        :param comments: komentar dari series, string
        :param reviewDate: tanggal review dari series, datetime
        :param lastWatch: terakhir kali menonton series, datetime
        :param totalEpisode: total episode dari series
        :param currentEpisode: episode terakhir yang ditonton, ID episode terakhir yang ditonton, optional saat construct
        :param episodes: list of episode dari series, optional saat construct
        """
        super().__init__(ID, title, posterPath, status, synopsis, genre, rating, comments, reviewDate, lastWatch)
        self.totalEpisode = totalEpisode
        self.currentEpisode = currentEpisode
        self.type = "Series"
        if episodes is None:
            self.episodes = []
        elif isinstance(episodes, list):
            self.episodes = episodes
        elif isinstance(episodes, Episode):
            self.episodes = [episodes]
        else: self.episodes = []
        Series.listSeries.append(self)


    # GETTER
    def getTotalEpisode(self): return self.totalEpisode
    def getCurrentEpisode(self): return self.currentEpisode
    def getEpisodes(self): return self.episodes
    def getType(self): return self.type
    def getSeriesProgress(self) -> float:
        """
        Mengembalikan progress series dalam persen
        :return: float, persentaese series selesai dalam persen
        """
        totalFinished = 0
        for episode in self.episodes:
            if episode.episodeProgress == episode.duration:
                totalFinished += 1
        return totalFinished / self.totalEpisode * 100


    # SETTER
    def setTotalEpisode(self, totalEpisode: int): self.totalEpisode = totalEpisode
    def setCurrentEpisode(self, currentEpisode: int | None): self.currentEpisode = currentEpisode
    def setEpisodes(self, episodes: list[Episode] | None): self.episodes = episodes

    # EDIT EPISODES
    def addEpisode(self, episode: Episode | None):
        """
        Add episode to series. Banyak episode bertambah 1 (totalEpisode += 1)
        :param episode: Episode
        """
        if episode is not None:
            if isinstance(episode, Episode):
                episode.episodeNumber = self.totalEpisode + 1
                episode.type = "Episode"
            elif isinstance(episode, list):
                self.episodes.extend(episode)
                self.totalEpisode += len(episode)

    def deleteEpisode(self):
        """
        Delete last episode from series. Banyak episode berkurang 1 (totalEpisode -= 1)
        :return: Episode
        """
        _ = self.episodes.pop()
        self.totalEpisode -= 1

    def getEpisode(self, idx: int):
        """
        Get episode by index
        :param idx: nomor episode
        :return: Episode
        """
        return self.episodes[idx]

    @staticmethod
    def cast_to_series(item : WatchItem):
        if isinstance(item, Series):
            return item
        else:
            return None

    @staticmethod
    def get_series_by_id(series_id: int):
        for item in Series.listSeries:
            if item.getID() == series_id:
                return item
        return None
