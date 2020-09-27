import pygame
pygame.init()
pygame.font.init()
class Square:
    """ 
        It is a class used to represent a square on gameboard
        =Data Members:
        -   Value : which store value on square
        -   pos   : stores the loctaion of square on game board (i,j) 2D format
        -   text  : value in text format
        -   Color : color of the square
        
    """
    font = pygame.font.SysFont('comicsansms', 32)
    Display = None
    def __init__(self,pos):
        """
           Initation of values
           required a list with 2 integer values eg: [1,2]
           assign value to pos
           Initally text is None
           Color is white
           calling update() function to insert into gameboard graphically
        """
        self.value = 0
        self.pos=pos
        self.text=None
        self.color=[255,255,255]
        self.update()

    def update(self,V=0):
        " It will update the color,value text contents once it is called for update"
        self.value=V
        self.colorUpdate()
        self.text=Square.font.render(str(self.value) if self.value!=0 else '  ' , True, (0,0,self.color[1]))
        pygame.draw.rect(Square.Display,self.color,(*self.pos,100,100))
        Square.Display.blit(self.text,(self.pos[0]+50 - self.text.get_width()//2,self.pos[1]+50-self.text.get_height()//2))
        pygame.display.update()

    def colorUpdate(self):
        """  It is used to update the color of the square based on value """
        if self.value ==0:
            self.color = [255,255,255]
            return
        k = 0
        V = self.value
        while V>0:
            k += 18
            V //= 2
        self.color = [k,255-k,0]

    def moveby(self,i,j,X,Y):
        """ 
           which is used to change the position of the square
           i,j : vector in which directon how much it have to move
           X,Y : is old position of the squre
           X+i,Y+j : is new position of the square
        """
        pygame.draw.rect(Square.Display,[255,255,255],(self.pos[0]+X,self.pos[1]+Y,100,100))
        pygame.draw.rect(Square.Display,self.color,(self.pos[0]+X+i,self.pos[1]+Y+j,100,100))
        Square.Display.blit(self.text,(self.pos[0]+X+i+50 - self.text.get_width()//2,self.pos[1]+Y+j+50-self.text.get_height()//2))
        pygame.display.update()
        
# Below code is used to test the above class

'''Square.Display=pygame.display.set_mode((400,400))
s=Square((100,100))
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            X = 0
            Y = 0
            if event.key == pygame.K_UP:
                for i in range(0,51):
                    s.moveby(0,-2,0,Y)
                    Y -= 2
                  
            elif event.key == pygame.K_DOWN:
                for i in range(0,51):
                    s.moveby(0,2,0,Y)
                    Y += 2
                    
            elif event.key == pygame.K_RIGHT:
                for i in range(0,51):
                    s.moveby(2,0,X,Y)
                    X += 2
                    
            elif event.key == pygame.K_LEFT:
                for i in range(0,51):
                    s.moveby(-2,0,X,Y)
                    X -= 2 '''

