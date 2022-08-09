'''
    Shriya Dhaundiyal
    CS 5001 Fall 2021
    Final Project
    GameBoard
        This class is the centre of control for the game.
        It handles the clicks, controls display and function
        of various components of the game, and provides for
        smooth functioning during game-play.
'''
import turtle
from math import sqrt
import random
from Buttons import Buttons
from CreateTiles import CreateTiles
import setup_game_board
from datetime import datetime
import time
import os.path
from os import path
import logging
import os, sys, traceback

class GameBoard:
    def __init__(self, puz_info):
        '''
        Method -- __init__
            This method creates an object gameboard
            and defines appropriate methods for the game play.

        Parameters -- self : object (tiles)
                      puz_info : dictionary containing puzzle info 

        Return -- None
        '''
        turtle.setup(800, 800)
        self.screen = turtle.Screen()
        self.dict_puz = puz_info
        #default used moves set to 0
        self.used_moves = 0

    def log_error(self, error_msg, error, location):
        '''
        Method -- log_error
            This method logs all the errors into a file

        Parameters -- self : object
                      error : String -  Error message to be printed
                      error_msg : String - Image location of error msg
                      location : function location
                      
        Return -- None
        '''
        # display error message for users
        self.err = turtle.Turtle()
        self.err.hideturtle()
        self.err.up()
        self.err.goto(0,0)
        self.err.down()
        self.err.showturtle()
        self.err.screen.addshape(error_msg)
        self.err.shape(error_msg)
        time.sleep(3)
        self.err.hideturtle()
        self.err.clear()
        
        # get present date and time
        now = time.ctime()

        # log all errors in the file
        with open("Error_log.err", mode="a", encoding="utf8") as outfile:
            outfile.write(f"{now} Error: {error} LOCATION: {location}() \n") 
        
    def start_display(self):
        '''
        Method -- start_display
            This method starts off the game and takes
            inputs from the players

        Parameters -- self : object

        Return -- None
        '''
        # Displaying splash screen
        self.screen.bgpic(".\Resources\splash_screen.gif")
        self.screen.title("CS5001 Sliding Puzzle Game")
        self.screen.update()
        time.sleep(3)
        self.screen.bgpic("")
        
        # dialog box for name input
        self.player_name = self.screen.textinput("CS5001 Puzzle Slide", "Your Name:")

        # dialog box for moves input. Default moves is 50. Max: 200, Min: 5.
        self.moves = int(self.screen.numinput("5001 Puzzle Slide - Moves", \
                                              "Enter the number of moves you want [5-200]?", \
                                              default=50, minval=5, maxval=200))
        # draw the shapes for gameboard area
        setup_game_board.game_board()
        
        # displays the interactive buttons - reset, load, quit
        self.load_buttons()

    def load_buttons(self):
        '''
        Method -- load_buttons
            This method loads the interactive buttons
            to load, reset, quit.

        Parameters -- self : Object

        Return -- None
        '''
        # calls class Buttons to make objects
        self.reset = Buttons("Reset", 100, -250, 80, 80, ".\Resources\\resetbutton.gif")
        self.load = Buttons("Load", 200, -250, 80, 76, ".\Resources\loadbutton.gif")
        self.quit = Buttons("Quit", 300, -250, 80, 53, ".\Resources\quitbutton.gif")

        # displays the buttons on screen 
        self.reset.show_button()
        self.load.show_button()
        self.quit.show_button()

    def read_leader_file(self):
        '''
        Method -- read_leader_file
            This method reads the file containing
            winner names and ccreates a list

        Parameters -- self : Object

        Return -- Boolean(True or False based on file existence)
        '''
        try:
            # create list of winners
            self.lst_players =[]
            with open("leaders.txt", mode="r", encoding="utf8") as infile:
                for each in infile:
                   self.lst_players.append(each.strip("\n"))
            return True

        # if file is not present, display error message
        except Exception as e:
            tb = sys.exc_info()[-1]
            stk = traceback.extract_tb(tb, 1)
            fname = stk[0][2]
            self.log_error(".\Resources\leaderboard_error.gif", \
                           "Could not open leaderboard.txt", fname )
            return False
            
    def setup_leader_list(self):
        '''
        Method -- setup_leader_list
            This method reads the file containing
            winners list and displays top 7
            players of the game

        Parameters -- self : Object

        Return -- None
        '''
        # check if file exists
        exists = self.read_leader_file()

        if exists:
            # display the leaders list
            self.leader_t = turtle.Turtle()
            self.leader_t.hideturtle()
            self.leader_t.up()
            self.leader_t.goto(255, 200)
            self.leader_t.down()
            style = ("Arial", 25,  "bold" )
            self.leader_t.write("Leaders ", font=style, align="center")

            x = 200
            y = 160
            # display the top 7 players
            for i in range(7):
                self.leader_t.hideturtle()
                self.leader_t.up()
                self.leader_t.goto(x, y)
                self.leader_t.down()
                style = ("Arial", 15,  "bold" )
                self.leader_t.write(f"{self.lst_players[i]}", font=style)

                # y offset between lines
                y -= 40

    def update_leaderboard(self):
        '''
        Method -- update_leaderboard
            This method adds on to the list of
            winners and updates the file

        Parameters -- self : Object

        Return -- None
        '''
        front_lst = []
        back_lst = []
        found = None 

        # present winner and his used moves
        add = f"{self.used_moves} : {self.player_name}"

        # check if the present winner defeats previous players
        for j in range(len(self.lst_players)):
            if self.used_moves <= int(self.lst_players[j].split(" : ")[0]):
                found = True
                # add the player at the correct position in the list
                front_lst = self.lst_players[ : j]
                back_lst = self.lst_players[j :]
                front_lst.append(add)
                front_lst.extend(back_lst)
                break
            else:
                found = False     

        if not found: 
            # add the player at the end of the list
            front_lst = self.lst_players.append(add)

        # update the leaders file
        with open("leaders.txt", mode="w", encoding="utf8") as outfile:
            for each in front_lst:
                outfile.write(each)
                outfile.write('\n')                       

    def tiles_info(self, file):
        '''
        Method -- tiles_info
            This method stores information about the
            puzzles in instance variables

        Parameters -- self : Object

        Return -- Boolean based on whether file is malformed or not
        '''
        malformed = False

        # name of the puzzle
        self.name = self.dict_puz[file][0][1]
        self.number = int(self.dict_puz[file][1][1])

        # find no. of rows and columns
        self.num = sqrt(self.number)
        if self.num % 1 != 0:
            malformed = True
        self.rows = int(self.num)
        self.columns = int(self.num)

        # check if size of images are within the limit
        self.size = int(self.dict_puz[file][2][1])
        if not self.size > 50 and not self.size < 110:
            malformed = True

        # check if thumbnail exists at given position
        self.thumbnail = self.dict_puz[file][3][1]
        if not path.exists(self.thumbnail):
            malformed = True

        # check if images exist at given location
        self.images = self.dict_puz[file][4:]
        for i in range(len(self.images)):
            if not path.exists(self.images[i][1]):                
                malformed = True

        # find blank tile
        for i in range(len(self.images)):
            loc = self.images[i][1]
            if loc == f"Images/{self.name}/blank.gif":
                self.blank_tile = loc

        # check if the puzzle is malformed or not
        if malformed:
            tb = sys.exc_info()[-1]
            stk = traceback.extract_tb(tb, 1)
            self.log_error(".\Resources\\file_error.gif", \
                           "Malformed Puzzle File!", "tiles_info")
            return False
        else:
            return True
        
    def orig_tiles(self):
        '''
        Method -- orig_tiles
            This method creates each tile as an object
            of its own

        Parameters -- self : Object

        Return -- None
        '''
        self.orig = []
        self.x = -340
        self.y = 310

        # create each tile as an object of its own, own turtle
        row_counter = 1
        for i in range(len(self.images)):
            self.orig.append(CreateTiles(self.name, self.images[i], self.blank_tile, \
                                         self.x, self.y, self.size, i))

            # arrange into rows and columns
            if row_counter < self.rows:
                self.x = self.x + 110
                row_counter += 1
            else:
                self.x = -340
                self.y = self.y - 110
                row_counter = 1

    def scramble_tiles(self):
        '''
        Method -- scramble_tiles
            This method generates a scrambled
            version of the puzzle.

        Parameters -- self : Object

        Return -- None
        '''
        # make copy of original placement
        self.scrambled_tiles = self.orig[:]

        # shuffle algorithm for tiles
        for i in range(len(self.scrambled_tiles) - 1, -1 , -1):
            r = random.randint(0, i)
            
            img_n = self.scrambled_tiles[i].get_image()
            img_r = self.scrambled_tiles[r].get_image()
           
            self.scrambled_tiles[i].set_image(img_r)
            self.scrambled_tiles[r].set_image(img_n)

    def display_player_moves(self):
        '''
        Method -- display_player_moves
            This method displays the no. of moves
            used by the player

        Parameters -- self : Object

        Return -- None
        '''
        self.moves_t = turtle.Turtle()
        self.moves_t.hideturtle()
        self.moves_t.speed(0)
        self.moves_t.up()
        self.moves_t.goto(-200, -265 )
        self.moves_t.down()
        style = ("Arial", 20,  "bold" )
        self.moves_t.write(f"Player Moves: {self.used_moves}", font=style, \
                           align="center")

    def display_tiles(self, file):
        '''
        Method -- display_tiles
            This method displays the puzzle on the screen.

        Parameters -- self : Object
                      file : puzzle to be displayed

        Return -- None
        '''
        # display each image / tile
        for each in self.scrambled_tiles:
            each.show_tile()
       
        # display the thumbnail
        self.thumb_t = turtle.Turtle()
        self.thumb_t.speed(0)
        self.thumb_t.hideturtle()
        # add thumbnail
        self.thumb_t.up()
        self.thumb_t.goto(300, 320)
        self.thumb_t.down()
        self.screen.addshape(self.thumbnail)
        self.thumb_t.shape(self.thumbnail)
        self.thumb_t.showturtle()
            
    def clear_tiles(self):
        '''
        Method -- clear_tiles
            This method clears the puzzle from the screen

        Parameters -- self : Object

        Return -- None
        '''
        # clear thumbnail
        self.thumb_t.clear()
        self.thumb_t.hideturtle()
        # clear puzzle
        for each in self.scrambled_tiles:
            each.clear_tile()
            
    def quit_program(self):
        '''
        Method -- quit_program
            This method quits the program

        Parameters -- self : Object

        Return -- None
        '''
        self.quit_game = turtle.Turtle()
        self.quit_game.screen.addshape(".\Resources\credits.gif")
        self.quit_game.shape(".\Resources\credits.gif")
        self.screen.update()
        time.sleep(2)
        turtle.bye()

    def check_quit(self, x, y):
        '''
        Method -- check_quit
            This method checks if the quit button was clicked
            and quits the game.

        Parameters -- self : Object
                      x : float -  clicked x coordinate
                      y : float - clicked y coordinate

        Return -- None
        '''
        # check if quit button was clicked
        if self.quit.clicked_region(x, y) == True:
            self.q = turtle.Turtle()
            self.q.hideturtle()
            self.q.up()
            self.q.goto(0,0)
            self.q.down()
            self.q.showturtle()
            # show quit message
            self.q.screen.addshape(".\Resources\quitmsg.gif")
            self.q.shape(".\Resources\quitmsg.gif")
            self.screen.update()
            time.sleep(2)
            self.screen.bgpic("")
            # show credits
            self.q.screen.addshape(".\Resources\credits.gif")
            self.q.shape(".\Resources\credits.gif")
            self.screen.update()
            time.sleep(2)
            turtle.clear()
            turtle.bye()

    def check_reset(self, x, y):
        '''
        Method -- check_reset
            This method checks if the reset button was clicked
            and unscrambles the puzzle

        Parameters -- self : Object
                      x : clicked x coordinate
                      y : clicked y coordinate

        Return -- None
        '''
        # if reset is clicked, display unscrambled puzzle
        if self.reset.clicked_region(x, y) == True:
            for i in range(len(self.scrambled_tiles)):
                self.scrambled_tiles[i].set_image(self.images[i])
            self.display_tiles(self.scrambled_tiles)
            
    def check_load(self, x, y):
        '''
        Method -- check_load
            This method checks if the load button was clicked
            and displays a list of puzzles that can be loaded

        Parameters -- self : Object
                      x : float - clicked x coordinate
                      y : float - clicked y coordinate

        Return -- None
        '''
        # if load button is clicked, display new puzzle
        if self.load.clicked_region(x, y) == True:
            
            # if files are more than 10, show error
            if len(self.dict_puz) > 10:
                self.log_error(".\Resources\\file_warning.gif", \
                               f"Too many files!", "check_load")

            # make a string of file names (10 max) that can be loaded
            display_file_names = ""
            count = 0
            for key, value in enumerate(self.dict_puz):
                display_file_names = display_file_names + str(value) + "\n"
                count += 1
                if count >= 10:
                    break
                
            # display message for loading and show files                
            prev_file = f"{self.name}.puz"
            self.file = self.screen.textinput("Load Puzzle",
                                              "Enter the name of the puzzle you wish to load."
                                              f" Choices are:\n{display_file_names}", )
            #if self.file in self.dict_puz:
            try:
                not_malformed = self.tiles_info(self.file)
                if not_malformed:
                    # clear puzzle from screen
                    self.clear_tiles()
                    # clear moves 
                    self.moves_t.clear()
                    self.moves_t.hideturtle()
                    # set used moves to zero
                    self.used_moves = 0
                    # load chosen puzzle
                    self.orig_tiles()
                    self.scramble_tiles()
                    self.display_tiles(self.file)
                # if file is malformed, left present file be active
                else:
                    self.tiles_info(prev_file)
            # if file foes not exist, log error
            except Exception as e:
                tb = sys.exc_info()[-1]
                stk = traceback.extract_tb(tb, 1)
                fname = stk[0][2]
                self.log_error(".\Resources\\file_error.gif", \
                               f"File {self.file} does not exist.", fname ) 

    def find_blank(self):
        '''
        Method -- find_blank
            This method finds the blank image location

        Parameters -- self : Object

        Return -- Boolean based on whether move is valid
        '''
        # find row and column of the blank tile
        counter = -1
        for i in range(self.rows):
            for j in range(self.columns):
                if self.scrambled_tiles[counter + 1].is_blank() == True:
                    self.blank_t = counter + 1
                    return (i, j) 
                counter += 1  

    def check_valid_moves(self):
        '''
        Method -- check_valid_moves
            This method checks if the location of the blank tile
            is adjacent to the clicked tile and if the move is
            valid

        Parameters -- self : Object

        Return -- Boolean( True if move is valid, false otherwise)
        '''
        # if the tiles are in same columns and adjacent rows
        if abs(self.blank_x - self.pres_x) == 1 and self.blank_y == self.pres_y:
            return True
        # if the tiles are in same rows and adjacent columns
        if abs(self.blank_y - self.pres_y) == 1 and self.blank_x == self.pres_x:
            return True
        return False

    def update_board(self):
        '''
        Method -- update_board
            This method updates the tile board after a swap is made

        Parameters -- self : Object

        Return -- None
        '''
        turtle.tracer(0)
        self.display_tiles(self.scrambled_tiles)
        turtle.tracer(1)
    
    def check_for_win(self):
        '''
        Method -- check_for_win
            This method checks if the puzzle has been solved by the
            player

        Parameters -- self : Object

        Return -- True if player wins the game
        '''
        counter = -1
        for i in range(len(self.scrambled_tiles)):
            img_present = self.scrambled_tiles[i].get_image()
            if self.scrambled_tiles[i] == self.images[i]:
                counter = 1
            else:
                counter = -1
                break
        # if every tile is in the correct position, display win message
        if counter == 1:
            self.win_t = turtle.Turtle()
            self.win_t.hideturtle()
            self.win_t.up()
            self.win_t.goto(0,0)
            self.win_t.down()
            self.win_t.showturtle()
            self.win_t.screen.addshape(".\Resources\winner.gif")
            self.win_t.shape(".\Resources\winner.gif")
            time.sleep(3)
            self.win_t.hideturtle()

            # update leaders list
            self.update_leaderboard()
            return True
        else:
            return False
            
    def swap(self):
        '''
        Method -- swap
            This method swaps the image locations of the blank
            and clicked tile if move is valid

        Parameters -- self : Object

        Return -- True if player won to end the game
        '''
        # if move is valid, make the swap
        if self.check_valid_moves() == True:
            # get the images 
            img1 = self.scrambled_tiles[self.pres_t].get_image()
            img2 = self.scrambled_tiles[self.blank_t].get_image()

            # swap and set the images
            self.scrambled_tiles[self.pres_t].set_image(img2)
            self.scrambled_tiles[self.blank_t].set_image(img1)

            # display the swap and increase used moves
            self.update_board()
            self.used_moves += 1
            # updates player moves
            self.moves_t.clear()
            self.display_player_moves()

            # check if the player won
            self.win = self.check_for_win()
            if self.win:
                return self.win
                
    def click_handler(self, x_clicked, y_clicked):
        '''
        Method -- click_handler
            This method handles the clicks of the user
            and calls on other functions based on the clicks

        Parameters -- self : Object
                    x_clicked : float - clicked x coordinates
                    y_clicked : float - clicked y coordinates

        Return -- None
        '''
        self.x_clicked = x_clicked
        self.y_clicked = y_clicked
        
        # check if quit is clicked
        self.check_quit(self.x_clicked, self.y_clicked)

        # check if reset button is clicked
        self.check_reset(self.x_clicked, self.y_clicked)

        # check if the load button is clicked
        self.check_load(self.x_clicked, self.y_clicked)

        # check if player has any moves left
        if self.used_moves < self.moves:
            # check row - column of clicked tile
            counter = -1
            found = -1
            for i in range(self.rows):
                for j in range(self.columns):
                    counter += 1
                    if self.scrambled_tiles[counter].clicked_area(self.x_clicked, self.y_clicked) == True:
                        self.pres_x = i
                        self.pres_y = j
                        self.pres_t = counter 
                        found = 1
                        break
                if found == 1:
                    break

            # if clicked area is identified as an image, call swap()
            if found == 1:
                # check the row - column of blank tile
                self.blank_x, self.blank_y = self.find_blank()
                is_win = self.swap()
                # if plaer won, quit the game
                if is_win:
                    self.quit_program()

        # if player moves are over, they lose the game
        else:
            self.lose_t = turtle.Turtle()
            self.lose_t = turtle.Turtle()
            self.lose_t.hideturtle()
            self.lose_t.up()
            self.lose_t.goto(0,0)
            self.lose_t.down()
            self.lose_t.showturtle()
            self.lose_t.screen.addshape(".\Resources\Lose.gif")
            self.lose_t.shape(".\Resources\Lose.gif")
            time.sleep(5)
            self.lose_t.hideturtle()
            self.quit_program()
