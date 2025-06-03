from ursina import *
from random import uniform, choice
app = Ursina()

speed_x = choice([0.1, -0.1])
speed_y = 0
cpu_offset = 0
player_score = 0
cpu_score = 0


player_paddle = Entity(
    model="cube",
    scale=(.5,3,1),
    position=(-6,0,0),
    collider="box"
    )
cpu_paddle = Entity(
    model="cube",
    scale=(.5,3,1),
    position=(6,0,0),
    collider="box"
    )

ball = Entity(
    model="sphere",
    scale=(.5,.5,.5),
    texture="perlin_noise"
    )


scores = Text(text=f"{player_score} : {cpu_score}",
              position=(-.1,.5),
              scale=(5,5)
              )


def update():    
    global speed_x, speed_y, cpu_offset, cpu_score, player_score, score, scores

    
    

    #change ball and cpu paddle position every frame
    ball.x += speed_x
    ball.y += speed_y
    cpu_paddle.y = ball.y + cpu_offset

    #controls for the player paddle, making sure it can't go off the screen
    if held_keys["w"] and player_paddle.screen_position[1] < window.top[1]:
        player_paddle.y += 5 * time.dt
    elif held_keys["s"] and player_paddle.screen_position[1] > window.bottom[1]:
        player_paddle.y -= 5 * time.dt

    #generates a small raycast to detect collision against the paddles
    ball_collision = raycast(ball.position,
                             ball.right,
                             distance=0.26,
                             debug=True
                             )

    
    if ball_collision.hit and ball.x > 0:
        #reverses speed when hits the cpu paddle
        speed_x = -abs(speed_x + .01)
        speed_y += ball.get_position(relative_to=cpu_paddle)[1] / 10
        
        
        ball.look_at(player_paddle, axis="right")

    elif ball_collision.hit and ball.x < 0:
        #reverses speed when hits the player paddle
        speed_x = abs(speed_x - .01)
        speed_y += ball.get_position(relative_to=player_paddle)[1] / 10
        #flips the ball so the raycast hits the other paddle
        ball.look_at(cpu_paddle, axis="right")
        #random offset created to influence the balls speed and direction
        cpu_offset = round(uniform(-2.5, 2.5), 1)

    if ball.screen_position[1] >= window.top[1]:
        #bounces the ball of the top of the screen
        speed_y = -abs(speed_y)
    
    if ball.screen_position[1] <= window.bottom[1]:
        #bounces the ball of the bottom of the screen
        speed_y = abs(speed_y)

    if ball.screen_position[0] <= window.left[0]:
        cpu_score += 1
        ball.position = (0,0,0)
        speed_y = 0
        speed_x = choice([0.1, -0.1])
        cpu_offset = 0

    
    if ball.screen_position[0] >= window.right[0]:
        player_score += 1
        ball.position = (0,0,0)
        speed_y = 0
        speed_x = choice([0.1, -0.1])
        cpu_offset = 0
    scores.text = f"{player_score} : {cpu_score}"


def input(key):
    if key == "left mouse down":
        print(ball.screen_position)
        print(window.top)
    
        


window.borderless = False
EditorCamera()
app.run()
