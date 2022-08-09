'''
    Shriya Dhaundiyal
    CS 5001 Fall 2021
    Final Project
    Buttons
        This class creates each interactive button (load, quit,
        reset) as an object of its own and defines appropriate
        methods for it.
'''
import turtle

class Buttons:

    def __init__(self, name, x, y, width, height, image):
        '''
        Method -- __init__
            This method initializes the load, reset and quit button as its
            own object and gives its own turtle.

        Parameters -- self : object
                      name : String - name of object
                      x : float - x position on board
                      y : float - y position on board
                      width : float -the width of the image
                      height : float - the height of the image
                      image : string - image location

        Return -- None
        '''
        # every tile has a turtle of its own
        self.screen = turtle.Screen()
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.name = name
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def show_button(self):
        '''
        Method -- show_button
            This method displays the buttons on the screen at their
            appropriate positions.

        Parameters -- self : object 
                
        Return -- None
        '''
        self.t.hideturtle()
        self.t.up()
        # goes to the midpoint position of the image
        self.t.goto(self.x, self.y)
        self.t.down()
        self.t.showturtle()
        self.screen.addshape(self.image)
        self.t.shape(self.image)

    def clear_tile(self):
        '''
        Method -- clear
             This method clears the turtle.

        Parameters -- self : object
                    
        Return -- None 
        '''
        self.t.reset()
        self.t.hideturtle()

    def get_t(self):
        '''
        Method -- get_t
            This method returns the turtle of the tile.

        Parameters -- self : object 
                
        Return -- turtle of the button
        '''
        return self.t
    
    def get_x(self):
        '''
        Method -- get_x
             This method returns the x coordinates of the object.

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

    def clicked_region(self, x, y):
        '''
        Method -- clicked_region
             This method checks if the button has
             been clicked.

        Parameters -- self : object (tile)
                      x : float - clicked x coordinate
                      y : float - clicked y coordinate
                    
        Return -- Boolean (True / False based on whether the click
                  is in the bounds of the button)
        '''
        # return true if the click is within the x-y bounds of the button
        if x > (self.x - (self.width / 2)) and x < (self.x + (self.width / 2)):
            if y > (self.y - (self.height / 2)) and y < (self.y + (self.height / 2)):
                return True
        # return false if the click is not within the x-y bounds of the button
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
        return f"This is {self.name} button!"
