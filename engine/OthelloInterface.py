from OthelloEngine import get_all_moves
import random

class Othello_AI:
   def __init__(self, team_type, board_size=8, time_limit=2.0):
      # team_type will be either 'W' or 'B', indicating what color you are
      # board_size and time_limit will likely stay constant, but if you want this can add different challanges
      self.team_type = team_type
      
   def get_move(self, board_state):
      # board state will be an board_size by board_size array with the current state of the game.
      #       Possible values are: 'W', 'B', or '-'
      # Return your desired move (If invalid, instant loss)
      # Example move: ('W', (1, 6))
      moves = get_all_moves(board_state, self.team_type)
      if len(moves) > 0:
         return random.choice(moves)
      return None
      
   def get_team_name(self):
      # returns a string containing your team name
      return "Default bot"
