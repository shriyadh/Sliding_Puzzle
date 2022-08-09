'''
    Shriya Dhaundiyal
    CS 5001 Fall 2021
    Final Project
    setup_game_goard
       This program contains functions to set up the gamebaord area,
       leadership and status area.
'''
import turtle

def draw_shape(draw, width, height):
    '''
    Function -- draw_shape
        This function draws the play area, leaderboard
        and status area

    Parameters -- draw : turtle
                  width : int
                  height : int

    Return -- None
    '''
    # draws required shape
    draw.showturtle()
    draw.forward(width)
    draw.right(90)
    draw.forward(height)
    draw.right(90)
    draw.forward(width)
    draw.right(90)
    draw.forward(height)
    draw.right(90)
    draw.hideturtle()
    
def game_board():
    '''
    Function -- game_board
        This function creates the setup for the gamebaord area,
       leadership and status area.

    Parameters -- None

    Return -- None
    '''
    draw = turtle.Turtle()
    draw.hideturtle()
    draw.pencolor("black")
    draw.pensize(8)
    draw.speed(0)
    
    # draw game board
    draw.up()
    draw.goto(-370, 340)
    draw.down()
    draw_shape(draw, 500, 500)
    
    # draw leaderboard
    draw.pencolor("blue")
    draw.up()
    draw.goto(145, 340)
    draw.down()
    draw_shape(draw, 225, 500)
  
    # draw status area
    draw.pencolor("black")
    draw.up()
    draw.goto(-370, -180)
    draw.down()
    draw_shape(draw, 745, 150)
