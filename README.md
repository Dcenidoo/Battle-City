# Welcome to Battle City! (Phase 3)
Submitted By: Ceñido, Dominic (2023-06831) & Mercado, Ervin (2023-11899)

The goal of this game is to shoot and eliminate all opposing tanks in a given stage.
Enemy tanks will spawn periodically at their specified spawn points with varying tank type.
Shoot bullets to eliminate tanks.
Use your bullets wisely as you can only have at most 1 active bullet.
Eliminate all tanks in all stages, you win.
Be careful not to eliminate yourself.

You will be given two lives for the entirety of the game.
Remaining lives will be visible at the bottom of the screen.
Use up the two lives and it is game over.

A power-up will also spawn in a given stage only if you have killed at least two enemy tanks.
The power-up can only be used if you have used up a life.

Stage 1 will have three enemy tanks.
Stage 2 will have five enemy tanks.

GLHF!

## Controls

Arrow_UP = move up

Arrow_DOWN = move down

Arrow_LEFT = move left

Arrow_RIGHT = move right

SPACE = shoot bullets


C = adds another life (cheat code)(usable only if you have lost a life)

B = respawn

R = reset game

Q = quit game

X = continue to next stage (only if stage 1 has been completed)


## Tiles

Empty = walkable

Stone = non_walkable; breaks bullets

Brick = non_walkable; breaks bullets and turns into Cracked_Brick

Cracked_Brick = non_walkable; breaks bullets and turns into Empty

Mirror = changes bullet trajectory depending on position of tank and mirror

Water = non_walkable; allows bullet to pass through

Forest = walkalbe; makes tank less visible

Home = non_walkable; automatic game over if destroyed

Power_Up = walkable(only if player has 1 health); grants an additonal health

## Enemy Tanks

Enemy Tanks move and shoot bullets at random intervals. Enemy tanks cannot move to spaces currently occupied by the player tank or a non_walkable block. Two types of enemy tanks are present in this game.

Enemy Tank Type 1 - Bullets shot by this tank move at the same speed as bullets shot by the player tank.

Enemy Tank Type 2 - Bullets shot by this tank move two times faster than the bullets shot by the player tank. Bullets shot by this tank are noticeably bigger.

For easier identification, each enemy tank type has its own distinct design.

## Contributions

Ceñido, Dominic = tile_drawing, music, player_tank_design, enemy_tank_designs, player_tank_movement, stage_file, stage_change, win_conditions, display_win_and_game_over, block_logic, bullet_to_bullet_collision_logic, bullet_logic, player_and_enemy_tank_logic
                

Mercado, Ervin = tile_drawing, player_lives_implementation, power_up_implementation, cheat_code_implementation, stage_file, player_respawn, bullet_logic, block_logic, bullet_to_bullet_collision_logic, player_and_enemy_tank_logic


## Video Demo

Link = https://drive.google.com/file/d/1QceLtQVrFPEATZcXikxM2rchfMsk31TX/view?usp=sharing

## Files

Game Code = 'MP1_phase3.py'

Resources = 'mygame.pyxres'

Stage 1 = 'stage1.py'

Stage 2 = 'stage2.py'


[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/-nd8uuv_)
