import time

class GameEngine:
   # white_team_file will be the file name of the white team's AI file
   # black_team_file will be the file name of the black team's AI file
   # output_file is the name of the file the game will be recorded to
   # nxn is the size of the board. Default is 8x8
   # time_limit is the amount of time for each turn in seconds
   def __init__(self, white_team_file, black_team_file, output_file, n = 8, time_limit = 2.0):
      self.n = n
      self.time_limit = time_limit
      self.output_file = output_file
      
      # game_state is an nxn array containing all of the positions on the board. 
      #       'W', 'B' and '-' are the possible values.
      # all_moves is a list of every move in the game (for output file). Example entry for move ('W', (1, 5)):
      #        { "turn": 0,
      #          "player": "W",
      #          "time":  1.4,
      #          "move": [1, 5]
      #        }
      # turn_number track the current turn number
      # turn_times keys each team's color character ('W' or 'B') to a list of their turn times
      # total time is the current sum of all of the player's turns
      self.all_moves = []
      self.turn_number = 0
      self.turn_times = {'W': [], 'B': []}
      self.total_time = 0
      self.game_state = [['-' for i in range(n)] for j in range(n)]
            
      # TODO Task 4 Below:
      # Initiaize white_team_file and black_team_file's AIs
      # (might want to refer to http://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/)
      self.white_team = None
      self.black_team = None
      # Add the initial tokens to the board (class names will all be Othello_AI)
      # call play_game (returns winner)
      # call output_game
      
      
   # Makes all of the general calls to play the game
   def play_game(self):
      # TODO Task 6 Below:
      # Loop through all the moves, calling .get_move(board_state) for each team.
      #       .get_move returns a move. Example move: ('B', (4, 5))
      #       Make sure that the bot doesn't throw an error (try-except) and doesn't exceed
      #       self.time_limit
      # Call check_valid on each move. If an AI returns an invalid move, the game is over.
      # Call the update board method with the move
      # Call the check end condition on board
      # remember to add each move to all_moves
      # Also track individual turn times as well as total time
      # Return the winner: 'W', 'B', or 'T'

      # Sanity check for self.check_end()
      while '-' in row in self.game_state:
         # Each team takes their turn
         for team in (self.white_team, self.black_team):
            move = self.record_turn(team)

            # execute_turn returns a character IFF the team's move
            # causes them to lose automatically
            if type(move) != tuple:
               return move

            # Else update the board and check if the game is over
            else:
               self.update_board(move)
               self.all_moves.append(move)

               gameEnd = self.check_end();
               if gameEnd != None:
                  return gameEnd

         # Increment turn
         self.turn_number += 1

      # Should be unreachable, if check_end functions
      return self.check_end()

   # Abstract turn taking
   def record_turn(self, team):
      try:
         start = time.time()
         move = team.get_move(self.game_state)
         turnTime = time.time() - start

         if turnTime > self.t or not self.check_valid(move):
            raise

         # Time keeping
         self.turn_times[team.team_type].append(turnTime)

         self.total_time += turnTime

         return move

      # Instant loss for the current team
      # if their turn exceeds the time limit
      # or their move is not valid
      # or their class raises an exception
      except:
         return 'B' if team.team_type == 'W' else 'W'

   # Check valid move method
   def check_valid(self, move):
      # TODO Task 5 Below:
      # move format: ('B', (i, j)) or ('B', None)
      # check if the given move is valid for board_state
      # A move of None indicates the player is skipping their turn. This is only valid if
      #    there are no legal moves for this player/
      # You will want to use get_all_moves
      # return True if the move is legal, and False otherwise
      pass
   
   # Perform move
   def update_board(self, move):
      # TODO Task 7 Below:
      # move format: ('B', (i, j)) or ('B', None)
      # update the board state given the current move and put the move in all_moves
      # if the move is None, do nothing
      # Assume that is a valid move, no need for extra error checking
      pass
      
   # Check for end condition
   def check_end(self):
      # TODO Task 8 Below:
      # Check the board to see if the game can continue
      # If the game is over return the winner: 'W', 'B', or 'T'
      # Otherwise, return None
      pass
   
   # write to output file
   # winner should be either 'W' or 'B' or 'T'
   def output_game(self, winner):
      # TODO Task 2 Below:
      # write a game file to self.output_file
      # See the example json formatted file for details
      # Recall that all_moves will contain a list of every move in the game
      pass

def get_all_moves(board_state, player):
   # TODO Task 9 Return a list of all possible moves for the given player ('W' or 'B')
   # Example return value: [('W', (2, 5)), ('W', (6, 4)), ... ]
   pass

if __name__ == "__main__":
   if len(argv) >= 3:
      GameEngine(white_team=argv[1], black_team=argv[2], output_file=argv[3])
   else:
      print("Usage: " + argv[0] + " white_bot.py black_bot.py replay_file.txt")
