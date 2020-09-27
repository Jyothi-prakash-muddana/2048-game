from gameboard import GameBoard
import pygame
import pickle
pygame.init()
class Game:
    """ It acts as inteface between game and player
        like following :
            1.input from keyboard
            2.popup for asking to save /dont save game while closing in middle
            3.pause the game
    """
    def __init__(self,Display):
        """ here we need a Display to show popup windows on screen
            play      : it says about game is paused or playing
            GameBoard : to play game and display it
            save      : it save text to display in popup
            yes       :           ''
            no        :           ''
            x         : cross mark in popup
        """
        self.Display=Display
        self.play=True
        self.GameBoard=GameBoard(self.Display)
        font=pygame.font.SysFont('comicsansms', 32)
        self.save=font.render('Save' , True, [200,200,200])
        font=pygame.font.SysFont('comicsansms', 25)
        self.yes=font.render('YES',True,[200,200,200])
        self.no=font.render('NO',True,[200,200,200])
        font=pygame.font.SysFont('comicsansms', 17)
        self.x=font.render('X',True,[0,0,0])

    def playgame(self):
        """ This function will startgame
            Follow strings will be written by this function
            1. GameOver  -  when GameOvers
            2. Won       -  when play won the game by generating 
            3. resume    -  To resume the game if player wants to continue it
            4. Exit      -  player wants to exit from game
        """
        self.play=True
        self.GameBoard.display()
        while self.play:
            if self.GameBoard.gameOver:
                return 'GameOver'
            if self.GameBoard.won==True:
                self.GameBoard.won=None
                return 'Won'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.pause()
                if event.type == pygame.KEYDOWN:
                    self.GameBoard.modify(event.key)

    def pause(self):
        """ This will pause the game and calles popup() function """
        self.play=False
        return self.popup()

    def popup(self):
        """ This will generate popup with small menu
            Save:
                yes
                no
            cross vailabel on popup to resume
            String is written by this function
            1.resume - if he/she wants to continue the game
            2.Exit - if he/shw wants to exit by saving/Not saving it
        """
        pygame.draw.rect(self.Display,[150,0,0],(80,145,250,130))
        pygame.draw.rect(self.Display,[150,150,150],(85,150,240,120))
        pygame.draw.circle(self.Display,(250,128,114),(305,170) , 10)
        pygame.draw.rect(self.Display,[150,0,0],(111,200,80,50))
        pygame.draw.rect(self.Display,[0,150,0],(219,200,80,50))
        self.Display.blit(self.save,(205 - self.save.get_width()//2,180 - self.save.get_height()//2))
        self.Display.blit(self.yes,(259 - self.yes.get_width()//2,225 - self.yes.get_height()//2))
        self.Display.blit(self.no,(151 - self.no.get_width()//2,225 - self.no.get_height()//2))
        self.Display.blit(self.x,(290,162))
        pygame.display.update()
        while True:
            x,y=pygame.mouse.get_pos()
            for event in pygame.event.get():
                if x>294 and x<315 and y>159 and y<180:
                    pygame.draw.circle(self.Display,(255,0,0),(305,170) , 13)
                    self.Display.blit(self.x,(299,162))
                else:
                    pygame.draw.rect(self.Display,[150,150,150],(290,155,30,30))
                    pygame.draw.circle(self.Display,(250,128,114),(305,170) , 10)
                    self.Display.blit(self.x,(299,162))
                if y>199 and y<251:
                    if x>110 and x<192:
                        pygame.draw.rect(self.Display,[145,0,0],(106,198,90,55))
                        self.Display.blit(self.no,(151 - self.no.get_width()//2,225 - self.no.get_height()//2))
                    else:
                        pygame.draw.rect(self.Display,[150,150,150],(106,198,90,55))
                        pygame.draw.rect(self.Display,[150,0,0],(111,200,80,50))
                        self.Display.blit(self.no,(151 - self.no.get_width()//2,225 - self.no.get_height()//2))
                    if x>218 and x<300:
                        pygame.draw.rect(self.Display,[0,145,0],(214,198,90,55))
                        self.Display.blit(self.yes,(259 - self.yes.get_width()//2,225 - self.yes.get_height()//2))
                    else:
                        pygame.draw.rect(self.Display,[150,150,150],(214,198,90,55))
                        pygame.draw.rect(self.Display,[0,150,0],(219,200,80,50))
                        self.Display.blit(self.yes,(259 - self.yes.get_width()//2,225 - self.yes.get_height()//2))
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y=pygame.mouse.get_pos()
                    if x>294 and x<315 and y>159 and y<180:
                        return 'resume'
                    if y>199 and y<251:
                        if x>110 and x<192:
                            return self.dontSave()
                        elif x>218 and x<300:
                            return self.yesSave()
                        
    def dontSave(self):
        """ saving None value in the file if player dont want to save """
        pickle_out=open('.\\2048.txt','wb')
        pickle.dump(None,pickle_out)
        pickle_out.close()
        return 'Exit'
    
    def yesSave(self):
        """ saving the matrix generated by gameboard.GameBoard.array() function in GameBoard """
        pickle_out=open('.\\2048.txt','wb')
        pickle.dump(self.GameBoard.array(),pickle_out)
        pickle_out.close()
        return 'Exit'

# Below code is used for testing the class
"""Game=Game(pygame.display.set_mode((410,410)))
Game.playgame()"""
