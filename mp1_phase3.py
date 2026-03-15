from dataclasses import dataclass
import pyxel as py
import random
import stage1
import stage2
from stage1 import player_tank, enemy_tank1, enemy_tank2, home_spawn_coords, enemy_spawn_coords, stone_coords, brick_coords, mirror_coords, water_coords, cracked_brick_coords, forest_coords, house_coords, heart_coords, power_up_coords, game_state as stage1_game_state
from stage2 import game_state as stage2_game_state

class BattleCity:
    def __init__(self):
        #initializing game
        py.init(256, 224, title='Battle City')
        py.load('mygame.pyxres')
        self.game_state = 'stage1'
        self.game_reset()
        self.player_health = 2  
        self.cheat_code_activated = False
        py.run(self.update, self.draw)

    def respawn(self):
        self.x, self.y = player_tank
        self.orientation = "up"
        self.player_alive = True

    def game_reset(self):
        self.i = 0
        self.player_bullets = []
        self.enemy1_bullets = []
        self.enemy2_bullets = []

        self.tank_already_spawned =[]
        self.dead_tank = 0
        self.bullet_hold = 0

        #player tank initialization
        self.x, self.y = player_tank
        self.orientation = "up"
        self.player_health = 2
        self.player_alive = True

        #enemy tank initialization
        self.enemy_tank1 = enemy_tank1[::]
        self.enemy_tank2 = enemy_tank2[::]

        #spawn point initialization
        self.home_spawn_coords = home_spawn_coords[::]
        self.enemy_spawn_coords = enemy_spawn_coords[::]

        #block initialization
        self.stone_coords = stone_coords[::]        
        self.brick_coords = brick_coords[::]
        self.mirror_coords = mirror_coords[::]
        self.water_coords = water_coords[::]
        self.cracked_brick_coords = cracked_brick_coords[::]
        self.forest_coords = forest_coords[::]
        self.house_coords = house_coords[::]
        self.life_coords = heart_coords[::]
        self.power_up_coords = power_up_coords[::]

        #movement initialization
        self.last_move_time = 0
        self.last_move_enemy1_time = 0
        self.last_move_enemy2_time = 0

        #enemy spawning initialization
        self.last_spawn_time =  0 #time it takes to spawn an enemy
        self.spawn_delay = 50 #time it takes to spawn next enemy

        #movement delay for bullet speed bias
        self.move_delay_player = 10
        self.move_delay_enemy1 = 25  #delay in frames between moves
        self.move_delay_enemy2 = 25  #delay in frames between moves

        #game result initialization
        if self.game_state == 'stage1':
            self.update_stage(stage1, stage1_game_state)
        elif self.game_state == 'stage2':
            self.update_stage(stage2, stage2_game_state)
        self.game_over = False
        self.stage_cleared = False
        self.win = False
        self.cheat_code_activated = False

    def change_stage(self):
        self.i = 0
        self.player_bullets = []
        self.enemy1_bullets = []
        self.enemy2_bullets = []

        self.tank_already_spawned =[]
        self.dead_tank = 0
        self.bullet_hold = 0

        #player tank initialization
        self.x, self.y = player_tank
        self.orientation = "up"
        self.player_health = self.player_health
        self.player_alive = True

        #enemy tank initialization
        self.enemy_tank1 = enemy_tank1[::]
        self.enemy_tank2 = enemy_tank2[::]

        #spawn point initialization
        self.home_spawn_coords = home_spawn_coords[::]
        self.enemy_spawn_coords = enemy_spawn_coords[::]

        #block initialization
        self.stone_coords = stone_coords[::]        
        self.brick_coords = brick_coords[::]
        self.mirror_coords = mirror_coords[::]
        self.water_coords = water_coords[::]
        self.cracked_brick_coords = cracked_brick_coords[::]
        self.forest_coords = forest_coords[::]
        self.house_coords = house_coords[::]
        self.life_coords = heart_coords[::]
        self.power_up_coords = power_up_coords[::]

        #movement initialization
        self.last_move_time = 0
        self.last_move_enemy1_time = 0
        self.last_move_enemy2_time = 0

        #enemy spawning initialization
        self.last_spawn_time =  0 #time it takes to spawn an enemy
        self.spawn_delay = 50 #time it takes to spawn next enemy

        #movement delay for bullet speed bias
        self.move_delay_player = 10
        self.move_delay_enemy1 = 25  #delay in frames between moves
        self.move_delay_enemy2 = 25  #delay in frames between moves

        #game result initialization
        if self.game_state == 'stage1':
            self.update_stage(stage1, stage1_game_state)
        elif self.game_state == 'stage2':
            self.update_stage(stage2, stage2_game_state)
        self.game_over = False
        self.stage_cleared = False
        self.win = False
    
    def next_stage(self):
        self.update_stage(stage2, stage2_game_state)
        self.change_stage()


    def stage_reset(self):
        self.game_reset()

    def update_stage(self, module, module_game_state):
        global player_tank, enemy_tank1, enemy_tank2, home_spawn_coords, enemy_spawn_coords
        global stone_coords, brick_coords, mirror_coords, water_coords, cracked_brick_coords, forest_coords, house_coords, heart_coords, power_up_coords
        
        player_tank = module.player_tank
        enemy_tank1 = module.enemy_tank1
        enemy_tank2 = module.enemy_tank2
        home_spawn_coords = module.home_spawn_coords
        enemy_spawn_coords = module.enemy_spawn_coords
        stone_coords = module.stone_coords
        brick_coords = module.brick_coords
        mirror_coords = module.mirror_coords
        water_coords = module.water_coords
        cracked_brick_coords = module.cracked_brick_coords
        forest_coords = module.forest_coords
        house_coords = module.house_coords
        heart_coords = module.heart_coords
        power_up_coords = module.power_up_coords
        self.game_state = module_game_state

    #game result checking
    def no_more_enemies(self):
        current_time = py.frame_count
        if current_time > (self.spawn_delay * 2 * len(self.enemy_spawn_coords)):
            if len(self.tank_already_spawned) == len(self.enemy_spawn_coords):
                if not self.enemy_tank1 and not self.enemy_tank2:
                    if self.game_state == 'stage1':
                        self.stage_cleared = True
                        if py.btnp(py.KEY_X):
                            self.next_stage()
                    if self.game_state == 'stage2':
                        self.win = True
    
    def already_spawned(self,x,y):
        return (x,y) in self.tank_already_spawned

    #block identification logic
    def mirror_direction(self, x: int, y: int):
        for x_mirror, y_mirror, direction in self.mirror_coords:
            if (x, y) == (x_mirror, y_mirror):
                return direction

    def is_there_brick(self, x, y):
        return (x, y) in self.brick_coords

    def is_there_stone(self, x: int, y: int):
        return (x, y) in self.stone_coords
    
    def is_there_mirror(self, x: int, y: int) -> bool:
        for mirror_x, mirror_y, _ in self.mirror_coords:
            if (x, y) == (mirror_x, mirror_y):
                return True
        return False

    def is_there_water(self, x, y):
        return (x, y) in self.water_coords
    
    def is_there_cracked_brick(self, x,y):
        return (x, y) in self.cracked_brick_coords
    
    def is_there_house(self, x, y):
        return (x, y) in self.house_coords

    def is_there_tank(self, x , y):
        return any((tank_x, tank_y) == (x, y) for tank_x, tank_y, _ in self.enemy_tank1) or \
            any((tank_x, tank_y) == (x, y) for tank_x, tank_y, _ in self.enemy_tank2) or \
            (x, y) == (self.x, self.y) 
    
    def is_there_player_tank(self, x, y):
        return (self.x, self.y) == (x, y)
    
    def is_there_powerup(self,x,y):
        return

    def is_there_block(self, cell_x: int, cell_y: int) -> bool:
        return self.is_there_brick(cell_x, cell_y) or self.is_there_stone(cell_x, cell_y) or self.is_there_mirror(cell_x, cell_y) or self.is_there_tank(cell_x,cell_y) or self.is_there_water(cell_x, cell_y) or self.is_there_cracked_brick(cell_x,cell_y) or self.is_there_house(cell_x,cell_y) or self.is_there_player_tank(cell_x,cell_y)

    #bullet collision with player logic
    def handle_player_bullet_collisions(self):

        for bullet in self.player_bullets:
            bullet_cell_x = (bullet.x // 16) * 16
            bullet_cell_y = (bullet.y // 16) * 16

            if self.is_there_brick(bullet_cell_x, bullet_cell_y):
                self.cracked_brick_coords.append((bullet_cell_x, bullet_cell_y))
                py.stop()
                py.playm(1, loop=False)
                self.brick_coords.remove((bullet_cell_x, bullet_cell_y))
                self.player_bullets.remove(bullet)

            elif self.is_there_cracked_brick(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.cracked_brick_coords.remove((bullet_cell_x, bullet_cell_y))
                self.player_bullets.remove(bullet)

            elif self.is_there_stone(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.player_bullets.remove(bullet)

            elif self.is_there_mirror(bullet_cell_x, bullet_cell_y):
                bullet_current_direction = self.mirror_direction(bullet_cell_x, bullet_cell_y)
                bullet.mirror(bullet_current_direction)

            elif self.is_there_house(bullet_cell_x, bullet_cell_y):
                self.house_coords.remove((bullet_cell_x, bullet_cell_y))
                self.player_bullets.remove(bullet)
                self.game_over = True

            elif (bullet_cell_x, bullet_cell_y) in [(bullet.x, bullet.y) for bullet in self.enemy1_bullets]:
                py.playm(1, loop=False)
                self.player_bullets.remove(bullet)

            elif (bullet_cell_x, bullet_cell_y) in [(bullet.x, bullet.y) for bullet in self.enemy2_bullets]:
                py.playm(1, loop=False)
                self.player_bullets.remove(bullet)

            elif self.is_there_tank(bullet_cell_x, bullet_cell_y):
                for tank in self.enemy_tank1:
                    if (tank[0], tank[1]) == (bullet_cell_x, bullet_cell_y):
                        self.enemy_tank1.remove(tank)
                        py.playm(2, loop=False)
                        self.dead_tank += 1
                        self.player_bullets.remove(bullet)
                        break
                for tank in self.enemy_tank2:
                    if (tank[0], tank[1]) == (bullet_cell_x, bullet_cell_y):
                        self.enemy_tank2.remove(tank)
                        py.playm(2, loop=False)
                        self.dead_tank += 1
                        self.player_bullets.remove(bullet)
                        break

    #general bullet collision logic
    def handle_enemy1_bullet_collisions(self):
        for bullet in self.enemy1_bullets:
            bullet_cell_x = (bullet.x // 16) * 16
            bullet_cell_y = (bullet.y // 16) * 16

            if self.is_there_brick(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.cracked_brick_coords.append((bullet_cell_x, bullet_cell_y))
                self.brick_coords.remove((bullet_cell_x, bullet_cell_y))
                self.enemy1_bullets.remove(bullet)

            elif self.is_there_cracked_brick(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.cracked_brick_coords.remove((bullet_cell_x, bullet_cell_y))
                self.enemy1_bullets.remove(bullet)
            
            elif self.is_there_stone(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.enemy1_bullets.remove(bullet)

            elif self.is_there_mirror(bullet_cell_x, bullet_cell_y):
                bullet_current_direction = self.mirror_direction(bullet_cell_x, bullet_cell_y)
                bullet.mirror(bullet_current_direction)

            elif self.is_there_house(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.house_coords.remove((bullet_cell_x, bullet_cell_y))
                self.enemy1_bullets.remove(bullet)
                self.game_over = True

            elif (bullet_cell_x, bullet_cell_y) in [(bullet.x, bullet.y) for bullet in self.player_bullets]:
                py.playm(1, loop=False)
                self.enemy1_bullets.remove(bullet)

            elif (bullet_cell_x, bullet_cell_y) == (self.x, self.y):
                self.enemy1_bullets.remove(bullet)
                if self.player_alive:
                    self.player_health -= 1
                    py.playm(3, loop=False)
                    self.player_alive = False
                    
                    if self.player_health == 0:
                            self.game_over = True

    def handle_enemy2_bullet_collisions(self):
        for bullet in self.enemy2_bullets:
            bullet_cell_x = (bullet.x // 16) * 16
            bullet_cell_y = (bullet.y // 16) * 16

            if self.is_there_brick(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.cracked_brick_coords.append((bullet_cell_x, bullet_cell_y))
                self.brick_coords.remove((bullet_cell_x, bullet_cell_y))
                self.enemy2_bullets.remove(bullet)

            elif self.is_there_cracked_brick(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.cracked_brick_coords.remove((bullet_cell_x, bullet_cell_y))
                self.enemy2_bullets.remove(bullet)
            
            elif self.is_there_stone(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.enemy2_bullets.remove(bullet)

            elif self.is_there_mirror(bullet_cell_x, bullet_cell_y):
                bullet_current_direction = self.mirror_direction(bullet_cell_x, bullet_cell_y)
                bullet.mirror(bullet_current_direction)

            elif self.is_there_house(bullet_cell_x, bullet_cell_y):
                py.stop()
                py.playm(1, loop=False)
                self.house_coords.remove((bullet_cell_x, bullet_cell_y))
                self.enemy2_bullets.remove(bullet)
                self.game_over = True

            elif (bullet_cell_x, bullet_cell_y) in [(bullet.x, bullet.y) for bullet in self.player_bullets]:
                py.playm(1, loop=False)
                self.enemy2_bullets.remove(bullet)

            elif (bullet_cell_x, bullet_cell_y) == (self.x, self.y):
                self.enemy2_bullets.remove(bullet)
                if self.player_alive:
                    self.player_health -= 1
                    py.playm(3, loop=False)
                    self.player_alive = False
                    
                    if self.player_health == 0:
                            self.game_over = True


    def handle_bullet_to_bullet_collison1(self):
        for player_bullet in self.player_bullets:
            for enemy1_bullet in self.enemy1_bullets:
                if abs(player_bullet.x - enemy1_bullet.x) < 3 and abs(player_bullet.y - enemy1_bullet.y) < 3:
                    self.player_bullets.remove(player_bullet)
                    self.enemy1_bullets.remove(enemy1_bullet)
                    py.playm(1, loop=False)

    def handle_bullet_to_bullet_collison2(self):
        for player_bullet in self.player_bullets:
            for enemy2_bullet in self.enemy2_bullets:
                if abs(player_bullet.x - enemy2_bullet.x) < 3 and abs(player_bullet.y - enemy2_bullet.y) < 3:
                    self.player_bullets.remove(player_bullet)
                    self.enemy2_bullets.remove(enemy2_bullet)
                    py.playm(1, loop=False)


                            
    def check_player_collision(self):
        for bullet in self.player_bullets:
            if abs(self.x - bullet.x) < 8 and abs(self.y - bullet.y) < 8:  #checks if player's bullet collided with player tank
                self.player_bullets.remove(bullet)
                if self.player_alive is True:
                    py.playm(3, loop=False)
                    self.player_alive = False
                    self.player_health -=  1
                    if self.player_health == 0:
                        self.game_over = True

    def fire_enemy1_bullet(self, x, y, direction):
        if random.randint(1,100) <= 3:
            self.enemy1_bullets.append(EnemyBullet1(x + 8, y + 8, direction))
            py.playm(0, loop=False)

    def fire_enemy2_bullet(self, x, y, direction):
        if random.randint(1,100) <= 3:
            self.enemy2_bullets.append(EnemyBullet2(x + 8, y + 8, direction))
            py.playm(0, loop=False)
            


    #enemy tank spawning logic
    def spawn_enemy_tank(self):
        if len(self.tank_already_spawned) < len(self.enemy_spawn_coords):  
            spawn_x, spawn_y = random.choice(self.enemy_spawn_coords)
            if not self.is_there_block(spawn_x, spawn_y) and not self.already_spawned(spawn_x, spawn_y):
                self.tank_already_spawned.append((spawn_x, spawn_y))
                choices = [1, 2]
                tank_choice = random.choice(choices)
                if tank_choice == 1:
                    self.enemy_tank1.append((spawn_x, spawn_y, random.choice(['up', 'down', 'left', 'right'])))
                else:
                    self.enemy_tank2.append((spawn_x, spawn_y, random.choice(['up', 'down', 'left', 'right'])))

    def game_state(self):
        pass 

    def check_input(self):

        if py.btnp(py.KEY_C): # cheat code (adds extra life)
            if not self.cheat_code_activated and self.player_health < 2:
                self.cheat_code_activated = True
                py.stop()
                py.playm(4, loop=False)
                self.player_health += 1
                pass #add life

        if self.game_state == 'running_stage1' or 'running_stage2':
            pass
    
    def check_power_up(self,x,y):
        if (x,y) in self.power_up_coords and self.player_health < 2:
            if self.dead_tank >= 2:
                py.playm(4, loop=False)
                self.player_health += 1
                self.power_up_coords.remove((x,y))

    def update(self):
        current_time = py.frame_count

        if py.btnp(py.KEY_Q): #quits game
            py.quit()

        if py.btn(py.KEY_R): #restarts game
            self.game_state = 'stage1'
            self.stage_reset()

        #updating game result (game over or stage cleared)
        if self.game_over:
            return
        if self.stage_cleared:
            if py.btnp(py.KEY_X):
                self.next_stage()
            return
        if self.win:
            return
        
        if not self.player_alive: #respawn only when player tank is dead
            if py.btn(py.KEY_B):
                 
                self.respawn()

        if self.player_health == 2:
            for cell_x, cell_y in self.life_coords:
                py.blt(cell_x, cell_y, 0, 48, 56, 16, 16, 0)    
        elif self.player_health == 1:
            py.blt(112, 208, 0, 48, 40, 16, 16, 0)    
            py.blt(128, 208, 0, 48, 56, 16, 16, 0)    
        else:
            pass

        # Movement of player
        if self.player_alive:
            if current_time - self.last_move_time > self.move_delay_player:
                if py.btn(py.KEY_UP):
                    self.orientation = "up"
                    if self.y > 0 and not self.is_there_block(self.x, self.y - 16):
                        self.y -= 16
                        self.check_power_up(self.x, self.y)
                        self.last_move_time = current_time
                elif py.btn(py.KEY_DOWN):
                    self.orientation = "down"
                    if self.y < py.height - 16 and not self.is_there_block(self.x, self.y + 16):
                        self.y += 16
                        self.check_power_up(self.x, self.y)
                        self.last_move_time = current_time
                elif py.btn(py.KEY_RIGHT):
                    self.orientation = "right"
                    if self.x < py.width - 16 and not self.is_there_block(self.x + 16, self.y):
                        self.x += 16
                        self.check_power_up(self.x, self.y)
                        self.last_move_time = current_time
                elif py.btn(py.KEY_LEFT):
                    self.orientation = "left"
                    if self.x > 0 and not self.is_there_block(self.x - 16, self.y):
                        self.x -= 16
                        self.check_power_up(self.x, self.y)
                        self.last_move_time = current_time

        #movement of enemy tank 1 in random
        if current_time - self.last_move_enemy1_time > self.move_delay_enemy1: #delay for movement of enemy
                new_enemy_tanks1 = []

                for enemy_cell_x, enemy_cell_y, enemy_direction in self.enemy_tank1:
                    free_cell = False
                    directions = ['up', 'down', 'left', 'right']
                    new_direction = random.choice(directions)

                    while not free_cell and directions:
                        new_direction = random.choice(directions)
                        directions.remove(new_direction)
                    #calculating new position based on new direction
                        if new_direction == 'up':
                            if enemy_cell_y > 0 and not self.is_there_block(enemy_cell_x, enemy_cell_y - 16):
                                new_enemy_tanks1.append((enemy_cell_x, enemy_cell_y - 16, new_direction))
                                free_cell = True
                        elif new_direction == 'down':
                            if enemy_cell_y < py.height - 16 and not self.is_there_block(enemy_cell_x, enemy_cell_y + 16):
                                new_enemy_tanks1.append((enemy_cell_x, enemy_cell_y + 16, new_direction))
                                free_cell = True
                        elif new_direction == 'left':
                            if enemy_cell_x > 0 and not self.is_there_block(enemy_cell_x - 16, enemy_cell_y):
                                new_enemy_tanks1.append((enemy_cell_x - 16, enemy_cell_y, new_direction))
                                free_cell = True
                        elif new_direction == 'right':
                            if enemy_cell_x < py.width - 16 and not self.is_there_block(enemy_cell_x + 16, enemy_cell_y):
                                new_enemy_tanks1.append((enemy_cell_x + 16, enemy_cell_y, new_direction))
                                free_cell = True

                    if not free_cell:
                        new_enemy_tanks1.append((enemy_cell_x, enemy_cell_y, enemy_direction))

                #updating enemy_tanks with the new positions
                self.enemy_tank1 = new_enemy_tanks1

                self.last_move_enemy1_time = current_time      

        #movement of enemy tank 2 in random
        if current_time - self.last_move_enemy2_time > self.move_delay_enemy2: #delay for movement of enemy
                new_enemy_tanks2 = []

                for enemy_cell_x, enemy_cell_y, enemy_direction in self.enemy_tank2:
                    free_cell = False
                    directions = ['up', 'down', 'left', 'right']
                    new_direction = random.choice(directions)

                    while not free_cell and directions:
                        new_direction = random.choice(directions)
                        directions.remove(new_direction)
                    #calculating new position based on new direction
                        if new_direction == 'up':
                            if enemy_cell_y > 0 and not self.is_there_block(enemy_cell_x, enemy_cell_y - 16):
                                new_enemy_tanks2.append((enemy_cell_x, enemy_cell_y - 16, new_direction))
                                free_cell = True
                        elif new_direction == 'down':
                            if enemy_cell_y < py.height - 16 and not self.is_there_block(enemy_cell_x, enemy_cell_y + 16):
                                new_enemy_tanks2.append((enemy_cell_x, enemy_cell_y + 16, new_direction))
                                free_cell = True
                        elif new_direction == 'left':
                            if enemy_cell_x > 0 and not self.is_there_block(enemy_cell_x - 16, enemy_cell_y):
                                new_enemy_tanks2.append((enemy_cell_x - 16, enemy_cell_y, new_direction))
                                free_cell = True
                        elif new_direction == 'right':
                            if enemy_cell_x < py.width - 16 and not self.is_there_block(enemy_cell_x + 16, enemy_cell_y):
                                new_enemy_tanks2.append((enemy_cell_x + 16, enemy_cell_y, new_direction))
                                free_cell = True

                    if not free_cell:
                        new_enemy_tanks2.append((enemy_cell_x, enemy_cell_y, enemy_direction))

                #updating enemy_tanks with the new positions
                self.enemy_tank2 = new_enemy_tanks2

                self.last_move_enemy2_time = current_time      


        #player bullets
        if self.player_alive:       
            if py.btn(py.KEY_SPACE):
                if not self.player_bullets: 
                    if self.bullet_hold == 0:
                        self.player_bullets.append(Bullet(self.x + 8, self.y + 8, self.orientation))
                        py.playm(0, loop=False)
                        self.bullet_hold = 15

        #game control initialization

        #enemy bullet logic
        for enemy_tank in self.enemy_tank1:
            if not self.enemy1_bullets:
                self.fire_enemy1_bullet(*enemy_tank)

        for enemy_tank in self.enemy_tank2:
            if not self.enemy2_bullets:
                self.fire_enemy2_bullet(*enemy_tank)


        #delay of bullets to support firing when holding down spacebar
        if self.bullet_hold > 0:
            self.bullet_hold -= 1

        for bullet in self.player_bullets:
            bullet.update()

        for bullet in self.enemy1_bullets:
            bullet.update()

        for bullet in self.enemy2_bullets:
            bullet.update()

        self.player_bullets = [bullet for bullet in self.player_bullets if 0 <= bullet.x < py.width and 0 <= bullet.y < py.height]

        self.enemy1_bullets = [bullet for bullet in self.enemy1_bullets if 0 <= bullet.x < py.width and 0 <= bullet.y < py.height]
        self.enemy2_bullets = [bullet for bullet in self.enemy2_bullets if 0 <= bullet.x < py.width and 0 <= bullet.y < py.height]

        
        # check for collisions of bullets with other entities
        self.handle_player_bullet_collisions()

        self.handle_enemy1_bullet_collisions()
        self.handle_enemy2_bullet_collisions()


        self.handle_bullet_to_bullet_collison1()
        self.handle_bullet_to_bullet_collison2()


        # for when bullet hits player
        self.check_player_collision()

        #checks for input during game
        self.check_input()

        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_enemy_tank()
            self.last_spawn_time = current_time

        if py.frame_count > 300:
            self.no_more_enemies()

        self.player_bullets = [bullet for bullet in self.player_bullets if 0 <= bullet.x < py.width and 0 <= bullet.y < py.height]

    def draw(self):

        py.cls(0)

        #draw blocks
        for cell_x, cell_y in self.stone_coords:
            py.blt(cell_x, cell_y, 0, 0, 56, 16, 16, 0)
        for cell_x, cell_y in self.brick_coords:
            py.blt(cell_x, cell_y, 0, 0, 72, 16, 16, 0)
        for cell_x, cell_y in self.water_coords:
            py.blt(cell_x, cell_y, 0, 0, 40, 16, 16, 0)    
        for cell_x, cell_y in self.cracked_brick_coords:
            py.blt(cell_x, cell_y, 0, 16, 72, 16, 16, 0)    
        for cell_x, cell_y, direction in self.mirror_coords:
            if direction == 'north-east': 
                py.blt(cell_x, cell_y, 0, 0, 88, 16, 16, 0)
            elif direction == 'north-west': 
                py.blt(cell_x, cell_y, 0, 16, 88, 16, 16, 0)
        for cell_x, cell_y in self.house_coords:
                py.blt(cell_x, cell_y, 0, 32, 104, 16, 16, 0)
        if self.dead_tank >= 2:
            for cell_x, cell_y in self.power_up_coords:
                py.blt(cell_x, cell_y, 0, 48, 72, 16, 16, 0)

        # draws and updates health on screen
        if self.player_health == 2:
            for cell_x, cell_y in self.life_coords:
                py.blt(cell_x, cell_y, 0, 48, 40, 16, 16, 0)    
        elif self.player_health == 1:
            py.blt(112, 208, 0, 48, 40, 16, 16, 0)    
            py.blt(128, 208, 0, 48, 56, 16, 16, 0)    

        #draws home and enemy spawn
        for cell_x, cell_y in self.home_spawn_coords:
            py.blt(cell_x, cell_y, 0, 0, 104, 16, 16, 0)

        for cell_x, cell_y in self.enemy_spawn_coords:
            py.blt(cell_x, cell_y, 0, 16, 104, 16, 16, 0)

        #draw enemy tank 1
        for enemy_cell_x, enemy_cell_y, enemy_direction in self.enemy_tank1:
                if enemy_direction == "up":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 0, 16, 16, 16, 0)
                elif enemy_direction == "down":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 16, 16, 16, 16, 0)
                elif enemy_direction == "left":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 32, 16, 16, 16, 0)
                elif enemy_direction == "right":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 48, 16, 16, 16, 0)

        #draw enemy tank 2
        for enemy_cell_x, enemy_cell_y, enemy_direction in self.enemy_tank2:
                if enemy_direction == "up":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 32, 40, 16, 16, 0)
                elif enemy_direction == "down":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 32, 56, 16, 16, 0)
                elif enemy_direction == "left":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 32, 72, 16, 16, 0)
                elif enemy_direction == "right":
                    py.blt(enemy_cell_x, enemy_cell_y, 0, 32, 88, 16, 16, 0)

        #game result animations
        if self.cheat_code_activated is True:
            py.text(70, 186, "Cheat Code Has Been Activated!", py.COLOR_WHITE)

        if not self.player_alive:
            py.text(90, 176, "Press B to Respawn", py.COLOR_WHITE)

        if self.game_over:
            py.cls(0)
            py.text(110, 100, "Game Over", 8)
            py.text(60, 120, "Press R to Restart or Press Q to Quit", 8)
            return
        
        if self.stage_cleared:
            py.cls(0)
            py.text(100, 100, "Stage Cleared!", 3)
            py.text(90, 120, "Press X to continue", 3)
            return
        
        if self.win:
            py.cls(0)
            py.text(110, 100, "You Win!", 3)
            py.text(50, 120, "Press R to Play Again or Press Q to Quit", 3)
            return

        #player orientation drawing
        if self.orientation == "up":
            py.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)
        elif self.orientation == "down":
            py.blt(self.x, self.y, 0, 16, 0, 16, 16, 0)
        elif self.orientation == "left":
            py.blt(self.x, self.y, 0, 32, 0, 16, 16, 0)
        elif self.orientation == "right":
            py.blt(self.x, self.y, 0, 48, 0, 16, 16, 0)

        #bullet drawing
        for bullet in self.player_bullets:
            bullet.draw()

        for bullet in self.enemy1_bullets:
            bullet.draw()

        for bullet in self.enemy2_bullets:
            bullet.draw()


        #drawing forest at the end of the draw function to ensure it is on top of all sprites
        for cell_x, cell_y in self.forest_coords:
                py.blt(cell_x, cell_y, 0, 16, 56, 16, 16, 0)

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    #bullet movement logic
    def update(self):
        if self.direction == "up":
            self.y -= 2
        elif self.direction == "down":
            self.y += 2
        elif self.direction == "right":
            self.x += 2
        elif self.direction == "left":
            self.x -= 2

    #bullet direction change logic
    def mirror(self, direction: str):
        if direction == 'north-east':
            if self.direction == 'up':
                self.direction = 'right'
            elif self.direction == 'right':
                self.direction = 'up'
            elif self.direction == 'down':
                self.direction = 'left'
            elif self.direction == 'left':
                self.direction = 'down'
        elif direction == 'north-west':  
            if self.direction == 'up':
                self.direction = 'left'
            elif self.direction == 'right':
                self.direction = 'down'
            elif self.direction == 'down':
                self.direction = 'right'
            elif self.direction == 'left':
                self.direction = 'up'
    def draw(self):
        py.rect(self.x, self.y, 3, 3, 6)

#enemy bullet logic
class EnemyBullet1:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.y -= 2
        elif self.direction == "down":
            self.y += 2
        elif self.direction == "right":
            self.x += 2
        elif self.direction == "left":
            self.x -= 2

    #enemy bullet direction change logic
    def mirror(self, direction: str):
        if direction == 'north-east':
            if self.direction == 'up':
                self.direction = 'right'
            elif self.direction == 'right':
                self.direction = 'up'
            elif self.direction == 'down':
                self.direction = 'left'
            elif self.direction == 'left':
                self.direction = 'down'
        elif direction == 'north-west':  
            if self.direction == 'up':
                self.direction = 'left'
            elif self.direction == 'right':
                self.direction = 'down'
            elif self.direction == 'down':
                self.direction = 'right'
            elif self.direction == 'left':
                self.direction = 'up'

    def draw(self):
        py.rect(self.x, self.y, 3, 3, 14)

class EnemyBullet2:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def update(self):
        if self.direction == "up":
            self.y -= 4
        elif self.direction == "down":
            self.y += 4
        elif self.direction == "right":
            self.x += 4
        elif self.direction == "left":
            self.x -= 4

    #enemy bullet direction change logic
    def mirror(self, direction: str):
        if direction == 'north-east':
            if self.direction == 'up':
                self.direction = 'right'
            elif self.direction == 'right':
                self.direction = 'up'
            elif self.direction == 'down':
                self.direction = 'left'
            elif self.direction == 'left':
                self.direction = 'down'
        elif direction == 'north-west':  
            if self.direction == 'up':
                self.direction = 'left'
            elif self.direction == 'right':
                self.direction = 'down'
            elif self.direction == 'down':
                self.direction = 'right'
            elif self.direction == 'left':
                self.direction = 'up'

    def draw(self):
        py.blt(self.x, self.y, 0, 48, 88, 16, 16, 0)


BattleCity()
