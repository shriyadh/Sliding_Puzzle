'''
    Shriya Dhaundiyal
    CS 5001 Fall 2021
    Final Project
    CreateTile
        This class creates each tile of the puzzle as an object
        and defines appropriate methods for it.
'''
import turtle

class CreateTiles():
    def __init__(self, name, image, blank, x, y, size, ID):
        '''
        Method -- __init__
            This method initializes every tile as its
            own turtle.

        Parameters -- self : object (tiles)
                      name : String - name of puzzle
                      image : String - image location
                      blank - String - blank location
                      x : float - x position on board
                      y : float - y position on board
                      size : float - size of the image
                      ID : Int - Identiication no. for each tile 

        Return -- None
        '''
        # every tile has a turtle of its own
        self.screen = turtle.Screen()
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.pensize(3)
        self.t.hideturtle()
        self.name = name
        self.image = image
        self.blank = blank
        self.x = x
        self.y = y
        self.size = size
        self.id = self.image[0]

    def show_tile(self):
        '''
        Method -- show_tile
            This method displays the tiles on the screen
            at their appropriate positions.

        Parameters -- self : object 
                
        Return -- None
        '''
        self.t.hideturtle()

        # draw tiles
        self.t.up()
        self.t.goto(self.x, self.y)
        self.t.down()
        self.t.forward(self.size)
        self.t.right(90)
        self.t.forward(self.size)
        self.t.right(90)
        self.t.forward(self.size)
        self.t.right(90)
        self.t.forward(self.size)
        self.t.right(90)
        
        # set position for images
        self.t.up()
        self.t.goto(self.x + (self.size / 2) ,\
                    self.y - (self.size / 2))
        self.t.down()
        self.screen.addshape(self.image[1])
        self.t.shape(self.image[1])
        self.t.showturtle()
            
    def get_image(self):
        '''
        Method -- get_image
             This method returns the image location.

        Parameters -- self : object (tile)
                    
        Return -- image location 
        '''
        return self.image

    def set_image(self, other):
        '''
        Method -- set_image
             This method changes the image (location).

        Parameters -- self : object
                      other: String - (image location)
                    
        Return -- None 
        '''
        self.image = other

    def clear_tile(self):
        '''
        Method -- clear_tile
             This method clears the turtle.

        Parameters -- self : object
                    
        Return -- None 
        '''
        self.t.clear()
        self.t.hideturtle()

    def get_turtle(self):
        '''
        Method -- get_turtle
            This method returns the turtle of the tile.

        Parameters -- self : object (tile)
                
        Return -- turtle of the tile
        '''
        return self.t

    def get_ID(self):
        '''
        Method -- get_ID
            This method returns the identification no.
            of the tile.

        Parameters -- self : object (tile)
                
        Return -- ID number (int) 
        '''
        return self.id

    def get_x(self):
        '''
        Method -- get_x
             This method returns the x coordinate of the object.

        Parameters -- self : object (tile)
                    
        Return -- x coordinate 
        '''
        return self.x

    def get_y(self):
        '''
        Method -- get_y
             This method returns the y coordinate of the object.

        Parameters -- self : object (tile)
                    
        Return -- y coordinate 
        '''
        return self.y

    def clicked_area(self, x, y):
        '''
        Method -- clicked_area
             This method checks if the tile has
             been clicked.

        Parameters -- self : object (tile)
                      x : float - clicked x coordinate
                      y : float - clicked y coordinate
                    
        Return -- Boolean (True / False based on whether the click
                  is in the bounds of the tile
        '''
        # return true if the click is within the x-y bounds of the tile
        if abs(self.x - x) <= self.size   and abs(self.y - y) <= self.size:
               return True
        # return false if the click is not within the x-y bounds of the tile
        else:
            return False

    def is_blank(self):
        '''
        Method -- is_blank
             This method checks if it is the blank
             image or not.

        Parameters -- self : object (tile)
                    
        Return -- Boolean (True / False) if the tile is
                  blank or not
        '''
        # checks if the image is the blank or not
        if self.image[1] == self.blank:
            return True
        return False

    def __eq__(self, other):
        '''
        Method -- __eq__
            This method checks if two objects are equal or not.

        Parameters -- self :  (object)
                      other : String - Image location

        Return -- Boolean values (true if both images are at the
                  correct IDs, else False)
        '''

        if self.image == other:
            return True
        return False
        
    def __str__(self):
        '''
        Method -- __str__
            This method returns the information
            that would be displayed on screen when
            the object is printed.

        Parameters -- self (object)

        Return -- returns the string representation
                  of what would be displayed on screen
        '''
        return f"This is {self.image[1]} of the {self.name} puzzle!"
        
