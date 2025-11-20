import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_haku_hakee_oikean_pelaajan(self):
        player = self.stats.search("K")

        self.assertEqual(str(player), "Kurri EDM 37 + 53 = 90")

    def test_haku_vaaralla_nimella_palauttaa_none(self):
        player = self.stats.search("mrNobody")

        self.assertEqual(player, None)

    def test_team_metodia(self):
        team_players = self.stats.team("PIT")
        self.assertEqual(len(team_players), 1)

        self.assertEqual(str(team_players[0]), "Lemieux PIT 45 + 54 = 99")

    def test_hae_top_pisteet_oikein(self):
        top_3 = self.stats.top(3)
        self.assertEqual(len(top_3), 3)
        self.assertEqual(str(top_3[0]), "Gretzky EDM 35 + 89 = 124")
        self.assertEqual(str(top_3[1]), "Lemieux PIT 45 + 54 = 99")
        self.assertEqual(str(top_3[2]), "Yzerman DET 42 + 56 = 98")


    def test_hae_top_maalit_oikein(self):
        top_3 = self.stats.top(3,SortBy.GOALS)

        self.assertEqual(str(top_3[0]), "Lemieux PIT 45 + 54 = 99")
        self.assertEqual(str(top_3[1]), "Yzerman DET 42 + 56 = 98")
        self.assertEqual(str(top_3[2]), "Kurri EDM 37 + 53 = 90")


    def test_hae_top_syotot_oikein(self):
        top_3 = self.stats.top(3, SortBy.ASSISTS)

        self.assertEqual(str(top_3[0]), "Gretzky EDM 35 + 89 = 124")
        self.assertEqual(str(top_3[2]), "Lemieux PIT 45 + 54 = 99")
        self.assertEqual(str(top_3[1]), "Yzerman DET 42 + 56 = 98")

    def test_liian_monen_haku_toimii_oikein(self):
        top = self.stats.top(10)
        self.assertEqual(self.stats.top(10), "Too many!")
