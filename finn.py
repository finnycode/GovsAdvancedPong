
ball_slope = -1
send_string = [1,ball_slope]

send_string = str(send_string)

send_string = list(send_string)

print(send_string[1])
print(send_string[4])
print(type(send_string))

slope_str = send_string[4] + send_string[5]

slope = int(slope_str)

print(slope)
