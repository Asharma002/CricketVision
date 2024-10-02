import streamlit as st
import time

class CricketMatch:
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
        self.max_wickets=len(team1)-1
        self.wicket_fallen = False
        self.setup_scorecard()

    def setup_scorecard(self):
        for player in self.team1:
            self.scorecard[player] = {"Runs": 0, "Balls": 0, 'Status': 'not out'}

    def match(self, outcome):
        if self.wickets >= self.max_wickets or self.balls >= self.overs * 6:
            return False

        if outcome == 'W':
            self.wicket_fallen = True
            self.wickets += 1
            self.current_over.append("W")
            self.balls += 1
            self.next_batsman()

        elif outcome == 'WI':
            st.write("Wide ball! Extra run awarded.")
            self.total_runs += 1
            self.current_over.append("WI")  # Wide ball added to the over

        elif outcome == 'N':
            st.write("No ball! Extra run awarded.")
            self.total_runs += 1
            self.current_over.append("N")  # No ball added to the over

        elif outcome == 'B':
            runs = st.number_input("Enter runs for bye/leg bye:", min_value=0, max_value=6, key="bye_runs")
            self.total_runs += runs
            self.current_over.append(f"B{runs}")
            self.balls += 1  # Ball counts for a bye

        else:
            runs = int(outcome)
            self.total_runs += runs
            self.scorecard[self.striker]['Runs'] += runs
            self.scorecard[self.striker]['Balls'] += 1
            self.current_over.append(str(runs))

            if runs in [1, 3]:
                self.change_strike()

            self.balls += 1  # Ball counts for a regular run

        return True

    def next_batsman(self):
        if self.batting_order:
            st.write(f"{self.striker} is out. New batsman is {self.batting_order[0]}")
            self.striker = self.batting_order.pop(0)

    def change_strike(self):
        st.write(f"Strike changed! {self.non_striker} is now on strike.")
        self.striker, self.non_striker = self.non_striker, self.striker

    def display_over(self):
        st.write(f"Over: {' '.join(self.current_over)}")
        self.current_over = []

    def display_score(self):
        st.write("### Scoreboard:")
        st.write(f"**Total runs:** {self.total_runs}/{self.wickets}")
        st.write(f"**Overs:** {self.balls // 6}.{self.balls % 6}")

    def simulate_match(self):
        if self.balls % 6 == 0 and self.balls != 0:
            self.display_over()
            self.change_strike()
        if self.wicket_fallen:
            st.write(f"**Wicket fallen! Total Wickets:** {self.wickets}")
            self.wicket_fallen = False  # Reset wicket flag after displaying

        if self.balls >= self.overs * 6:
            st.write("Innings Over!")
            self.display_score()
            return False

        return True


# Get input for teams from the user in Streamlit
def get_team(team_name):
    size = st.number_input(f"Enter size of {team_name}", min_value=2, max_value=11, key=f"size_{team_name}")
    team = []
    for i in range(1, size + 1):
        # Reduce text box size by using columns
        cols = st.columns([2, 4])  # The first column is for labels, the second for inputs
        with cols[1]:
            player = st.text_input(f"Player {i}", key=f"{team_name}_player_{i}").strip()
        team.append(player)
    return team


def display_match_summary(team1, team2, overs):
    st.write("### Match Summary")
    cols = st.columns([1, 1, 1])
    with cols[0]:
        st.write(f"**Team 1:**")
        for player in team1:
            st.write(player)
    with cols[1]:
        st.write(f"**Team 2:**")
        for player in team2:
            st.write(player)
    with cols[2]:
        st.write(f"**Overs:** {overs}")


# Main game logic in Streamlit
def main():
    st.title("Cricket Match Simulation")

    # Session state to store the match object
    if 'match' not in st.session_state:
        team1 = get_team("Team 1")
        team2 = get_team("Team 2")
        overs = st.number_input("Enter the number of overs:", min_value=1, max_value=50, key="overs")

        # Display the match summary
        if team1 and team2:
            display_match_summary(team1, team2, overs)

        if st.button("Start Match"):
            st.session_state.match = CricketMatch(team1, team2, overs)

    if 'match' in st.session_state:
        match = st.session_state.match

        # Horizontal bowling options
        st.write("### Select the outcome for the ball:")

        # Create 10 columns for each outcome, so they appear horizontally
        cols = st.columns(10)
        bowling_options = ['0', '1', '2', '3', '4', '6', 'W', 'WI', 'N', 'B']

        outcome = None
        for i, opt in enumerate(bowling_options):
            if cols[i].button(opt):
                outcome = opt

        if outcome:
            if match.simulate_match():
                match.match(outcome)
                match.display_score()

if __name__ == "__main__":
    main()