import streamlit as st
import time

class Cricket:
    def __init__(self, team1, team2, overs):
        self.overs = overs
        self.total_runs = 0
        self.wickets = 0
        self.balls = 0
        self.current_over = []
        self.striker = team1[0]
        self.non_striker = team1[1]
        self.batting_order = team1[2:]
        self.team1 = team1
        self.team2 = team2
        self.scorecard = {}
        self.wicket_fallen = False
        self.max_wickets = len(team1) - 1
        self.setup_scorecard()

    def setup_scorecard(self):
        for player in self.team1:
            self.scorecard[player] = {"Runs": 0, "Wickets": 0, "Balls": 0, 'Status': 'not out'}

    def match(self, outcome):
        if self.wickets >= self.max_wickets or self.balls >= self.overs * 6:
            return False

        if outcome == 'W':
            self.wicket_fallen = True
            self.wickets += 1
            self.current_over.append("W")
            self.next_batsman()

        elif outcome == 'WI':
            self.total_runs += 1
            self.current_over.append("WI")

        elif outcome == 'N':
            self.total_runs += 1
            self.current_over.append("N")

        elif outcome == 'B':
            runs = int(st.number_input("Enter runs for bye/leg bye:", min_value=0, max_value=6))
            self.total_runs += runs
            self.current_over.append(f"B{runs}")
            self.balls += 1

        else:
            runs = int(outcome)
            self.total_runs += runs
            self.scorecard[self.striker]['Runs'] += runs
            self.scorecard[self.striker]['Balls'] += 1
            self.current_over.append(str(runs))

            if runs in [1, 3]:
                self.change_strike()

            self.balls += 1

        return True

    def next_batsman(self):
        if self.batting_order:
            self.striker = self.batting_order.pop(0)

    def change_strike(self):
        self.striker, self.non_striker = self.non_striker, self.striker

    def display_over(self):
        st.write(f"Over: {' '.join(self.current_over)}")
        self.current_over = []

    def display_score(self):
        st.write("Scoreboard:")
        st.write(f"Runs: {self.total_runs}/{self.wickets}")
        st.write(f"Overs: {self.balls // 6}.{self.balls % 6}")

    def simulate_match(self, target=None):
        return self.total_runs, self.wickets, self.balls

    def compare(self, target):
        if self.total_runs > target:
            return "Team 2 won!"
        elif self.total_runs < target:
            return f"Team 1 won by {target - self.total_runs} runs!"
        else:
            return "It's a tie!"

# Main game logic
def main():
    st.title("Cricket Match Simulation")

    if "match1" not in st.session_state:
        # Input for team names and players
        team1 = st.text_input("Enter Team 1 Name", value="Team 1")
        team2 = st.text_input("Enter Team 2 Name", value="Team 2")
        
        players_team1 = [st.text_input(f"Enter player {i+1} for {team1}", value=f"Player {i+1}") for i in range(11)]
        players_team2 = [st.text_input(f"Enter player {i+1} for {team2}", value=f"Player {i+1}") for i in range(11)]
        
        # Input for overs
        overs = st.number_input("Enter the number of overs:", min_value=1, max_value=50)

        if st.button("Start Match"):
            # Initialize match state
            st.session_state.match1 = Cricket(players_team1, players_team2, overs)
            st.session_state.match2 = Cricket(players_team2, players_team1, overs)
            st.session_state.target = None
            st.session_state.innings = 1
            st.session_state.score = 0

    if "match1" in st.session_state:
        match = st.session_state.match1 if st.session_state.innings == 1 else st.session_state.match2
        target = st.session_state.target
        
        st.write(f"Innings: {st.session_state.innings}")
        
        # Horizontal bowling outcome input
        bowling_options = ['0', '1', '2', '3', '4', '6', 'W', 'WI', 'N', 'B']
        cols = st.columns(len(bowling_options))
        outcome = None
        for i, opt in enumerate(bowling_options):
            if cols[i].button(opt):
                outcome = opt

        if outcome:
            # Simulate the match with the selected outcome
            match.match(outcome)
            
            # Display the scoreboard after every ball
            match.display_score()

            # Check if Team 1's innings is over
            if st.session_state.innings == 1 and match.balls >= match.overs * 6 or match.wickets >= match.max_wickets:
                st.session_state.target = match.total_runs+1
                st.write(f"Target for Team 2: {st.session_state.target}")
                st.session_state.innings = 2

            # Check if Team 2 surpasses the target
            elif st.session_state.innings == 2 and match.total_runs > st.session_state.target:
                st.write("Team 2 won!")
                st.session_state.clear()  # Reset the target for the next innings
                st.session_state.innings = 3  # End of the game

            # Check if match ends without exceeding the target
            if st.session_state.innings == 2 and match.balls >= match.overs * 6 or match.wickets >= match.max_wickets:
                result = match.compare(st.session_state.target)
                st.write(result)

if __name__ == "__main__":
    main()
