
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
      # total time is the current sum of all of the player's turns
      self.all_moves = []
      self.turn_number = 0
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
      pass


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
      # move format: ('B', (i, j)) or ('B', None)
      # update the board state given the current move
      # if the move is None, do nothing
      # Assume that is a valid move, no need for extra error checking
      if move is not None:
         r = move[1][0]
         c = move[1][1]
         color = move[0]

         #left
         i = r
         j = c - 1
         while j >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               j -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at c-1
                  for index in range(c - j - 1):
                     self.game_state[i][j + index + 1] = color
               #end the loop
               break

         #left-up direction
         i = r - 1
         j = c - 1
         while i >= 0 and j >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i -= 1
               j -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at c-1, r-1
                  for index in range(c - j - 1):
                     self.game_state[i + index + 1][j + index + 1] = color
               #end the loop
               break

         #up
         i = r -1
         j = c
         while i >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r-1
                  for index in range(r - i - 1):
                     self.game_state[i + index + 1][j] = color
               #end the loop
               break

         #right-up direction
         i = r - 1
         j = c + 1
         while i >= 0 and j < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i -= 1
               j += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r-1, c+1
                  for index in range(r - i - 1):
                     self.game_state[i + index + 1][j - index - 1] = color
               #end loop
               break

         #right direction
         i = r
         j = c + 1
         while j < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               j += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at c+1
                  for index in range(j - c - 1):
                     self.game_state[i][j - index - 1] = color
               #end loop
               break

         #right-down
         i = r + 1
         j = c + 1
         while i < len(self.game_state) and j < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i += 1
               j += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r+1,c+1
                  for index in range(j - c - 1):
                     self.game_state[i - index - 1][j - index - 1] = color
               #end loop
               break

         #down
         i = r + 1
         j = c
         while i < len(self.game_state):
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i += 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r+1
                  for index in range(i - r - 1):
                     self.game_state[i - index - 1][j] = color
               #end loop
               break

         #left-down
         i = r + 1
         j = c - 1
         while i < len(self.game_state) and j >= 0:
            if self.game_state[i][j] != color and self.game_state[i][j] != '-':
               #it's opposite color, keep checking
               i += 1
               j -= 1
            else:
               if self.game_state[i][j] == color:
                  #it's the same color, go back and change till we are at r+1
                  for index in range(i - r - 1):
                     self.game_state[i - index - 1][j + index + 1] = color
               #end loop
               break

         #set the spot in the game_state
         self.game_state[r][c] = color


   # Check for end condition
   def check_end(self):
      # Check the board to see if the game can continue
      # If the game is over return the winner: 'W', 'B', or 'T'
      # Otherwise, return None

      if len(get_all_moves(self.game_state, 'W')) != 0 or len(get_all_moves(self.game_state, 'B')) != 0:
         return None

      white_count = sum(row.count('W') for row in self.game_state)
      black_count = sum(row.count('B') for row in self.game_state)

      if white_count == black_count:
         return 'T'
      elif white_count > black_count:
         return 'W'
      else:
         return'B'

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
