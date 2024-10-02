import unittest
from deploy import CricketMatch

class TestCricketMatchInitialization(unittest.TestCase):
    def test_init_with_correct_overs(self):
        overs = 50
        team1 = ["Player1", "Player2", "Player3"]
        team2 = ["Player4", "Player5", "Player6"]
        match = CricketMatch(team1, team2, overs)
        self.assertEqual(match.overs, overs)


    def test_update_scorecard_after_each_ball(self):
        overs = 50
        team1 = ["Player1", "Player2", "Player3"]
        team2 = ["Player4", "Player5", "Player6"]
        match = CricketMatch(team1, team2, overs)

        # Simulate a ball outcome
        outcome = 4  # 4 runs scored
        match.match(outcome)

        # Check if the scorecard is updated correctly
        expected_scorecard = {
            "Player1": {"Runs": 4, "Balls": 1, 'Status': 'not out'},
            "Player2": {"Runs": 0, "Balls": 0, 'Status': 'not out'},
            "Player3": {"Runs": 0, "Balls": 0, 'Status': 'not out'}
        }
        self.assertEqual(match.scorecard, expected_scorecard)



    def test_next_batsman_after_wicket_falls(self):
        overs = 50
        team1 = ["Player1", "Player2", "Player3"]
        team2 = ["Player4", "Player5", "Player6"]
        match = CricketMatch(team1, team2, overs)

        # Set initial state
        match.striker = "Player1"  # Player1 is on strike
        match.non_striker = "Player2"  # Player2 is non-striker

        # Simulate a wicket fall for Player1
        match.wicket_fallen = True
        match.wickets += 1
        match.next_batsman()

        # Expected outcome: Player2 stays at non-striker end, Player3 comes in as striker
        expected_striker = "Player3"
        self.assertEqual(match.striker, expected_striker)
        self.assertEqual(match.non_striker, "Player2")  # Player2 should still be at non-striker's end
        self.assertEqual(match.batting_order, [])
    def test_total_runs_scored_by_each_team(self):
        overs = 50
        team1 = ["Player1", "Player2", "Player3"]
        team2 = ["Player4", "Player5", "Player6"]
    def test_total_runs_scored_by_each_team(self):
        """
        This function simulates a cricket match and verifies the total runs scored by each team.

        Parameters:
        overs (int): The total number of overs in the match.
        team1 (list): A list of player names representing the first team.
        team2 (list): A list of player names representing the second team.
        match (CricketMatch): An instance of the CricketMatch class representing the ongoing match.

        Returns:
        None. The function asserts the total runs scored by each team and does not return any value.
        """
        overs = 50
        team1 = ["Player1", "Player2", "Player3"]
        team2 = ["Player4", "Player5", "Player6"]
        match = CricketMatch(team1, team2, overs)

        # Simulate a ball outcome for each player in team1
        for player in team1:
            for _ in range(10):  # Simulate 10 balls for each player
                outcome = 4  # 4 runs scored
                match.match(outcome)

        # Simulate a ball outcome for each player in team2
        for player in team2:
            for _ in range(10):  # Simulate 10 balls for each player
                outcome = 3  # 3 runs scored
                match.match(outcome)

        # Check if the total runs scored by each team is accurate
        expected_total_runs_team1 = 40 * len(team1)  # 40 runs per player * number of players in team1
        expected_total_runs_team2 = 30 * len(team2)  # 30 runs per player * number of players in team2
        self.assertEqual(match.total_runs, expected_total_runs_team1 + expected_total_runs_team2)
        match = CricketMatch(team1, team2, overs)

        # Simulate a ball outcome for each player in team1
        for player in team1:
            for _ in range(10):  # Simulate 10 balls for each player
                outcome = 4  # 4 runs scored
                match.match(outcome)

        # Simulate a ball outcome for each player in team2
        for player in team2:
            for _ in range(10):  # Simulate 10 balls for each player
                outcome = 3  # 3 runs scored
                match.match(outcome)

        # Check if the total runs scored by each team is accurate
        expected_total_runs_team1 = 40 * len(team1)  # 40 runs per player * number of players in team1
        expected_total_runs_team2 = 30 * len(team2)  # 30 runs per player * number of players in team2
        self.assertEqual(match.total_runs, expected_total_runs_team1 + expected_total_runs_team2)



if __name__ == '__main__':
    unittest.main()
    
