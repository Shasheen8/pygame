import pygame
pygame.init()

win = pygame.display.set_mode((500,480))
# This line creates a window of 500 width, 500 height

pygame.display.set_caption("My New Game")

# This goes outside the while loop, near the top of the program
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bkFog.png')
char = pygame.image.load('standing.png')

clock= pygame.time.Clock()
bulletSound = pygame.mixer.Sound("bullets.wav")
killSound = pygame.mixer.Sound("bloop.wav")



music = pygame.mixer.music.load("post.mp3")
pygame.mixer.music.play(-1)

score = 0

class player():
    def __init__(self,x,y,height,width):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.vel= 8
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount= 0
        self.standing = True
        self.hitbox = (self.x+17,self.y+11, 29,60)


    def draw(self,win):  # We have 9 images for our walking animation, I want to show the same image for 3 frames
    # so I use the number 27 as an upper bound for walkCount because 27 / 3 = 9. 9 images shown
    # 3 times each animation.

        if man.walkCount +1 >= 27:
            man.walkCount=0

        if not(self.standing):
            if man.left:
                win.blit(walkLeft[man.walkCount//3], (man.x,man.y))
                man.walkCount +=1
            elif man.right:
                win.blit(walkRight[man.walkCount//3], (man.x,man.y))
                man.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x,self.y)) # If the character is standing still
            else:
                win.blit(walkLeft[0], (self.x,self.y))
        self.hitbox = (self.x+17,self.y+11, 29,60)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit (self):
        self.isJump=False
        self.jumpCount=10
        self.x=60
        self.y=410
        self.walkCount=0
        wording= pygame.font.SysFont('Times New Roman',100)
        text = wording.render('-5',1,(255,0,0))
        win.blit(text,(250-(text.get_width()/2) , 250-(text.get_height()/2) ))
        pygame.display.update()
        i=0
        while i< 300:
            pygame.time.delay (1)
            i+=1
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    i=301
                    pygame.quit()



class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius= radius
        self.color= color
        self.facing= facing
        self.vel = 8 * facing
    
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y), self.radius)



class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end= end
        self.path=[self.x,self.y] 
        self.walkCount= 5
        self.vel= 4
        self.hitbox = (self.x+17,self.y+2, 31,57)
        self.health= 10
        self.visible= True


    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount +1 >= 33:
                self.walkCount = 0
            if self.vel > 0 :
                win.blit(self.walkRight[self.walkCount// 3], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            pygame.draw.rect(win,(0,255,0), (self.hitbox[0],self.hitbox[1]-20, 50,10 ))
            pygame.draw.rect(win,(255,0,0), (self.hitbox[0],self.hitbox[1]-20, 50 - (5*(10-self.health)),10 ))
            self.hitbox = (self.x+17,self.y+2, 31,57)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        

    def move(self):
        if self.vel>0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else :
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        
    def explode(self):
        if self.health > 0:
            self.health -=1
        else:
            self.visible=False 

        print("Explode")


def redrawGameWindow():
    win.blit(bg,(0,0)) #  This will draw our background image at (0,0)
    text = font.render('Score:  ' + str(score),1, (0,0,255))
    win.blit(text,(370,10))
    man.draw(win)
    kill.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update() # This updates the screen so we can see our rectangle

#Main LOOP for character
font= pygame.font.SysFont('comicsans',20,True,True)
man= player(200,410,64,64)
kill = enemy(50,410,64,64,400)
shoothim= 0
bullets= []
run= True
while run:
    clock.tick(27) # This will delay the game the given amount of milliseconds. In our case 0.1 seconds will be the delay    

    if kill.visible== True:
        if man.hitbox[1] < kill.hitbox[1] + kill.hitbox[3] and man.hitbox[1] + man.hitbox[3] > kill.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > kill.hitbox[0] and man.hitbox[0] < kill.hitbox[0] + kill.hitbox[2]:
                man.hit()
                score -= 5

    if shoothim > 0:
        shoothim += 1
    if shoothim > 3:
        shoothim =0
    
    
    for event in pygame.event.get():   # This will loop through a list of any keyboard or mouse events.
        if event.type == pygame.QUIT:  # Checks if the red button in the corner of the window is clicked
            run= False   # Ends the game loop

    for bullet in bullets:
        if bullet.y - bullet.radius < kill.hitbox[1] + kill.hitbox[3] and bullet.y + bullet.radius > kill.hitbox[1]:
            if bullet.x + bullet.radius > kill.hitbox[0] and bullet.x - bullet.radius < kill.hitbox[0] + kill.hitbox[2]:
                killSound.play()
                kill.explode()
                bullets.pop(bullets.index(bullet))
                score +=1
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel 
        else:
            bullets.pop(bullets.index(bullet))

    keys= pygame.key.get_pressed() # This will give us a dictionary where each key has a value of 1 or 0. Where 1 is pressed and 0 is not pressed.

    if keys[pygame.K_SPACE] and shoothim==0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 3:
            bullets.append(projectile(round(man.x+ man.width // 2), round(man.y + man.height//2),6,(0,0,0),facing))
            shoothim = 1
    
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left= True
        man.right= False
        man.standing= False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.vel- man.width :
        man.x += man.vel
        man.left=False
        man.right= True
        man.standing= False
    else:
        man.standing= True
        man.walkCount=0

    if not(man.isJump):  #check if user is not jumping
        if keys[pygame.K_UP]:
            man.isJump=True
            man.left= False
            man.right= False
            man.walkCount= 0

    else:  # what happens when we jump
        if man.jumpCount >= -10:
            man.y -=(man.jumpCount *abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else:
            man.isJump= False
            man.jumpCount =10


    redrawGameWindow()


pygame.quit() # If we exit the loop this will execute and close our game
