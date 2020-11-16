import pygame
import pickle
from numpy import array
from random import choice
from game import Game
from gameboard import GameBoard
pygame.init()
pygame.font.init()
pygame.display.set_caption("2048")
icon = pygame.image.load('2048_IC5_2.ico')
pygame.display.set_icon(icon)

class Main:
    """ It is the main class which handles all the menus like as followes:
        1. MainMenu
        2. GameOver Menu
        3  Game Won Menu
        
        Controls game 
        Loads old game/ new game based on inputs 
        """
    def __init__(self):
        self.Display=pygame.display.set_mode((410, 410))
        font=pygame.font.SysFont('comicsansms',35)
        self.Newgame=font.render('New Game',True,[32,27,29])
        self.Continue=font.render('Continue',True,[32,27,29])
        self.Exit=font.render('Exit',True,[32,27,29])
        font=pygame.font.SysFont('comicsansms',80)
        self.Won=font.render('U WON',True,[200,200,200])
        self.GameOver=font.render('Game Over',True,[200,200,200])
        self.Game=None

    def start(self):
        """
        After loadin the game in Game variable This function is called
        
        It is used to start and handle the whole game by calling differnet function
        
        Game.playgame() // To play game
           it return different values like 'Exit','resuem','GameOver','Won','newgame'
           
           Based on the ouputs given by the playgame() function other events are initianted 
           
        Game is controled by single variable (runing)
           True - continues
           False - Breaks
        Returns
        -------
        None.

        """
        running = True
        while running:
            k=self.Game.playgame()
            if k=='Exit':
                running = False
                continue
            elif k=='resume':
                continue
            elif k=='GameOver':
                o=self.gameover()
                if o=='newgame':
                    self.Game=Game(self.Display)
                else:
                    running = False
            while k=='Won':
                o=self.won()
                if o=='newgame':
                    self.Game=Game(self.Display)
                    break
                elif o=="Exit":
                    output = self.Game.popup()
                    if output == 'resume':
                        self.Game.GameBoard.display()
                        continue
                else:
                    running = True
                    break



    def mainmenu(self):
        """ main menu 
            Menu display while opening the game
            1. Continue
            2. New Game
            3. Exit
            
            continue
              calls resume function to load the old game into Game object
              return None
            
            newgame
              creates a game object newly
              return None
              
           exit
              return 'exit' (String)
        """
        l=[2,4,8,16,32,64,0,0,0,0,0]
        try:
            pickle_in = open('.\\2048.txt','rb')
            a = pickle.load(pickle_in)
            GameBoard.highScore = a[4,3]
            pickle_in.close()
        except:
            GameBoard.highScore = 0
        board=GameBoard(self.Display)
        board.restore(array([choice(l) for i in range(16)]).reshape((4,4)))
        board.display()
        for i in range(100,85,-1):
            font=pygame.font.SysFont('comicsansms', i)
            _2048=font.render('2048',True,[i*2,i*2,i*2])
            self.Display.blit(_2048,(205-_2048.get_width()//2,100-_2048.get_height()//2))
            pygame.display.update()
        font=pygame.font.SysFont('comicsansms', 85)
        _2048=font.render('2048',True,[106,106,150])
        self.Display.blit(_2048,(205-_2048.get_width()//2,100-_2048.get_height()//2))
        pygame.draw.rect(self.Display,[200,97,48],(60,140,290,70))
        pygame.draw.rect(self.Display,[200,97,48],(60,230,290,70))
        pygame.draw.rect(self.Display,[200,97,48],(60,320,290,70))
        pygame.draw.rect(self.Display,[106,106,150],(65,145,280,60))
        pygame.draw.rect(self.Display,[106,106,150],(65,235,280,60))
        pygame.draw.rect(self.Display,[106,106,150],(65,325,280,60))
        pygame.display.update()
        self.Display.blit(self.Continue,[205-self.Continue.get_width()//2,175-self.Continue.get_height()//2])
        self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
        self.Display.blit(self.Exit,[205-self.Exit.get_width()//2,355-self.Exit.get_height()//2])
        pygame.display.update()
        running=True
        while running:
            x,y=pygame.mouse.get_pos()
            if x>64 and x<345:
                if y>144 and y<206:
                    pygame.draw.rect(self.Display,[200,97,48],(65,145,280,60))
                    self.Display.blit(self.Continue,[205-self.Continue.get_width()//2,175-self.Continue.get_height()//2])
                else:
                    pygame.draw.rect(self.Display,[106,106,150],(65,145,280,60))
                    self.Display.blit(self.Continue,[205-self.Continue.get_width()//2,175-self.Continue.get_height()//2])
                if y>234 and y<295:
                    pygame.draw.rect(self.Display,[200,97,48],(65,235,280,60))
                    self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
                else:
                    pygame.draw.rect(self.Display,[106,106,150],(65,235,280,60))
                    self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
                if y>324 and y<386:
                    pygame.draw.rect(self.Display,[200,97,48],(65,325,280,60))
                    self.Display.blit(self.Exit,[205-self.Exit.get_width()//2,355-self.Exit.get_height()//2])
                else:
                    pygame.draw.rect(self.Display,[106,106,150],(65,325,280,60))
                    self.Display.blit(self.Exit,[205-self.Exit.get_width()//2,355-self.Exit.get_height()//2])
                pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return 'exit'

                if event.type==pygame.MOUSEBUTTONDOWN:
                    x,y=pygame.mouse.get_pos()
                    if x>64 and x<345:
                        if y>144 and y<206:
                            self.resume()
                            return

                        elif y>234 and y<295:
                            self.Game=Game(self.Display)
                            return

                        elif y>324 and y<386:
                            return 'exit'

    def resume(self):
        """ To reload the game from file to continue the previous game """
        self.Game=Game(self.Display)
        try:
            pickle_in=open('.\\2048.txt','rb')
        except:
            return
        a=pickle.load(pickle_in)
        self.Game.GameBoard.restore(a)
        pickle_in.close()

    def gameover(self):
        """
        Menu gets generated with two buttons
          newgame
          exit
        
        Returns
        -------
        None value (Exit/Quit) gameover going to exit
        "newgame" if play wants to start a newgame again
            DESCRIPTION.
        """
        self.Display.blit(self.GameOver,[205-self.GameOver.get_width()//2,150-self.GameOver.get_height()//2])
        pygame.draw.rect(self.Display,[200,97,48],(60,230,290,70))
        pygame.draw.rect(self.Display,[200,97,48],(60,320,290,70))
        pygame.draw.rect(self.Display,[106,106,150],(65,235,280,60))
        pygame.draw.rect(self.Display,[106,106,150],(65,325,280,60))
        pygame.display.update()
        self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
        self.Display.blit(self.Exit,[205-self.Exit.get_width()//2,355-self.Exit.get_height()//2])
        pygame.display.update()
        while True:
            x,y=pygame.mouse.get_pos()
            if x>64 and x<345:
                if y>234 and y<295:
                    pygame.draw.rect(self.Display,[200,97,48],(65,235,280,60))
                    self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
                else:
                    pygame.draw.rect(self.Display,[106,106,150],(65,235,280,60))
                    self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
                if y>324 and y<386:
                    pygame.draw.rect(self.Display,[200,97,48],(65,325,280,60))
                    self.Display.blit(self.Exit,[205-self.Exit.get_width()//2,355-self.Exit.get_height()//2])
                else:
                    pygame.draw.rect(self.Display,[106,106,150],(65,325,280,60))
                    self.Display.blit(self.Exit,[205-self.Exit.get_width()//2,355-self.Exit.get_height()//2])
                pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.Game.dontSave()
                    return
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    x,y=pygame.mouse.get_pos()
                    if x>64 and x<345:
                        if y>234 and y<296:
                            return 'newgame'
                        elif y>324 and y<386:
                            self.Game.dontSave()
                            return

    def won(self):
        """
           generates a menu if player won the game 
           1. Newgame
           2. continue
           
           we can use cross to exit from game 
        """
        self.Display.blit(self.Won,[205-self.Won.get_width()//2,150-self.Won.get_height()//2])
        pygame.draw.rect(self.Display,[200,97,48],(60,230,290,70))
        pygame.draw.rect(self.Display,[200,97,48],(60,320,290,70))
        pygame.draw.rect(self.Display,[106,106,150],(65,235,280,60))
        pygame.draw.rect(self.Display,[106,106,150],(65,325,280,60))
        pygame.display.update()
        self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
        self.Display.blit(self.Continue,[205-self.Continue.get_width()//2,355-self.Continue.get_height()//2])
        pygame.display.update()
        while True:
            x,y=pygame.mouse.get_pos()
            if x>64 and y<345:
                if y>234 and y<295:
                    pygame.draw.rect(self.Display,[200,97,48],(65,235,280,60))
                    self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
                else:
                    pygame.draw.rect(self.Display,[106,106,150],(65,235,280,60))
                    self.Display.blit(self.Newgame,[205-self.Newgame.get_width()//2,265-self.Newgame.get_height()//2])
                if y>324 and y<386:
                    pygame.draw.rect(self.Display,[200,97,48],(65,325,280,60))
                    self.Display.blit(self.Continue,[205-self.Continue.get_width()//2,355-self.Continue.get_height()//2])
                else:
                    pygame.draw.rect(self.Display,[106,106,150],(65,325,280,60))
                    self.Display.blit(self.Continue,[205-self.Continue.get_width()//2,355-self.Continue.get_height()//2])
                pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.Game.GameBoard.display()
                    return "Exit"
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    x,y=pygame.mouse.get_pos()
                    if x>64 and x<345:
                        if y>234 and y<296:
                            return 'newgame'
                        elif y>324 and y<386:
                            return

if __name__ == "__main__":
    """ main is the object of Main class will handle whole game 
        creates a menu takes input
        if player wants to exit from main menu exit
        if not enter into game by using main.start() function
    """
    main=Main()
    if main.mainmenu() != 'exit':
        main.start()
    pygame.quit()
