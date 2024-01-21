#Finn Allen & Laird Gerdes
#1/21/23
#Governor's Academy
#Honors Engineering
#The following code is pong pong pong pong pong, a game that is similar to the pong game. 

#starting code for the microbit that sends the ball to the other microbit


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
                radio.send('w')

        #changes the slope of the ball if it hits the wall

        if ball_column == 0:
            ball_slope = 1

        if ball_column == 4:
            ball_slope = -1

        #if the ball reaches the top of the screen it sends a message to the other microbit to accept the ball

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

            #if the ball hits the paddle it checks if the button was pressed within 500 ms and changes the slope of the ball to replicate the ball being hit at an angle
                

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

            #moves the ball on the screen
                
            ball_column += ball_slope
            ball_row += ball_direction
            
            display.set_pixel(ball_column, ball_row, 9)

            #trail logic for the ball  

            if older_prev_ball_row is not None and older_prev_ball_column is not None:
                display.set_pixel(older_prev_ball_column, older_prev_ball_row, 0)

            # Update the trail position
            # Check if the previous position is not out of bounds
            if 0 <= prev_ball_row < 5 and 0 <= prev_ball_column < 5:
                #display the trail
                display.set_pixel(prev_ball_column, prev_ball_row, 3) # make it dimmer 

            for col in paddle_column:
                display.set_pixel(col, paddle_row, 9)
        iteration+=1


#second loop after the ball is recived again from the other microbit


while True:

    #listening for any win or loss messages
        
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
        

                #check for win or loss messages


                w_or_l = radio.receive()

                if str(w_or_l)[0] == 'w':
                    while True:
                        display.show('W')
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
                            radio.send('w') #fix dis ASAP

                        
                    #changes the slope of the ball if it hits the wall
            
                    if ball_column == 0:
                        ball_slope = 1
                
                    if ball_column == 4:
                        ball_slope = -1

                    #if the ball reaches the top of the screen it sends a message to the other microbit to accept the ball
                
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
                
                            
                        #if the ball hits the paddle it checks if the button was pressed within 500 ms and changes the slope of the ball to replicate the ball being hit at an angle
                
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
                

                        #trail logic for the ball
                
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


###################################
                        

#Finn Allen & Laird Gerdes
#1/21/23
#Governor's Academy
#Honors Engineering
#The following code is pong pong pong pong pong, a game that is similar to the pong game. 
                        
#reciving microbit code

# Imports go at the top
from microbit import *
import time as t
import random
import radio
#paddle vars
paddle_column = [0,1]
paddle_row = 4
display.set_pixel(paddle_column[0], paddle_row, 9)
display.set_pixel(paddle_column[1], paddle_row, 9)
hit_paddle = False
paddle_moved_direction = 'straight'
last_paddle_direction = None

ball_on_my_side = False


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

ball_on_my_side = False

#set radio group and turn it on to listen for other microbit
radio.config(group=5)
radio.on()

listen = True

display.set_pixel(ball_column, ball_row, 9)

#button vars

button_pressed_time = 0
time_difference = 0
collision_detected = False
#sleep(500)

iteration = 0

touching_logo = False

#loop runs to start game if both players touch top button

while True:
    if pin_logo.is_touched():
        touching_logo = True
    if touching_logo:
        radio.send('8')
    start_now = radio.receive()

    start_now = str(start_now)

    if start_now[0] == '8':
        radio.send('9')
        break

    if touching_logo:
        if start_now[0] == '9':
            break
#stupid_loop delay for 2 seconds
stupid_loop_start = 0

#2 second buffer

current_time = running_time()

stupid_loop_start = running_time()

radio.config(group=69)

while current_time < stupid_loop_start + 2000:

    current_time = running_time()

current_time = 0

#Main game loop


while True:


    if listen:
        message = radio.receive()
    else:
        message = None
    

    #win or loss message logic

    if message is not None and listen:
        
        gotten_message = message

        if gotten_message[0] == 'w':
            while True:
                display.show('W')

        
        #code to recive the ball from the other microbit
        
        if gotten_message[1] == '1' and ball_on_my_side == False:
            
            
            ball_on_my_side == True

            listen = False
            #turn off radio
            
        

        
            hit_paddle = False
            paddle_moved_direction = 'straight'
            last_paddle_direction = None

            #ball vars
            ball_column = 2
            ball_row = 0
            ball_speed = 300 # 3 ms between pixel movements
            ball_moved_time = 0
            ball_direction = 1 # positive being moving towards player

            try:
                ball_slope = int(gotten_message[4])
            except:
                ball_slope = -1
                    
            #trail vars
            
            prev_ball_column = ball_column
            prev_ball_row = ball_row
            older_prev_ball_column = None
            older_prev_ball_row = None

            #button vars

            button_pressed_time = 0
            time_difference = 0
            collision_detected = False

            iteration = 0


            gotten_message = '0'

            message = None

            #logic to see if win or loss message is sent
    
            while True:

                w_or_l = radio.receive()

                if str(w_or_l)[0] == 'w':
                    while True:
                        display.show('W')
                current_time = running_time()
            
                
                #Code for left movement

                #code to move paddles left and right

                # Move paddle left
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

                # Code for moving right
                if button_b.was_pressed():
                    button_pressed_time = current_time
                    paddle_moved_direction = 'right'
                    last_paddle_direction = 'right'
                    
                    if paddle_column[1] + 1 <= 4:
                    # move paddle right
                        display.set_pixel(paddle_column[0], paddle_row, 0)
                        display.set_pixel(paddle_column[1], paddle_row, 0)
                        
                        paddle_column[0] += 1
                        paddle_column[1] += 1
            
                        
                        display.set_pixel(paddle_column[0], paddle_row, 9)
                        display.set_pixel(paddle_column[1], paddle_row, 9)
                    else:
                        pass
            
            
                # logic to move the ball, paddles, and do all of the game logic. more specfic comments below

                if current_time > ball_moved_time + ball_speed:# wait 3 ms
                    
                    ball_moved_time = current_time
            
                    older_prev_ball_column, older_prev_ball_row = prev_ball_column, prev_ball_row
                    
                    prev_ball_column = ball_column
                    prev_ball_row = ball_row
                    # Check if ball hit the paddle
                    if ball_row == 4:
                        if ball_column == paddle_column[0] or ball_column == paddle_column[1]:
                            ball_direction = -1
                            #ball_row += ball_direction
                            ball_moved_time = current_time
                            hit_paddle = True
                        
                    # Check if ball hits left wall, if so change slope
                    if ball_column == 0:
                        ball_slope = 1
                    # Check if ball hits right wall, if so change slope 
                    if ball_column == 4:
                        ball_slope = -1
            
                    #Ball transfer between microbits
                    if ball_row == 0 and iteration > 0:
                        ball_direction = 1
                        send_string = [1,ball_slope]# The message "1" initializes the code on the other microbit
                        radio.send(str(send_string))
                        ball_on_my_side = False
                        display.set_pixel(ball_column, ball_row, 0)
                        display.set_pixel(older_prev_ball_column, older_prev_ball_row, 0)
                        listen = True
                        break 
            
                        

                    if ball_row < 5:
                        # Check collision and change slope accordingly


                        if hit_paddle:
            
                            time_difference = current_time - button_pressed_time
            
                            # If the button was pressed within 500 ms of the ball hitting the paddle, change the slope of the ball to replicate the ball being hit at an angle
            
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
                         #Updates ball position using the slope and direction   
                        ball_column += ball_slope
                        ball_row += ball_direction

                        

                        try:
                            display.set_pixel(ball_column, ball_row, 9)
                        except:
                            radio.send('w')
                            display.show('L')
                            #if the ball position is unavailable send winning message to other microbit and present losing message
                        if older_prev_ball_row is not None and older_prev_ball_column is not None:
                            display.set_pixel(older_prev_ball_column, older_prev_ball_row, 0) #clear ball trail
            
                        # Update the trail position
                        # Check if the previous position is not out of bounds
                        if 0 <= prev_ball_row < 5 and 0 <= prev_ball_column < 5:
                            # Set the previous position of the ball to a dimmer light to create a trail effect
                            display.set_pixel(prev_ball_column, prev_ball_row, 3) # Adjust the brightness as needed
            
                        for col in paddle_column:
                            display.set_pixel(col, paddle_row, 9)
                    iteration+=1
            
