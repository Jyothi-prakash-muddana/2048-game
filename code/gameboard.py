from numpy import  array  # to create 4x4 matrix for gameboard 
from square import Square # to create objects for each square on gameboard
from random import choice # for choosing a random postoin,values for inserting new value  into gameboard
import pygame

pygame.init()

class GameBoard:
    Direction={'up':(0,-2),'down':(0,2),'left':(-2,0),'right':(2,0)}
    font = pygame.font.SysFont('Comicsansms',20)
    font_h = pygame.font.SysFont('comicsansms', 25)
    highScore = 0
    """It is used to represent the gameboard 
       class variable:
           Direction which is used to represnt some parameters based on direction in modify() function
       data members:
           board : stores all the square objects in 4x4 matrix format
           flag  : modification is done on board or not (True : done,False : not done)
           max   : stores the max value on board
           won   : Game Own or not
           gameOver : GameOver or not
    """
    def __init__(self,Display):
        """ Requires a Display to show the square on gameBoard
            default value
            board = with 16 square objects with 0 as value and i,j values as position 
            flag  = True
            max   = 2
            won   = False
            gameOver = False
            calling insert() function 
        """
        Square.Display=Display
        list=[Square((i,j)) for j in range(72,470,102) for i in range(2,400,102)]
        self.board=array(list).reshape((4,4))
        self.flag=True
        self.score = 0
        self.max=2
        self.won=False
        self.gameOver=False
        Square.Display.fill((255,255,255))
        pygame.draw.rect(Display,[0,0,255],(5,5,400,65))
        pygame.draw.rect(Square.Display,[255,255,0],(7,7,396,61))
        Score_h = GameBoard.font_h.render(' YOUR SCORE         HIGH SCORE', True, (255,0,0))
        Square.Display.blit(Score_h,(5,5))
        Score = GameBoard.font.render(str(self.score), True, (0,0,255))
        Square.Display.blit(Score,(20,40))
        Score = GameBoard.font.render(str(GameBoard.highScore), True, (0,0,255))
        Square.Display.blit(Score,(240,40))
        self.insert()

    def array(self):
        """  Generating an 4x4 matrix only with values on the gameboard to store """
        a=[self.board[i,j].value for i in range(0,4) for j in range(0,4)]+[0,self.max,self.score,GameBoard.highScore]
        return array(a).reshape((5,4))

    def restore(self,a):
        """ Regenerating the gameboard by taking values that are stored """
        GameBoard.highScore = a[4,3]
        self.score = a[4,2]
        self.max = a[4,1]
        if a.all()==None:
            self.score = 0
            self.max = 2
            return
        if self.max >= 2048:
            self.won = None
        for i in range(4):
            for j in range(4):
                self.board[i,j].value=a[i,j]

    def display(self):
        """ this is used to display the gameboard """
        if self.score !=0 :
            pygame.draw.rect(Square.Display,[255,255,0],(7,40,198,28))
            Score = GameBoard.font.render(str(self.score), True, (0,0,255))
            Square.Display.blit(Score,(20,40))
        pygame.draw.rect(Square.Display,[255,255,255],(0,80,410,410))
        for i in range(4):
            for j in range(4):
                self.board[i,j].update(self.board[i,j].value)

    def modify(self,event):
        """ This used to rotate the gameboard virtually
            so that we can use same function for all inputs with small modification on gameboard
            rules followed for player inputs:
                 Up    : No change 
                 Down  : Flip the rows 
                 Left  : Transpose then Flip the coloums
                 Right : Flip the rows then Transpose
                 
               After complicaton of updating the gameboard again 
                 Up    : No change
                 Down  : Flip the rows
                 Left  : Flip the coloumns then Transpose
                 Right : Transpose then Flip the coloumns
        """
        self.flag=False
        if event==pygame.K_DOWN:
            self.board[:,:]=self.board[::-1,:]
            self.update('down')
            self.board[:,:]=self.board[::-1,:]
        elif event==pygame.K_LEFT:
            self.board[:,:]=self.board.T[:,::-1]
            self.update('left')
            self.board[:,:]=self.board[:,::-1].T
        elif event==pygame.K_RIGHT:
            self.board[:,:]=self.board.T[::-1,:]
            self.update('right')
            self.board[:,:]=self.board[::-1,:].T
        elif event==pygame.K_UP:
            self.update('up')
        if self.flag:
            self.insert()

    def motion(self,direction,List):
        """ while modifying to give motion animation to the squares on board"""
        i,j = GameBoard.Direction[direction]
        X,Y = 0,0
        for m in range(0,51):
            for n in List:
                n.moveby(i,j,X,Y)
            X += i
            Y += j

    def shift(self,direction):
        """ While modifying to remove the blank spaces inbetween squares based on players input"""
        i=0
        while i<3:
            l=list()
            for j in range(4):
                if self.board[i,j].value==0:
                    l.extend(list(filter(lambda x:x.value!=0,list(self.board[i+1:,j]))))
            s = len(l)
            self.score += s
            if s==0:
                i+=1
                continue
            else:
                self.flag=True
            self.motion(direction,l)
            for j in range(4):
                if self.board[i,j].value==0:
                    for k in range(i+1,4):
                        self.board[k-1,j].update(self.board[k,j].value)
                    self.board[3,j].update()

    def update(self,direction):
        """ Update is used to initate modification of squared 
            1. shifting the values will take place to remove middle spaces inbetween squares
            2. merging will takeplace next and animation is give to it by using motion function
        """
        self.shift(direction)
        i=0
        while i<3:
            l=list()
            for j in range(4):
                if self.board[i,j].value==self.board[i+1,j] and self.board[i,j].value!=0:
                    l+=list(list(self.board[i+1:,j]))
            self.motion(direction,l)
            for j in range(4):
                if self.board[i,j].value==self.board[i+1,j].value and self.board[i,j].value!=0:
                    self.flag=True
                    self.board[i,j].update(self.board[i,j].value*2)
                    for k in range(i+2,4):
                        self.board[k-1,j].update(self.board[k,j].value)
                    self.board[3,j].update()
            i+=1

    def check(self):
        """ To check whether GameOver or not by checking any two square are adjancent and same """
        for i in range(3):
            for j in range(3):
                if self.board[i,j].value==self.board[i+1,j].value or self.board[i,j].value==self.board[i,j+1].value:
                    return
            if self.board[i,3].value == self.board[i+1,3].value or self.board[3,i].value == self.board[3,i+1].value:
                return
        self.gameOver=True

    def insert(self):
        """ To insert a new value on the gameboard at random position with either 2 or 4 randomly 
             it will update the score on screen also
        """
        pygame.draw.rect(Square.Display,[255,255,0],(7,40,198,28))
        Score = GameBoard.font.render(str(self.score), True, (0,0,255))
        Square.Display.blit(Score,(20,40))
        if self.score > GameBoard.highScore:
            GameBoard.highScore = self.score
            pygame.draw.rect(Square.Display,[255,255,0],(210,40,180,28))
            Score = GameBoard.font.render(str(GameBoard.highScore), True, (0,0,255))
            Square.Display.blit(Score,(240,40))
        l=list()
        for i in range(4):
            for j in range(4):
                if self.board[i,j].value==0:
                    l.append((i,j))
                elif self.max<self.board[i,j].value:
                    self.max=self.board[i,j].value
                    if self.max>=2048:
                        if self.won==None:
                            return
                        self.won=True
        if len(l)!=0 and self.flag:
            k=[2,2,2,2,2,2,2,2,4]
            self.board[choice(l)].update(choice(k))
        if len(l)==1:
            self.check()

# Below code is used to check Above class (testing Manually)
"""play=True
GameBoard=GameBoard(pygame.display.set_mode((410,410)))
while play:
    if GameBoard.gameOver:
        break
    if GameBoard.won==True:
        GameBoard.won=None
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play=False
            break
        elif event.type == pygame.KEYDOWN:
            GameBoard.modify(event.key)
pygame.quit()"""

