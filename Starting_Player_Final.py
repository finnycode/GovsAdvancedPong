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
# Establish radio group
radio.config(group=5)
# Turn the radio on
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


iteration = 0

listen = False

#game start loop 

touching_logo = False

#loop runs to start game if both players touch top button

while True:
    if pin_logo.is_touched():
        touching_logo == True
    if touching_logo:
        radio.send('8')
    start_now = radio.receive()

    start_now = str(start_now)

    if start_now[0] == '8':
        radio.send('9')
        radio.off()
        break
        
    if touching_logo:
        if start_now == '9':
            radio.off()
            break
    


current_time = running_time()

stupid_loop_start = running_time()

#2 second buffer

radio.config(group=69)
while current_time < stupid_loop_start + 2000:

    current_time = running_time()

current_time = 0 

#main game loop

while True:

    #message = radio.receive()

    #configure radio again

    radio.on()

    radio.config(group=69)
    
    current_time = running_time()


    #code to move paddles left and right 
    

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

    # logic to move the ball, paddles, and do all of the game logic. more specfic comments below

    if current_time > ball_moved_time + ball_speed:
        
        ball_moved_time = current_time

        # variables for the ball trail
            
        older_prev_ball_column, older_prev_ball_row = prev_ball_column, prev_ball_row
        
        prev_ball_column = ball_column
        prev_ball_row = ball_row

        #paddle collision logic

        if ball_row == 4:
            if ball_column == paddle_column[0] or ball_column == paddle_column[1]:
                ball_direction = -1
                #ball_row += ball_direction
                ball_moved_time = current_time
                hit_paddle = True
            else:
                display.show('L') #ends the game if player misses and tells the other microbit that they've won
                radio.send('L')

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

        if gotten_message[0] == 'w':
        # Display 'W' on screen if "w" is recieved
            while True:
                display.show('W')
        
        if gotten_message[1] == '1' and ball_on_my_side == False:
            ball_on_my_side = True
            #display.scroll(1)    

            listen = False
    
    
            # Reset ball vars
            ball_column = 2
            ball_row = 0
            ball_speed = 300
            ball_moved_time = 0
            ball_direction = 1 # positive being moving towards player

           
            try:
                ball_slope = int(gotten_message[4])
            except:
                ball_slope = -1
            
            
            
            prev_ball_column = ball_column
            prev_ball_row = ball_row
            older_prev_ball_column = None
            older_prev_ball_row = None
            
            display.set_pixel(ball_column, ball_row, 9)
            
            # Reset button vars
            
            button_pressed_time = 0
            time_difference = 0
            collision_detected = False
            
            
            iteration = 0
            
            hit_paddle = False
            paddle_moved_direction = 'straight'
            last_paddle_direction = None
    
            
        #Clear message and wait for the next loop
            gotten_message = '0'

            message = None
    
            while True:
        
                #display.scroll(1)

                w_or_l = radio.receive()

                if str(w_or_l)[0] == 'w':
                    while True:
                        display.show('W')
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
                        else:
                            display.show('L') #ends the game if player misses and tells the other microbit that they've won
                            radio.send('L') #fix dis ASAP

                        
                    
            
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
                               
                                            
                                        
                                
                    
                
                                
                            display.set_pixel(ball_column, ball_row, 9)
                            hit_paddle = False
                        else:
                            display.set_pixel(ball_column, ball_row, 0)
                                
                        ball_column += ball_slope
                        ball_row += ball_direction

                        try:
                            display.set_pixel(ball_column, ball_row, 9)
                        except:
                            radio.send('w')
                            while True:
                                display.show('L')
                
                
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
