#  automated scoreboard

import time
class cricket:
    def __init__(self, team1,team2,overs):

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
        self.setup_scorecard()
        self.max_wickets=len(team1)-1
      
        

    

       

    def setup_scorecard(self):
        for player in self.team1 :
            self.scorecard[player] = {"Runs": 0, "Wickets": 0, "Balls": 0,'Status':'not out'}
        
    # def wicket_way(self):
        # wicket_type= input("b for bowled ,  r for runout, l for lbw, c for caught. ")
    def match(self):
        if self.wickets >= self.max_wickets or  self.balls >= self.overs * 6:
        
            return False
    
        print(f"current_striker: {self.striker}")
        print(f"current_non_striker: {self.non_striker}")
        outcome = input("Enter the outcome (0 for dot, 1, 2, 3, 4, 6, W for wicket, WI for wide, N for no ball, B for leg bye and bye): ").strip().upper()
    
        if outcome == 'W':
            self.wicket_fallen = True
            self.wickets += 1
            self.current_over.append("W")
            self.next_batsman()
    
        elif outcome == 'WI':
            print("Wide ball! Extra run awarded.")
            self.total_runs += 1
            self.current_over.append("WI")  # Wide ball added to the over
    
        elif outcome == 'N':
            print("No ball! Extra run awarded.")
            self.total_runs += 1
            self.current_over.append("N")  # No ball added to the over
        
        elif outcome == 'B':
            print("Bye or leg bye! Runs don't count towards the batsman's score.")
            runs = int(input("Enter runs for bye/leg bye: ").strip())
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
            print(f"{self.striker} is out. New batsman is {self.batting_order[0]}")
            self.striker = self.batting_order.pop(0)
    def change_strike(self):
        print(f"Strike changed! {self.non_striker} is now on strike.")
        self.striker, self.non_striker = self.non_striker, self.striker

    def display_over(self):
        print(f"Over: {' '.join(self.current_over)}")
        self.current_over = []


    def display_score(self):
        print("scorboard:")
        print("------------")
        print(f"final score:{self.total_runs}/{self.wickets}")
        print("------------")
        print(f"overs:{self.overs}")
    
      
    def simulate_match(self,target=None):
        while self.match():
            if self.balls % 6 == 0:
                self.display_over()
                self.change_strike()
            if self.wicket_fallen:
                print(f"Wicket fallen! Total Wickets: {self.wickets}")
            if target is not None and self.total_runs>target:
                print(f" team 2 won!")
                break
            
            
                
            time.sleep(0.5)

        if self.current_over:
            self.display_over()
        self.display_score()



    def compare(self,target):
        if self.total_runs>target:
            print(f" team 2 won!")
            pass
        elif self.total_runs<target:
            print(f"team1 won by {target - self.total_runs} runs!")
        else: 
            print("It's a tie!")
        
# Get input for teams from the user
def get_team(team_name):
        team = []
        size=int(input("enter size of both teams"))
        print(f"Enter players for {team_name}----------- {size} players required")
        
        for i in range(1,size+1):
            player = input(f"Enter name for player {i}: ").strip()
            team.append(player)
        return team

# Get the number of overs
def get_overs():
        while True:
            try:
                overs = int(input("Enter the number of overs: ").strip())
                return overs
            except ValueError:
                print("Please enter a valid number.")

# Main game logic
def main():
    print("Welcome to the Cricket Match Simulation!")
    
    team1 = get_team("Team 1")
    team2 = get_team("Team 2")
    overs = get_overs()

    match1 = cricket(team1, team2, overs=overs)
    match1.simulate_match()

    target=match1.total_runs
    print(f"Target runs:{target}")

    match2 = cricket(team1, team2, overs=overs)
    match2.simulate_match(target)
    if match2.total_runs <= target:
        match2.compare(target)
    

if __name__ == "__main__":
    main()