#Name
#5/12/23
#Governor's Academy
#Honors Engineering
#The following codes for a game that is similar to the pong game. 

# Imports go at the top
from microbit import *
import time as t
import random

#paddle vars
paddle_column = [0,1]
paddle_row = 4
display.set_pixel(paddle_column[0], paddle_row, 9)
display.set_pixel(paddle_column[1], paddle_row, 9)
score = 0
high_score = 0
        
#ball vars
ball_column = 2
ball_row = 0
ball_speed = 500
ball_moved_time = 0

display.set_pixel(ball_column, ball_row, 9)



collision_detected = False
#sleep(500)

while True:

    current_time = running_time()

    

    if button_a.was_pressed():
        if paddle_column[0] - 1 >= 0:
            
            display.set_pixel(paddle_column[0], paddle_row, 0)
            display.set_pixel(paddle_column[1], paddle_row, 0)
            
            paddle_column[0] -= 1
            paddle_column[1] -= 1
            display.set_pixel(paddle_column[0], paddle_row, 9)
            display.set_pixel(paddle_column[1], paddle_row, 9)
        else:
            pass

    if button_b.was_pressed():
        if paddle_column[1] + 1 <= 4:

            display.set_pixel(paddle_column[0], paddle_row, 0)
            display.set_pixel(paddle_column[1], paddle_row, 0)
            
            paddle_column[0] += 1
            paddle_column[1] += 1

            
            display.set_pixel(paddle_column[0], paddle_row, 9)
            display.set_pixel(paddle_column[1], paddle_row, 9)
        else:
            pass


    if current_time > ball_moved_time + ball_speed:
        
        ball_moved_time = current_time
        
        if ball_row - 1 < 4:
            
            display.set_pixel(ball_column, ball_row, 0)
            
            ball_row += 1
            
            display.set_pixel(ball_column, ball_row, 9)

        if ball_row == 4 and (ball_column == paddle_column[0] or ball_column = paddle_column[1]

        ball_moved_time = current_time


    







