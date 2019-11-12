
class GameEngine:
	# team_white will be the file name of the white team's AI file
	# team_black will be the file name of the black team's AI file
    # output_file is the name of the file the game will be recorded to
	# nxn is the size of the board. Default is 8x8
	# time_limit is the amount of time for each turn in seconds
	def init(self, team_white, team_black, output_file, n = 8, time_limit = 2.0):
		self.n = n
		self.time_limit = time_limit
        self.output_file = output_file
        
        # game_state is an nxn array containing all of the positions on the board. 
        #       'W', 'B' and '-' are the possible values.
        # all_moves is a list of every move in the game (for output file). Example move: ('W', (1, 3))
        # turn_number track the current turn number
        self.all_moves = []
		self.turn_number = 0
        self.game_state = [['-' for _ in range(n)] for _ in range(n)]
            
		# TODO Below:
		# Initiaize team_white and team_black's AIs
        self.white_team = None
        self.black_team = None
		# Add the initial tokens to the board (class names will all be Othello_AI)
        # call play_game (returns winner)
		# call output_game
		
        
    # Makes all of the general calls to play the game
    def play_game(self):
        # TODO Below:
        # Loop through all the moves, calling .get_move(board_state) for each team.
        #       .get_move returns a move. Example move: ('B', (4, 5))
        # Call check_valid on each move. If an AI returns an invalid move, the game is over.
        # Call the update board method with the move
        # Call the check end condition on board
        # remeber to add each move to all_moves
        # Return the winner: 'W', 'B', or 'T'
        
	
	# Check valid move method
    def check_valid(self, move):
        # TODO Below:
        # move format: ('B', (i, j)) or ('B', None)
        # check if the given move is valid for board_state
        # A move of None indicates the player is skipping their turn. This is only valid if
        #    there are no legal moves for this player
        # return True if the move is legal, and False otherwise
	
	# Perform move
    def update_board(self, move):
        # TODO Below:
        # move format: ('B', (i, j)) or ('B', None)
        # update the board state given the current move and put the move in all_moves
        # if the move is None, do nothing
        # Assume that is a valid move, no need for extra error checking
        
    # Check for end condition
    def check_end(self):
        # TODO Below:
        # Check the board to see if the game can continue
        # If the game is over return the winner: 'W', 'B', or 'T'
        # Otherwise, return None
	
	# write to output file
    # winner should be either 'W' or 'B' or 'T'
    def output_game(self, winner):
        # TODO Below:
        # write a game file to self.output_file
        # See the example json formatted file for details
        # Recall that all_moves will contain a list of every move in the game


if __name__ == "__main__":
    if len(argv) >= 3:
        GameEngine(white_team=argv[1], black_team=argv[2], output_file=argv[3])
    else:
        print("Usage: " + argv[0] + " white_bot.py black_bot.py replay_file.txt")
