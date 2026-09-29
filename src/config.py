"""
config.py : constantes partagées par les scripts (source unique).

BUDGET_LAG : décalage de publication de la situation mensuelle budgétaire, en mois. La situation du mois M est
             publiée début M+2 (vérifié 2023-2026 ; 2014-2019 = hypothèse, testée avec un décalage de 1 et de 3 mois).
TEST_START : premier mois de la période de test (validation glissante), commun à 04 et 06.
"""
BUDGET_LAG = 2
TEST_START = "2020-01"
