'''
    Shriya Dhaundiyal
    CS 5001 Fall 2021
    Final Project
    Puzzle Slider Game - Slider Puzzle
        This program makes a board game, loads different puzzle files,
        creates an interactive interface for the user which allows them
        to solve the puzzle within the no. of moves specified,
        reset the puzzle to get hints and quit the game!
'''
import turtle
import time
import os, sys
import setup_game_board
from Buttons import Buttons
from GameBoard import GameBoard
from CreateTiles import CreateTiles

def file_names():
    '''
    Function -- file_names
        This function gets all the puzzle files in
        the directory

    Parameters -- None

    Return -- returns a list of puz files in a folder
    '''
    puz_files = []
    for folder, sub_folder, files in os.walk(os.getcwd()):
        # access puz files for game
        for each in files:
            if each.split(".")[1] == "puz":
                puz_files.append(each)
    return puz_files

def create_dict(lst):
    '''
    Function -- create_dict

    Parameters -- lst : list containing file names 

    Return -- dictionary of all puz file with file name as key and
              list of information about puz files as values
    '''
    try:
        data_puz = []
        dictionary = {}
        for file in lst:
            with open(f"./{file}", mode="r", encoding='utf8') as infile:
                for each in infile:
                    data_puz.append(each.split())
                # file name is key, info is value
                dictionary[file] = data_puz
                data_puz = []
        return dictionary
             
    except OSError:
        print("File not found!")

def main():
    # find the puz files and create dictionary of information
    puz_files = file_names()
    dict_puz = create_dict(puz_files)
    
    # Start the game
    screen = turtle.Screen()
    gb = GameBoard(dict_puz)
    gb.start_display()
    gb.setup_leader_list()

    # set deafault puzzle to mario
    gb.tiles_info("mario.puz")
    gb.orig_tiles()

    # shuffle the puzzle file
    scrambled = gb.scramble_tiles()

    # display the puzzle and no. of moves
    gb.display_tiles(scrambled)
    gb.display_player_moves()

    # allow clicks by user 
    turtle.listen()
    screen.onclick(gb.click_handler)
    
if __name__ == "__main__":
    main()
