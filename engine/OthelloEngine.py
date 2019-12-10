import time
import json
import sys
import copy

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

      # Initiaize white_team_file and black_team_file's AIs
      # (might want to refer to http://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/)
      if white_team_file.endswith('.py'):
         white_team_file = white_team_file[:-3]
      if black_team_file.endswith('.py'):
         black_team_file = black_team_file[:-3]
      w_module = __import__(white_team_file)
      b_module = __import__(black_team_file)
      self.white_team = getattr(w_module, "Othello_AI")('W', n, time_limit)
      self.black_team = getattr(b_module, "Othello_AI")('B', n, time_limit)
      # Add the initial tokens to the board (class names will all be Othello_AI)
      self.game_state[n//2-1][n//2-1]="W"
      self.game_state[n//2][n//2]="W"
      self.game_state[n//2-1][n//2]="B"
      self.game_state[n//2][n//2-1]="B"
      # call play_game (returns winner)
      self.winner = self.play_game()
      # call output_game
      self.output_game(self.winner)
      
    # Makes all of the general calls to play the game
   def play_game(self):
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
      while True:
         # Each team takes their turn
         for team in (self.black_team, self.white_team):
             move = self.record_turn(team)
             # record_turn returns a character IFF the team's move
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
             # Odd turns white, even turns black
             self.turn_number += 1
   
   # Abstract turn taking
   def record_turn(self, team):
      try:
         start = time.time()
         move = team.get_move(copy.deepcopy(self.game_state))
         turnTime = time.time() - start

         if turnTime > self.time_limit:
            raise Exception("Team {} exceeded their time limit: {}".format(team.team_type, turnTime))
         elif not self.check_valid(move):
            raise Exception("Team {} made an invalid move: {}".format(team.team_type, move))

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
      # move format: ('B', (i, j)) or ('B', None)
      # check if the given move is valid for board_state
      # A move of None indicates the player is skipping their turn. This is only valid if
      #    there are no legal moves for this player/
      # You will want to use get_all_moves
      # return True if the move is legal, and False otherwise
      current_team = 'W' if self.turn_number % 2 == 1 else 'B'
      if (move[0] != current_team):
          return False
      
      vMoves = get_all_moves(self.game_state, move[0])
      if move[1] is None:
         if len(vMoves) is 0:
            return True
         else:
            return False
      else:
         if move in vMoves:
            return True
         else:
            return False
      pass

   # Perform move
   def update_board(self, move):
      # move format: ('B', (i, j)) or ('B', None)
      # update the board state given the current move
      # if the move is None, do nothing
      # Assume that is a valid move, no need for extra error checking
      if move[1] is not None:
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
      # write a game file to self.output_file
      # See the example json formatted file for details
      # Recall that all_moves will contain a list of every move in the game

      turns = []
      for i in range(len(self.all_moves)):
         player = self.all_moves[i][0]
         turn_index = i // 2 if player == 'B' else (i - 1) // 2
         turn = {"turn": i, "player": player, "time": self.turn_times[player][turn_index],
                 "move": self.all_moves[i][1]}
         turns.append(turn)

      white_count = sum(row.count('W') for row in self.game_state)
      black_count = sum(row.count('B') for row in self.game_state)
      game_statistics = {"numTurns": len(turns), "numBlack": black_count, "numWhite":
                             white_count}

      game_metadata = {"version": self.get_version(), "teamWhite": self.white_team.get_team_name(),
                       "teamBlack": self.black_team.get_team_name(), "winner": self.winner, "statistics": game_statistics,
                       "boardSize": self.n, "totalTime": self.total_time, "turns": turns}

      with open(self.output_file, "w") as out:
         json.dump(game_metadata, out, indent = 3)

   def get_version(self):
      """Returns the current version of the game engine
      """
      return 1.0    # update when the engine version is incremented

def get_all_moves(board_state, player):
   # Return a list of all possible moves for the given player ('W' or 'B')
   # Example return value: [('W', (2, 5)), ('W', (6, 4)), ... ]
   moves = []
   adjacencies = get_adjacencies()
   for x in range(len(board_state)):
      for y in range(len(board_state[x])):
         for adjacency in adjacencies:
            if(is_valid_move(x, y, adjacency[0], adjacency[1], board_state, player, False)):
               moves.append((player, (x, y)))
               break
   return moves

def get_adjacencies():
   adjacencies = []
   for dx in range(-1, 2):
      for dy in range(-1, 2):
         if(dx == 0 and dy == 0):
            continue
         adjacencies.append((dx, dy))
   return adjacencies

def is_valid_move(x, y, dx, dy, board_state, player, surrounds):
   if(board_state[x][y] != '-' and not surrounds):
      return False
   newx = x + dx
   newy = y + dy
   board_size = len(board_state)
   if(player == 'B'):
      enemy = 'W'
   else:
      enemy = 'B'
   if(newx < 0 or newx >= board_size or newy < 0 or newy >= board_size):
      return False
   newcolor = board_state[newx][newy]
   if(newcolor == enemy):
      return is_valid_move(newx, newy, dx, dy, board_state, player, True)
   if(newcolor == player):
      return surrounds
   return False

if __name__ == "__main__":
   if len(sys.argv) >= 3:
      GameEngine(white_team_file=sys.argv[1], black_team_file=sys.argv[2], output_file=sys.argv[3])
   else:
      print("Usage: " + sys.argv[0] + " white_bot.py black_bot.py replay_file.txt")
