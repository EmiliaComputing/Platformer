#imports
import arcade
import time

from enemy1 import Enemy1
from enemy2 import Enemy2
from player import Player
from coin import Coin

#define constants
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
SCREEN_TITLE = 'GAME'

#control the game window
class Game(arcade.Window):
    #initialise the game
    def __init__(self):
        #initialise the game
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #choose the background colour
        arcade.set_background_color(arcade.color.LA_SALLE_GREEN)

        #define more constants
        self.CHANGE_Y = 40
        self.CHANGE_X = 25

        #define variables
        self.up = self.CHANGE_Y * 2
        self.right = False
        self.left = False
        self.stop_y = False
        self.enemy2_down = False
        self.time = 0

        #define variables (coins)
        self.coins_l2 = False
        self.coins_l3 = False

    #draw the screen
    def on_draw(self):
        arcade.start_render()
        #screen after player loses
        if self.level == -1:
            arcade.draw_text('YOU LOSE', 141, 317, arcade.color.BLACK, 30)
            arcade.draw_text('CLICK HERE', 125, 267, arcade.color.BLACK, 30)
            arcade.draw_text('TO RESTART', 123, 217, arcade.color.BLACK, 30)
            self.hit_enemy = False

        #screen when game is first opened
        if self.level == 0:
            arcade.draw_text('CLICK HERE', 120, 277, arcade.color.BLACK, 30)
            arcade.draw_text('TO START', 141, 227, arcade.color.BLACK, 30)

        #level one - design/layout
        if self.level == 1:
            arcade.draw_rectangle_filled(55, 25, 50, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(115, 55, 50, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(175, 85, 50, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(235, 115, 50, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(295, 145, 50, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(420, 175, 175, 15, arcade.color.WHITE)

        #level two - design/layout
        if self.level == 2:
            self.enemy_list1.draw()
            
            arcade.draw_rectangle_filled(25, 175, 50, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(200, 135, 150, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(265, 170, 20, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(240, 205, 20, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(215, 240, 20, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(190, 275, 20, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(165, 310, 20, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(342, 345, 315, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(322, 360, 15, 30, arcade.color.WHITE)
            arcade.draw_rectangle_filled(395, 360, 15, 30, arcade.color.WHITE)

        #level three - design/layout
        if self.level == 3:
            self.enemy_list2.draw()
            arcade.draw_rectangle_filled(0, 345, 80, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(130, 345, 6, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(230, 345, 6, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(330, 345, 6, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(430, 345, 6, 15, arcade.color.WHITE)
            arcade.draw_rectangle_filled(478, 320, 90, 15, arcade.color.WHITE)

        #level four - design/layout - in progress
        if self.level == 4:
            self.player_list = arcade.SpriteList()
            arcade.draw_text('YOU WON', 141, 245, arcade.color.BLACK, 30)

        #draw in the player sprite when one of the levels is being player
        if (self.level > 0):
            self.player_list.draw()
            self.coin_list.draw()
            coins_text = f'COINS: {self.coins_collected}'
            arcade.draw_text(coins_text, 50, 450, arcade.color.BLACK, 15)

            if not(self.coins_l2):
                self.setup_coins_for_level2()
            if not(self.coins_l3):
                self.setup_coins_for_level3()
  
    #gravity
    def stop_up(self, min_x, max_x, max_y, min_y):
        if ((self.player_sprite.center_x > min_x) and
            (self.player_sprite.center_x < max_x) and
            (self.player_sprite.center_y < max_y) and
            (self.player_sprite.center_y > min_y)):
            self.stop_y = True
            return True
        
        else:
            return False

    #stop at blocks on the right
    def stop_right(self, min_x, max_x, max_y, min_y):
        if ((self.player_sprite.center_x > min_x) and
            (self.player_sprite.center_y > min_y) and
            (self.player_sprite.center_y < max_y) and
            (self.player_sprite.center_x < max_x)):
            self.player_sprite.center_x -= 1

    #stop at blocks on the left
    def stop_left(self, min_x, max_x, max_y, min_y):
        if ((self.player_sprite.center_x > min_x) and
            (self.player_sprite.center_y > min_y) and
            (self.player_sprite.center_y < max_y) and
            (self.player_sprite.center_x < max_x)):
            self.player_sprite.center_x += 1

    #move the player
    def move(self):
        if self.up < self.CHANGE_Y:
            self.player_sprite.center_y+=1
            self.up +=1
        elif not self.stop_y:
            self.player_sprite.center_y-=1
            self.up += 1

        if self.right:
            self.player_sprite.center_x+=1

        if self.left:
            self.player_sprite.center_x-=1
            
        if self.player_sprite.center_x > SCREEN_WIDTH:
            self.player_sprite.center_x = 0
            self.level += 1

        elif self.player_sprite.center_x < 0:
            if self.level > 1:
                self.level-=1
                self.player_sprite.center_x = SCREEN_WIDTH - 1
                
            else:
                self.player_sprite.center_x = 1

        if self.player_sprite.center_y < 0:
            self.level = -1

    def check_for_collision_with_coin(self):
        for coin in self.coin_list:
            check_hit_coin = arcade.check_for_collision(self.player_sprite, coin)

            if check_hit_coin:
                self.coins_collected += 1
                self.coin_list.remove(coin)

    #update
    def on_update(self, deltatime):
        self.time += 1
        #move enemies
        self.move_enemy1()
        self.move_enemy2()

        self.check_for_collision_with_coin()

        #check for collision between player and enemy
        check = arcade.check_for_collision(self.player_sprite, self.enemy_sprite1)

        if ((check) and
            (self.level == 2)):
            self.level =-1

        check2 = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list2)

        if ((check2) and
            (self.level == 3)):
            self.level = -1
                
        #if it is level 1
        if self.level == 1:
            self.check_for_collision_with_coin()
            #stop going down where there are blocks
            if (not self.stop_up((55-(50//2)-12),
                                 (55+(50//2)+12),
                                 (25+(15//2)+20),
                                 (25+(15//2)+10))):
                
                if (not self.stop_up((115-(50//2)-12),
                                     (115+(50//2)+12),
                                     (55+(15//2)+20),
                                     (55+(15//2)+10))):

                    if (not self.stop_up((175-(50//2)-12),
                                         (175+(50//2)+12),
                                         (85+(15//2)+20),
                                         (85+(15//2)+10))):
                    
                        if (not self.stop_up((235-(50//2)-12),
                                             (235+(50//2)+12),
                                             (115+(15//2)+20),
                                             (115+(15//2)+10))):
                            
                            if (not self.stop_up((295-(50//2)-12),
                                                 (295+(50//2)+12),
                                                 (145+(15//2)+20),
                                                 (145+(15//2)+10))):
                                
                                if (not self.stop_up((420-(175//2)-12),
                                                     (420+(175/2)+12),
                                                     (175+(15//2)+20),
                                                     (175+(15//2)+10))):

                                    self.stop_y = False

            #move the player
            self.move()
            
        #if it is level 2
        elif self.level == 2:
            self.check_for_collision_with_coin()
            
            if (not self.stop_up((25-(50//2)-12),
                                 (25+(50//2)+12),
                                 (175+(15//2)+20),
                                 (175+(15//2)+10))):
                
                if (not self.stop_up((200-(150//2)-12),
                                     (200+(150//2)+12),
                                     (135+(15//2)+20),
                                     (135+(15//2)+10))):

                    if (not self.stop_up((265-(20//2)-12),
                                         (265+(20//2)+12),
                                         (170+(15//2)+20),
                                         (170+(15//2)+10))):
                    
                        if (not self.stop_up((240-(20//2)-12),
                                             (240+(20//2)+12),
                                             (205+(15//2)+20),
                                             (205+(15//2)+10))):
                            
                            if (not self.stop_up((215-(20//2)-12),
                                                 (215+(20//2)+12),
                                                 (240+(15//2)+20),
                                                 (240+(15//2)+10))):
                                
                                if (not self.stop_up((190-(20//2)-12),
                                                     (190+(20//2)+12),
                                                     (275+(15//2)+20),
                                                     (275+(15//2)+10))):
                                    
                                    if (not self.stop_up((165-(20//2)-12),
                                                         (165+(20//2)+12),
                                                         (310+(15//2)+20),
                                                         (310+(15//2)+10))):

                                        if (not self.stop_up((342-(315//2)-12),
                                                             (342+(315//2)+12),
                                                             (345+(15//2)+20),
                                                             (345+(15//2)+10))):
                                            
                                            if (not self.stop_up((322-(15//2)-12),
                                                                 (322+(15//2)+12),
                                                                 (360+(30//2)+20),
                                                                 (360+(30//2)+10))):

                                                if (not self.stop_up((395-(15//2)-12),
                                                                     (395+(15//2)+12),
                                                                     (360+(30//2)+20),
                                                                     (360+(30//2)+10))):

                                                    self.stop_y = False

            #stop at blocks                                        
            self.stop_right((322-(15//2)-14),
                            (322+(15//2)+13),
                            (360+(30//2)+17),
                            (360+(30//2)-20))
            
            
            self.stop_right((395-(15//2)-14),
                            (395+(15//2)+13),
                            (360+(30//2)+17),
                            (360+(30//2)-20))
            
            self.stop_left((322-(15//2)-12),
                            (322+(15//2)+15),
                            (360+(30//2)+17),
                            (360+(30//2)-20))
            
            self.stop_left((395-(15//2)-12),
                            (395+(15//2)+15),
                            (360+(30//2)+17),
                            (360+(30//2)-20))
            
            self.move()

        #if it is level 3
        elif self.level == 3:
            if (not self.stop_up((0-(80//2)-12),
                                (0+(80//2)+12),
                                (345+(15//2)+20),
                                (345+(15//2)-20))):
                
                if (not self.stop_up((130-(6//2)-12),
                                    (130+(6//2)+12),
                                    (345+(15//2)+20),
                                    (345+(15//2)-20))):
                    
                    if (not self.stop_up((230-(6//2)-12),
                                        (230+(6//2)+12),
                                        (345+(15//2)+20),
                                        (345+(15//2)-20))):
                        
                        if (not self.stop_up((330-(6//2)-12),
                                            (330+(6//2)+12),
                                            (345+(15//2)+20),
                                            (345+(15//2)-20))):
                            
                            if (not self.stop_up((430-(6//2)-12),
                                                (430+(6//2)+12),
                                                (345+(15//2)+20),
                                                (345+(15//2)-20))):
                                
                                if (not self.stop_up((478-(90//2)-12),
                                                    (478+(90//2)+12),
                                                    (320+(15//2)+20),
                                                    (320+(15//2)-20))):

                                    self.stop_y = False

            self.move()

    #'click to start' screens only - when screen clicked, move to level 1
    def on_mouse_press(self, x, y, button, modifiers):
        if ((y < 307) and
            (y > 220) and
            (x < 365) and
            (x > 120) and
            (self.level == 0)):
            self.level += 1

        elif ((y < 337) and
            (y > 197) and
            (x < 365) and
            (x > 120) and
            (self.level == -1)):
            self.setup()
            self.level = 1 
        return

    #move when keys are pressed
    def on_key_press(self, key, modifiers):
        #arrow keys
        if key == arcade.key.UP:
            if self.stop_y:
                self.up = 0

        if key == arcade.key.LEFT:
            self.left = True
            
        if key == arcade.key.RIGHT:
            self.right = True
            
        #WASD keys
        if key == arcade.key.W:
            if self.stop_y:
                self.up = 0

        if key == arcade.key.D:
            self.right = True

        if key == arcade.key.A:
            self.left = True

    def on_key_release(self, key, modifiers):
        #arrow keys
        if key == arcade.key.LEFT:
            self.left = False
            
        if key == arcade.key.RIGHT:
            self.right = False

        #WASD keys
        if key == arcade.key.D:
            self.right = False

        if key == arcade.key.A:
            self.left = False

    #setup coins for level 2
    def setup_coins_for_level2(self):
        if self.level == 2:
            self.coin_list = arcade.SpriteList()

            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 265
            self.coin_sprite.center_y = 185
            self.coin_list.append(self.coin_sprite)
            
            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 240
            self.coin_sprite.center_y = 220
            self.coin_list.append(self.coin_sprite)

            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 215
            self.coin_sprite.center_y = 255
            self.coin_list.append(self.coin_sprite)

            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 190
            self.coin_sprite.center_y = 290
            self.coin_list.append(self.coin_sprite)

            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 165
            self.coin_sprite.center_y = 325
            self.coin_list.append(self.coin_sprite)

            self.coins_l2 = True

    def setup_coins_for_level3(self):
        if self.level == 3:
            self.coin_list = arcade.SpriteList()

            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 130
            self.coin_sprite.center_y = 362
            self.coin_list.append(self.coin_sprite)
            
            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 230
            self.coin_sprite.center_y = 362
            self.coin_list.append(self.coin_sprite)

            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 330
            self.coin_sprite.center_y = 362
            self.coin_list.append(self.coin_sprite)

            self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
            self.coin_sprite.center_x = 430
            self.coin_sprite.center_y = 362
            self.coin_list.append(self.coin_sprite)

            self.coins_l2 = False
            self.coins_l3 = True

    #setup the game
    def setup(self):
        #player
        self.player_sprite = Player(":resources:images/enemies/frog.png", 0.25)
        self.player_list = arcade.SpriteList()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        #level
        self.level = 0

        #enemy 1
        self.enemy1_right = False
        self.enemy_sprite1 = Enemy1(':resources:images/enemies/mouse.png', 0.25)
        self.enemy_list1 = arcade.SpriteList()
        self.enemy_sprite1.center_x = 149
        self.enemy_sprite1.center_y = 162
        self.enemy_list1.append(self.enemy_sprite1)
        self.hit_enemy = False

        #enemy 2
        self.enemy1_up = False
        self.enemy_sprite2 = Enemy2(':resources:images/enemies/bee.png', 0.15)
        self.enemy_list2 = arcade.SpriteList()
        self.enemy_sprite2.center_x = 180
        self.enemy_sprite2.center_y = 345
        self.enemy_list2.append(self.enemy_sprite2)
        
        self.enemy_sprite2b = Enemy2(':resources:images/enemies/bee.png', 0.15)
        self.enemy_sprite2b.center_x = 280
        self.enemy_sprite2b.center_y = 345
        self.enemy_list2.append(self.enemy_sprite2b)

        self.enemy_sprite2c = Enemy2(':resources:images/enemies/bee.png', 0.15)
        self.enemy_sprite2c.center_x = 380
        self.enemy_sprite2c.center_y = 345
        self.enemy_list2.append(self.enemy_sprite2c)

        self.enemy_sprite2d = Enemy2(':resources:images/enemies/bee.png', 0.15)
        self.enemy_sprite2d.center_x = 80
        self.enemy_sprite2d.center_y = 345
        self.enemy_list2.append(self.enemy_sprite2d)

        #coins (for level 1)
        self.coins_collected = 0
        self.coin_list = arcade.SpriteList()
        
        self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
        self.coin_sprite.center_x = 115
        self.coin_sprite.center_y = 70
        self.coin_list.append(self.coin_sprite)

        self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
        self.coin_sprite.center_x = 175
        self.coin_sprite.center_y = 100
        self.coin_list.append(self.coin_sprite)

        self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
        self.coin_sprite.center_x = 235
        self.coin_sprite.center_y = 130
        self.coin_list.append(self.coin_sprite)

        self.coin_sprite = Coin(':resources:images/items/coinGold.png', 0.2)
        self.coin_sprite.center_x = 295
        self.coin_sprite.center_y = 160
        self.coin_list.append(self.coin_sprite)

    #move enemies
    def move_enemy1(self):
        if self.level == 2:
            if ((self.enemy_sprite1.center_x < 250) and
                (self.enemy_sprite1.center_x > 150)):
                if self.enemy1_right:
                    self.enemy_sprite1.center_x += 1
                else:
                    self.enemy_sprite1.center_x -=1

            else:       
                self.change_enemy_direction_to_move()

    def move_enemy2(self):
        if self.level == 3:
            if ((self.enemy_sprite2.center_y < 385) and
                (self.enemy_sprite2.center_y > 305)):
                for enemy in self.enemy_list2:
                    if self.enemy2_down:
                        enemy.center_y -= 1
                    else:
                        enemy.center_y += 1
                        
            else:
                self.change_enemy_direction_to_move2()

    #change enemies' direction
    def change_enemy_direction_to_move(self):
        if self.enemy1_right:
            self.enemy1_right = False
            self.enemy_sprite1.center_x -= 2
        else:
            self.enemy1_right = True
            self.enemy_sprite1.center_x += 2

    def change_enemy_direction_to_move2(self):
        if self.enemy2_down:
            self.enemy2_down = False
            for enemy in self.enemy_list2:
                enemy.center_y += 2
        else:
            self.enemy2_down = True
            for enemy in self.enemy_list2:
                enemy.center_y -= 2

def main():
    window = Game()
    window.setup()
    arcade.run()  

main()

