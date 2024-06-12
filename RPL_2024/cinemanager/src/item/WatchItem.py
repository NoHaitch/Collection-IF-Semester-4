import datetime
import os
from typing import Optional, List

class WatchItem:
    """
    Parent class untuk Film dan Series. Berisi semua atribut common untuk film dan series
    Abstract Class
    """
    listGenre = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family"]

    def __init__(self, ID,
                 title: str,
                 posterPath: Optional[str] = 'None',
                 status: Optional[str] = None,
                 synopsis: Optional[str] = None,
                 genre: Optional[List[str] | str] = None,
                 rating: Optional[float] = None,
                 comments: Optional[str] = None,
                 reviewDate: Optional[datetime] = None,
                 lastWatch: Optional[datetime] = None):
        """
        :param ID: ID dari WatchItem, ditentukan oleh database
        :param title: judul dari film atau series
        :param posterPath: path dari poster film atau series, nama file saja tidak perlu dengan path lainnya
        :param status: status dari film atau series, string. Nilai hanya: "Finished", "Ongoing", "Unwatched"
        :param synopsis: simopsis dari film atau series
        :param genre: genre dari film atau series, list of string (list of genre)
        :param rating: rating dari film atau series, float, 0-5
        :param comments: komentar dari film atau series, string
        :param reviewDate: tanggal review dari film atau series, datetime
        :param lastWatch: terakhir kali menonton film atau series, datetime
        """
        # Cek rating harus berada di antara 0 dan 5
        if rating is not None:
            assert 0 <= rating <= 5, "Rating harus berada di antara 0 dan 5"

        # Cek apakah posterPath adalah file gambar
        if posterPath is None or posterPath == "None":
            self.posterPath = None
        elif (posterPath.endswith('.jpg') or posterPath.endswith('.png') or posterPath.endswith('.jpeg') or posterPath.endswith('.gif') or
                posterPath.endswith('.bmp') or posterPath.endswith('.tiff') or posterPath.endswith('.webp')):
            # Path from src/item
            self.posterPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'poster', posterPath))
        else:
            raise AssertionError("Poster harus berupa file gambar")

        # Cek apakah status berada di antara Finished, Ongoing, atau Unwatched
        assert status is None or status in ["Finished", "Ongoing", "Unwatched", "Reviewed"], "Status harus berada di antara Finished, Ongoing, Unwatched, atau Reviewed"
        if status is None:
            self.status = "Unwatched"
        else:
            self.status = status

        # Cek apakah genre adalah list atau string
        if genre is None or genre == 'None':
            self.genre = []
        elif isinstance(genre, list):
            self.genre = []
            for i in range(len(genre)):
                same = False
                for g2 in WatchItem.listGenre:
                    if genre[i].lower() == g2.lower():
                        same = True
                        self.genre.append(g2[0].upper() + g2[1:])
                if not same:
                    WatchItem.listGenre.append(genre[i][0].upper() + genre[i][1:])
                    self.genre.append(genre[i][0].upper() + genre[i][1:])
        else:
            same = False
            for g in WatchItem.listGenre:
                if g.lower() == genre.lower():
                    same = True
                    self.genre = [g.capitalize()]
            if not same:
                WatchItem.listGenre.append(genre.capitalize())
                self.genre = [genre.capitalize()]

        self.ID = ID
        self.title = title
        self.synopsis = synopsis
        self.rating = rating
        self.comments = comments
        self.reviewDate = reviewDate
        self.lastWatch = lastWatch

    # GETTER
    def getID(self): return self.ID
    def getTitle(self): return self.title
    def getPosterPath(self): return self.posterPath
    def getStatus(self): return self.status
    def getSynopsis(self): return self.synopsis
    def getGenre(self): return self.genre
    def getRating(self): return self.rating
    def getComments(self): return self.comments
    def getReviewDate(self): return self.reviewDate
    def getLastWatch(self): return self.lastWatch

    #SETTER
    def setID(self, ID: str): self.ID = ID
    def setTitle(self, title: str): self.title = title
    def setPosterPath(self, posterPath: str | None):
        if posterPath is None or posterPath == "None":
            self.posterPath = None
        else:
            assert (posterPath.endswith('.jpg') or posterPath.endswith('.png') or posterPath.endswith('.jpeg') or posterPath.endswith('.gif') or
                    posterPath.endswith('.bmp') or posterPath.endswith('.tiff') or posterPath.endswith('.webp')), "Poster harus berupa file gambar"
            # Path from src/item to db/poster
            self.posterPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'poster', posterPath))
    def setStatus(self, status: str | None):
        assert status is None or status in ["Finished", "Ongoing",
                                            "Unwatched", "Reviewed"], "Status harus berada di antara Finished, Ongoing, Finished atau Reviewed"
        if status is None:
            self.status = "Unwatched"
        else:
            self.status = status
    def setSynopsis(self, synopsis: str | None): self.synopsis = synopsis
    def setGenre(self, genre: list[str] | str | None):
        if genre is None or genre == 'None':
            self.genre = []
        elif isinstance(genre, list):
            self.genre = []
            for i in range(len(genre)):
                same = False
                for g2 in WatchItem.listGenre:
                    if genre[i].lower() == g2.lower():
                        same = True
                        self.genre.append(g2[0].upper() + g2[1:])
                if not same:
                    WatchItem.listGenre.append(genre[i][0].upper() + genre[i][1:])
                    self.genre.append(genre[i][0].upper() + genre[i][1:])
        else:
            same = False
            for g in WatchItem.listGenre:
                if g.lower() == genre.lower():
                    same = True
                    self.genre = [g.capitalize()]
            if not same:
                WatchItem.listGenre.append(genre.capitalize())
                self.genre = [genre.capitalize()]
    def addGenre(self, genre: str | list[str] | None):
        if genre is None or genre == 'None':
            self.genre = []
        elif isinstance(genre, list):
            self.genre = []
            for i in range(len(genre)):
                same = False
                for g2 in WatchItem.listGenre:
                    if genre[i].lower() == g2.lower():
                        same = True
                        self.genre.append(g2[0].upper() + g2[1:])
                if not same:
                    WatchItem.listGenre.append(genre[i][0].upper() + genre[i][1:])
                    self.genre.append(genre[i][0].upper() + genre[i][1:])
        else:
            same = False
            for g in WatchItem.listGenre:
                if g.lower() == genre.lower():
                    same = True
                    self.genre = [g.capitalize()]
            if not same:
                WatchItem.listGenre.append(genre.capitalize())
                self.genre = [genre.capitalize()]
    def setRating(self, rating: int | None):
        if rating is None:
            self.rating = None
        else:
            assert 0 <= rating <= 5, "Rating harus berada di antara 0 dan 5"
            self.rating = rating
    def setComments(self, comments: str | None): self.comments = comments
    def setReviewDate(self, reviewDate: datetime.datetime | None): self.reviewDate = reviewDate
    def setLastWatch(self, lastWatch: datetime.datetime | None): self.lastWatch = lastWatch

    # FUNGSI FILTER DAN SORTIR

    # Fungsi filter list watch item berdasarkan sudah dikomentari atau belum, statik
    @staticmethod
    def filterIsCommented(listWatchItem: List['WatchItem']) -> List['WatchItem']:
        """
        Fungsi filter list watch item berdasarkan sudah dikomentari atau belum
        :param listWatchItem: list watch item yang akan difilter
        :return: list watch item yang sudah dikomentari
        """
        return [watchItem for watchItem in listWatchItem if watchItem.getComments() is not None]


    # Fungsi filter list watch item berdasarkan genre, statik
    @staticmethod
    def filterByGenre(listWatchItem: List['WatchItem'], genre: str | List[str]) -> List['WatchItem']:
        """
        Fungsi filter list watch item berdasarkan genre
        :param listWatchItem: list watch item yang akan difilter
        :param genre: genre yang akan dijadikan acuan filter
        :return: list watch item yang memiliki genre yang dicari
        """
        if isinstance(genre, list):
            return [watchItem for watchItem in listWatchItem if watchItem.getGenre() is not None and any(g in watchItem.getGenre() for g in genre)]
        else:
            return [watchItem for watchItem in listWatchItem if watchItem.getGenre() is not None and genre in watchItem.getGenre()]


    # Fungsi filter list watch item berdasarkan rating, statik
    @staticmethod
    def filterByRating(listWatchItem: List['WatchItem'], rating: float) -> List['WatchItem']:
        """
        Fungsi filter list watch item berdasarkan rating
        :param listWatchItem: list watch item yang akan difilter
        :param rating: rating yang akan dijadikan acuan filter
        :return: list watch item yang memiliki rating yang dicari
        """
        return [watchItem for watchItem in listWatchItem if watchItem.getRating() is not None and watchItem.getRating() == rating]


    # Fungsi filter list film berdasarkan status, statik
    @staticmethod
    def filterByStatus(listWatchItem: List['WatchItem'], status: str) -> List['WatchItem']:
        """
        Fungsi filter list watch item berdasarkan status
        :param listWatchItem: list watch item yang akan difilter
        :param status: status yang akan dijadikan acuan filter. Jika status yang ada pada watchitem None asumsinya status = "Unwatched"
        :return: list watch item yang memiliki status yang dicari
        """
        if status == "Unwatched":
            return [watchItem for watchItem in listWatchItem if watchItem.getStatus() is None or watchItem.getStatus() == status]
        elif status == "Finished" or status == "Reviewed":
            return [watchItem for watchItem in listWatchItem if watchItem.getStatus() is not None and (watchItem.getStatus() == "Reviewed" or watchItem.getStatus() == "Finished")]
        else:
            return [watchItem for watchItem in listWatchItem if watchItem.getStatus() is not None and watchItem.getStatus() == status]


    # Fungsi sortir list watch item berdasarkan rating, statik. Jika rating sama, sortir berdasarkan judul.
    # isAscending = True, sortir dari rating terendah ke tertinggi, else sebaliknya
    @staticmethod
    def sortByRating(listWatchItem: List['WatchItem']) -> List['WatchItem']:
        """
        Fungsi sortir list film berdasarkan rating
        :param listWatchItem: list watch item yang akan disortir. Watch item yang belum memiliki rating akan dianggap memiliki rating terendah
        :return: list watch item yang sudah disortir
        """
        return sorted(listWatchItem, key=lambda x: (0-x.getRating() if (x.getRating() is not None) else 1, x.getTitle()), reverse = False)


    @staticmethod
    def sortByAlphabet(listWatchItem: List['WatchItem'], isAscending: bool) -> List['WatchItem']:
        """
        Fungsi sortir list film berdasarkan alfabet title
        :param listWatchItem: list watch item yang akan disortir.
        :param isAscending: True jika sortir dari abjad terkecil ke terbesar, False sebaliknya
        :return: list watch item yang sudah disortir
        """
        return sorted(listWatchItem, key=lambda x: x.getTitle(), reverse=not isAscending)

    @staticmethod
    def sortByLastWatchedNewest(listWatchItem: List['WatchItem']) -> List['WatchItem']:
        """
        Fungsi sortir list film berdasarkan tanggal terakhir tonton secara menurun
        :param listWatchItem: list watch item yang akan disortir.

        :return: list watch item yang sudah disortir
        """
        return sorted(listWatchItem, key=lambda x: (x.getLastWatch(), x.getTitle()), reverse = True)

    @staticmethod
    def sortByLastWatchedOldest(listWatchItem: List['WatchItem']) -> List['WatchItem']:
        """
        Fungsi sortir list film berdasarkan tanggal terakhir tonton secara menaik
        :param listWatchItem: list watch item yang akan disortir.

        :return: list watch item yang sudah disortir
        """
        return sorted(listWatchItem, key=lambda x: (x.getLastWatch(), x.getTitle()), reverse = False)

    @staticmethod
    def sortByReviewDateNewest(listWatchItem: List['WatchItem']) -> List['WatchItem']:
        """
        Fungsi sortir list film berdasarkan tanggal review secara menurun
        :param listWatchItem: list watch item yang akan disortir.

        :return: list watch item yang sudah disortir
        """
        return sorted(listWatchItem, key=lambda x: (x.getReviewDate() if (x.getReviewDate() is not None) else datetime.datetime.min, x.getTitle()), reverse = True)

    @staticmethod
    def sortByReviewDateOldest(listWatchItem: List['WatchItem']) -> List['WatchItem']:
        """
        Fungsi sortir list film berdasarkan tanggal review secara menaik
        :param listWatchItem: list watch item yang akan disortir.

        :return: list watch item yang sudah disortir
        """
        return sorted(listWatchItem, key=lambda x: (x.getReviewDate() if (x.getReviewDate() is not None) else datetime.datetime.max, x.getTitle()), reverse = False)