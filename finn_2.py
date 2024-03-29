#Name
#5/12/23
#Governor's Academy
#Honors Engineering
#The following codes for a game that is similar to the pong game. 

# Imports go at the top
from microbit import *
import time as t
import random
import radio

radio.config(group=5)

radio.on()

#paddle vars
paddle_column = [0,1]
paddle_row = 4
display.set_pixel(paddle_column[0], paddle_row, 9)
display.set_pixel(paddle_column[1], paddle_row, 9)
hit_paddle = False
paddle_moved_direction = 'straight'
last_paddle_direction = None

ball_on_my_side = True #lairds is false
ball_is_on_my_side_again = False

score = 0
high_score = 0
        
#ball vars
ball_column = 2
ball_row = 0
ball_speed = 300
ball_moved_time = 0
ball_direction = 1 # positive being moving towards player
ball_slope = 0 # -1 being moving up left 1 being moving up right
prev_ball_column = ball_column
prev_ball_row = ball_row
older_prev_ball_column = None
older_prev_ball_row = None

display.set_pixel(ball_column, ball_row, 9)

#button vars

button_pressed_time = 0
time_difference = 0
collision_detected = False
#sleep(500)

iteration = 0

listen = False



while True:

    #message = radio.receive()

    
    current_time = running_time()

    

    if button_a.was_pressed():
        button_pressed_time = current_time
        paddle_moved_direction = 'left'
        last_paddle_direction = 'left'
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
        button_pressed_time = current_time
        paddle_moved_direction = 'right'
        last_paddle_direction = 'right'
        
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

        older_prev_ball_column, older_prev_ball_row = prev_ball_column, prev_ball_row
        
        prev_ball_column = ball_column
        prev_ball_row = ball_row

        if ball_row == 4:
            if ball_column == paddle_column[0] or ball_column == paddle_column[1]:
                ball_direction = -1
                #ball_row += ball_direction
                ball_moved_time = current_time
                hit_paddle = True

        if ball_column == 0:
            ball_slope = 1

        if ball_column == 4:
            ball_slope = -1

        if iteration > 0 and ball_row == 0:
            ball_direction = 1
            send_string = [1,ball_slope]
            radio.send(str(send_string))
            ball_on_my_side = False
            display.set_pixel(ball_column, ball_row, 0)
            display.set_pixel(older_prev_ball_column, older_prev_ball_row, 0)
            listen = True
            break
                
                

        if ball_row < 5:

            
                

            if hit_paddle:

                time_difference = current_time - button_pressed_time


                if time_difference <= 500:
                    if paddle_moved_direction == 'right':
                        if ball_slope == 1:
                            ball_slope = 0
                        else:
                            ball_slope = 1
                            
                    elif paddle_moved_direction == 'left':
                        if ball_slope == -1:
                            ball_slope = 0
                        else:
                            ball_slope = -1
                # else:
                    
                #     ball_slope = 1
                            
                        
                
    

                
                display.set_pixel(ball_column, ball_row, 9)
                hit_paddle = False
            else:
                display.set_pixel(ball_column, ball_row, 0)
                
            ball_column += ball_slope
            ball_row += ball_direction
            
            display.set_pixel(ball_column, ball_row, 9)

            if older_prev_ball_row is not None and older_prev_ball_column is not None:
                display.set_pixel(older_prev_ball_column, older_prev_ball_row, 0)

            # Update the trail position
            # Check if the previous position is not out of bounds
            if 0 <= prev_ball_row < 5 and 0 <= prev_ball_column < 5:
                # Set the previous position of the ball to a dimmer light to create a trail effect
                display.set_pixel(prev_ball_column, prev_ball_row, 3) # Adjust the brightness as needed

            for col in paddle_column:
                display.set_pixel(col, paddle_row, 9)
        iteration+=1





while True:

        
    if listen:
        message = radio.receive()
    else:
        message = None
        
    if message is not None and listen:
        gotten_message = message
        
        if gotten_message[1] == '1' and ball_on_my_side == False:
            ball_on_my_side = True
            #display.scroll(1)    

            listen = False
    
    
            #ball vars
            ball_column = 2
            ball_row = 0
            ball_speed = 300
            ball_moved_time = 0
            ball_direction = 1 # positive being moving towards player

            # if int(gotten_message[4]) == 1 or int(gotten_message[4]) == 0:
            #     ball_slope = int(gotten_message[4]) # -1 being moving up left 1 being moving up right 0 head on

            # else:
            #     try:
            #         slope_str = gotten_message[4] + gotten_message[5]
            #         slope_str = int(slope_str)
            #         ball_slope = slope_str
            #     except:
            #         pass

            try:
                ball_slope = int(gotten_message[4])
            except:
                ball_slope = -1
            
            
            
            prev_ball_column = ball_column
            prev_ball_row = ball_row
            older_prev_ball_column = None
            older_prev_ball_row = None
            
            display.set_pixel(ball_column, ball_row, 9)
            
            #button vars
            
            button_pressed_time = 0
            time_difference = 0
            collision_detected = False
            #sleep(500)
            
            iteration = 0
            
            hit_paddle = False
            paddle_moved_direction = 'straight'
            last_paddle_direction = None
    
            #message = None

            #gotten_message = '0'

            #message = None
    
            while True:
        
                #display.scroll(1)
                    
                current_time = running_time()
                
                    
                
                if button_a.was_pressed():
                    button_pressed_time = current_time
                    paddle_moved_direction = 'left'
                    last_paddle_direction = 'left'
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
                    button_pressed_time = current_time
                    paddle_moved_direction = 'right'
                    last_paddle_direction = 'right'
                        
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
                
                    older_prev_ball_column, older_prev_ball_row = prev_ball_column, prev_ball_row
                        
                    prev_ball_column = ball_column
                    prev_ball_row = ball_row
                
                    if ball_row == 4:
                        if ball_column == paddle_column[0] or ball_column == paddle_column[1]:
                            ball_direction = -1
                            #ball_row += ball_direction
                            ball_moved_time = current_time
                            hit_paddle = True
            
                    if ball_column == 0:
                        ball_slope = 1
                
                    if ball_column == 4:
                        ball_slope = -1
                
                    if iteration > 0 and ball_row == 0:
                        ball_direction = 1
                        send_string = [1,ball_slope]
                        radio.send(str(send_string))
                        ball_on_my_side = False
                        display.set_pixel(ball_column, ball_row, 0)
                        display.set_pixel(older_prev_ball_column, older_prev_ball_row, 0)
                        listen = True
                        break
                                
                                
                
                    if ball_row < 5:
                
                            
                                
                
                        if hit_paddle:
                
                            time_difference = current_time - button_pressed_time
                
                
                            if time_difference <= 500:
                                if paddle_moved_direction == 'right':
                                    if ball_slope == 1:
                                        ball_slope = 0
                                    else:
                                        ball_slope = 1
                                            
                                elif paddle_moved_direction == 'left':
                                    if ball_slope == -1:
                                        ball_slope = 0
                                    else:
                                        ball_slope = -1
                                # else:
                                    
                                #     ball_slope = 1
                                            
                                        
                                
                    
                
                                
                            display.set_pixel(ball_column, ball_row, 9)
                            hit_paddle = False
                        else:
                            display.set_pixel(ball_column, ball_row, 0)
                                
                        ball_column += ball_slope
                        ball_row += ball_direction
                            
                        display.set_pixel(ball_column, ball_row, 9)
                
                        if older_prev_ball_row is not None and older_prev_ball_column is not None:
                            display.set_pixel(older_prev_ball_column, older_prev_ball_row, 0)
                
                            # Update the trail position
                            # Check if the previous position is not out of bounds
                        if 0 <= prev_ball_row < 5 and 0 <= prev_ball_column < 5:
                            # Set the previous position of the ball to a dimmer light to create a trail effect
                            display.set_pixel(prev_ball_column, prev_ball_row, 3) # Adjust the brightness as needed
                
                        for col in paddle_column:
                            display.set_pixel(col, paddle_row, 9)
                        iteration+=1
                    
