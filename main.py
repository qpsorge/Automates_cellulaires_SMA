import sys, math, random
import pygame
import pygame.draw
import numpy as np
import json

__screenSize__ = (800,800) #(500,500) #(1280,1280)
__cellSize__ = 10 
__gridDim__ = tuple(map(lambda x: int(x/__cellSize__), __screenSize__))
__density__ = 3 

area_block = 4
space_between_blocks = 20
percentage_apparition = 80
percentage_alea_burning = 1
percentage_neighbor_burning = 60
percentage_neighbor_birth = 60

#BVR Blanc Vert Rouge
__colors__ = [(255,255,255),(0,200,0),(200,0,0)]

def getColorCell(n):
    return __colors__[n]

class Grid:
    _grid= None
    _gridbis = None
    #_indexVoisins = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    #Voisinage de Von Neumann
    _indexVoisins = [(-1,0),(0,-1),(0,1),(1,0)]
    def __init__(self):
        print("Creating a grid of dimensions " + str(__gridDim__))
        self._grid = np.zeros(__gridDim__, dtype='int8')
        self._gridbis = np.zeros(__gridDim__, dtype='int8')
        nx, ny = __gridDim__
        if True : # random blocks of trees
            for x in range(int(__gridDim__[0]/space_between_blocks)):
                for y in range(int(__gridDim__[1]/space_between_blocks)):
                    if(random.random()*100<percentage_apparition):
                        for length in range(area_block,2*area_block+1):
                            for height in range(area_block,2*area_block+1):
                                self._grid[x*space_between_blocks+length,y*space_between_blocks+height]=1
        elif False: # True to init with one block at the center
            self._grid[nx//2,ny//2] = 1
            self._grid[nx//2+1,ny//2] = 1
            self._grid[nx//2,ny//2+1] = 1
            self._grid[nx//2+1,ny//2+1] = 1
        elif False: # True to init with random values at the center
            mx, my = 20, 16
            ones = np.random.random((mx, my)) > 0.75
            self._grid[nx//2-mx//2:nx//2+mx//2, ny//2-my//2:ny//2+my//2] = ones
        else: # Else if init with glider gun
            a = np.fliplr(np.rot90(np.array(glidergun),3))
            mx, my = a.shape
            self._grid[nx//2-mx//2:nx//2+mx//2, ny//2-my//2:ny//2+my//2] = a


    def indiceVoisins(self, x,y):
        return [(dx+x,dy+y) for (dx,dy) in self._indexVoisins if dx+x >=0 and dx+x < __gridDim__[0] and dy+y>=0 and dy+y < __gridDim__[1]] 

    def voisins(self,x,y):
        return [self._grid[vx,vy] for (vx,vy) in self.indiceVoisins(x,y)]
   
    def sommeVoisins(self, x, y):
        return sum(self.voisins(x,y))

    def bruleVoisins(self, x, y):
        return True if 2 in self.voisins(x,y) else False

    def sumEnumerate(self):
        return [(c, self.sommeVoisins(c[0], c[1])) for c, _ in np.ndenumerate(self._grid)]

    def drawMe(self):
        pass

class Scene:
    _mouseCoords = (0,0)
    _grid = None
    _font = None

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode(__screenSize__)
        self._font = pygame.font.SysFont('Arial',25)
        self._grid = Grid()

    def drawMe(self):
        if self._grid._grid is None:
            return
        self._screen.fill((255,255,255))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen, 
                        getColorCell(self._grid._grid.item((x,y))),
                        (x*__cellSize__ + 1, y*__cellSize__ + 1, __cellSize__-2, __cellSize__-2))

    def drawText(self, text, position, color = (255,64,64)):
        self._screen.blit(self._font.render(text,1,color),position)

    def updateBrain(self,percentage_neighbor_burning=percentage_neighbor_burning,percentage_alea_burning=percentage_alea_burning,percentage_neighbor_birth=percentage_neighbor_birth):
        for c, s in self._grid.sumEnumerate():
            if self._grid._grid[c[0],c[1]] == 2: # Rouge devient Blanc : Mort
                ret = 0
            elif self._grid._grid[c[0],c[1]] == 1: # Vert devient Rouge si au moins 1 voisin: feu Avec percentage_neighbor_burning%
                if(self._grid.bruleVoisins(c[0],c[1]) and random.random()*100<percentage_neighbor_burning): #si au moins 1 voisin, l'arbre brule 
                    ret = 2
                elif(random.random()*100<percentage_alea_burning): # % de passer rouge en étant vert
                    ret = 2
                else: # sinon reste vert
                    ret=1
            else: # blanc devient Vert si 1 voisins : naissance
                ret = 1 if (1<=s<=3 and random.random()*100<percentage_neighbor_birth) else 0
            self._grid._gridbis[c[0], c[1]] = ret
        self._grid._grid = np.copy(self._grid._gridbis)



    def eventClic(self, coord, b):
        pass

    def recordMouseMove(self, coord):
        pass

def main():
    statis = {}
    for percentage_neighbor_burning in [1]:#i*10 for i in range(10)]:
        for percentage_neighbor_birth in [1]:#i*10 for i in range(10)]:
            for percentage_alea_burning in [1]:#i*10 for i in range(10)]:
                scene = Scene()
                clock = pygame.time.Clock()
                ticks=0
                done=False
                print(f"Turn {percentage_neighbor_burning}_{percentage_alea_burning}_{percentage_neighbor_birth}")
                while done == False:
                    stats=[]
                    scene.drawMe()
                    pygame.display.flip()
                    scene.updateBrain(
                        percentage_neighbor_burning=percentage_neighbor_burning,
                        percentage_neighbor_birth=percentage_neighbor_birth,
                        percentage_alea_burning=percentage_alea_burning
                    )
                    stats.append(np.sum(scene._grid._grid==1)/(scene._grid._grid.shape[0]*scene._grid._grid.shape[1]))
                    clock.tick(30)
                    ticks+=30
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: 
                            print("Exiting")
                            done=True
                    if(ticks%(30*200)==0):
                        done=True
                        index= f"neighbor_burning_{percentage_neighbor_burning}--neighbor_birth_{percentage_neighbor_birth}--alea_burning_{percentage_alea_burning}"
                        statis[index] = np.mean(stats)
    #json.dump(statis, open("simulation_ac_feu.json","w"))
    print(statis)
    pygame.quit()

if not sys.flags.interactive: main()

