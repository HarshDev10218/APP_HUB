import tkinter as tk
import math
import pygame as pyg
import time
import random

def switch_screen(root, next_screen_function):
    for widget in root.winfo_children():
        widget.destroy()
    next_screen_function(root)

def Home(root):
    Label_Home = tk.Label(root, text="HOME SCREEN", font=("Arial", 20, "bold"))
    Label_Home.pack(pady=20)
    
    btn_Calc = tk.Button(root, text="Calculator", font=("Arial", 16), width=15,
                         command=lambda: switch_screen(root, open_Calc))
    btn_Snake = tk.Button(root, text="Snake Game", font=("Arial", 16), width=15,
                          command=lambda: switch_screen(root, open_Snake))
    btn_Space = tk.Button(root, text="Space Game", font=("Arial", 16), width=15,
                          command=lambda: switch_screen(root, open_Space))
    btn_Pig = tk.Button(root, text="Pig Game", font=("Arial", 16), width=15,
                        command=lambda: switch_screen(root, open_Pig))
    
    btn_Calc.pack(pady=10)
    btn_Snake.pack(pady=10)
    btn_Space.pack(pady=10)
    btn_Pig.pack(pady=10)

def open_Calc(root):
    equation = tk.StringVar(value="0")
    expression = [""]

    def press(value):
        expression[0] += str(value)
        equation.set(expression[0])

    def clear():
        expression[0] = ""
        equation.set("0")

    def equal_press():
        try:
            exp = expression[0].replace("^", "**")
            result = str(eval(exp))
            equation.set(result)
            expression[0] = result
        except:
            equation.set("ERROR")
            expression[0] = ""

    def sqrt_press():
        try:
            num = float(expression[0])
            if num < 0:
                raise ValueError
            result = round(math.sqrt(num), 6)
            equation.set(str(result))
            expression[0] = str(result)
        except:
            equation.set("ERROR")
            expression[0] = ""

    def log_press():
        try:
            num = float(expression[0])
            if num <= 0:
                raise ValueError
            result = round(math.log10(num), 6)
            equation.set(str(result))
            expression[0] = str(result)
        except:
            equation.set("ERROR")
            expression[0] = ""

    def trig_press(function):
        try:
            num = float(expression[0])
            if function == "sin":
                result = math.sin(math.radians(num))
            elif function == "cos":
                result = math.cos(math.radians(num))
            elif function == "tan":
                if num % 180 == 90:
                    raise ValueError
                result = math.tan(math.radians(num))
            elif function == "asin":
                if num < -1 or num > 1:
                    raise ValueError
                result = math.degrees(math.asin(num))
            elif function == "acos":
                if num < -1 or num > 1:
                    raise ValueError
                result = math.degrees(math.acos(num))
            elif function == "atan":
                result = math.degrees(math.atan(num))

            result = round(result, 6)
            equation.set(str(result))
            expression[0] = str(result)
        except:
            equation.set("ERROR")
            expression[0] = ""

    def factorial_press():
        try:
            num = float(expression[0])
            if num < 0 or not num.is_integer():
                raise ValueError
            result = math.factorial(int(num))
            equation.set(str(result))
            expression[0] = str(result)
        except:
            equation.set("ERROR")
            expression[0] = ""

    def pi_press():
        expression[0] = str(math.pi)
        equation.set(expression[0])

    def e_press():
        expression[0] = str(math.e)
        equation.set(expression[0])

    display = tk.Entry(root, textvariable=equation, font=("Arial", 20), justify="right", width=20, bd=10)
    display.grid(row=0, column=0, columnspan=5, ipady=15, padx=10, pady=10, sticky="nsew")

    buttons = [
        ("sin", 1, 0), ("cos", 1, 1), ("tan", 1, 2), ("√", 1, 3), ("C", 1, 4),
        ("asin", 2, 0), ("acos", 2, 1), ("atan", 2, 2), ("log", 2, 3), ("/", 2, 4),
        ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("*", 3, 3), ("^", 3, 4),
        ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("-", 4, 3), ("π", 4, 4),
        ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3), ("e", 5, 4),
        ("0", 6, 0), (".", 6, 1), ("!", 6, 2), ("=", 6, 3)
    ]
    
    for (text, row, col) in buttons:
        if text == "C": action = clear
        elif text == "=": action = equal_press
        elif text == "√": action = sqrt_press
        elif text == "log": action = log_press
        elif text in ["sin", "cos", "tan", "asin", "acos", "atan"]: action = lambda t=text: trig_press(t)
        elif text == "!": action = factorial_press
        elif text == "π": action = pi_press
        elif text == "e": action = e_press
        else: action = lambda t=text: press(t)

        btn = tk.Button(root, text=text, font=("Arial", 12, "bold"), width=5, height=2, command=action)

        if text == "=":
            btn.grid(row=row, column=col, columnspan=2, padx=5, pady=5, sticky="nsew")
        else:
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    exit_btn = tk.Button(root, text="Exit", font=("Arial", 14, "bold"), command=lambda: switch_screen(root, Home))
    exit_btn.grid(row=7, column=0, columnspan=5, pady=10, sticky="nsew")

    for i in range(8): root.grid_rowconfigure(i, weight=1)
    for i in range(5): root.grid_columnconfigure(i, weight=1)

def open_Snake(root):
    root.withdraw()
    run_snake_game()
    root.deiconify()
    for widget in root.winfo_children():
        widget.destroy()
    Home(root)

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read().strip())
    except:
        return 0

def save_high_score(new_score):
    current_high = load_high_score()
    if new_score > current_high:
        with open("highscore.txt", "w") as file:
            file.write(str(new_score))

def draw_snake(screen, colour, snake_list, block_size):
    for block in snake_list:
        pyg.draw.rect(screen, colour, [block[0], block[1], block_size, block_size])

def spawn_food(block_size):
    food_x = random.randrange(0, 600 - block_size, block_size)
    food_y = random.randrange(0, 500 - block_size, block_size)
    return food_x, food_y

def show_start_menu(screen):
    font_title = pyg.font.SysFont("Arial", 45, bold=True)
    font_sub = pyg.font.SysFont("Arial", 20)
    
    menu_running = True
    while menu_running:
        screen.fill((10, 20, 30))
        title_surf = font_title.render("SNAKE ARCADE", True, (0, 255, 255))
        start_surf = font_sub.render("Press S to Start Game", True, (0, 225, 0))
        score_surf = font_sub.render("Press H to View High Score", True, (225, 225, 0))
        exit_surf = font_sub.render("Press Q to Quit to Hub", True, (255, 100, 100))
        
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 120))
        screen.blit(start_surf, (300 - start_surf.get_width() // 2, 230))
        screen.blit(score_surf, (300 - score_surf.get_width() // 2, 280))
        screen.blit(exit_surf, (300 - exit_surf.get_width() // 2, 330))
        
        pyg.display.update()
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return "QUIT"
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_s: return "PLAY"
                if event.key == pyg.K_q: return "QUIT"
                if event.key == pyg.K_h:
                    high_score = load_high_score()
                    showing_score = True
                    while showing_score:
                        screen.fill((10, 20, 30))
                        hs_title = font_title.render("HIGH SCORE", True, (225, 225, 0))
                        hs_val = font_title.render(f"{high_score}", True, (255, 255, 255))
                        back_surf = font_sub.render("Press any key to go back", True, (200, 200, 200))
                        
                        screen.blit(hs_title, (300 - hs_title.get_width() // 2, 150))
                        screen.blit(hs_val, (300 - hs_val.get_width() // 2, 230))
                        screen.blit(back_surf, (300 - back_surf.get_width() // 2, 350))
                        pyg.display.update()
                        
                        for sub_event in pyg.event.get():
                            if sub_event.type == pyg.QUIT: return "QUIT"
                            if sub_event.type == pyg.KEYDOWN: showing_score = False

def show_game_over_menu(screen, score):
    font_title = pyg.font.SysFont("Arial", 40, bold=True)
    font_sub = pyg.font.SysFont("Arial", 20)
    
    menu_running = True
    while menu_running:
        screen.fill((20, 10, 10))
        title_surf = font_title.render("GAME OVER", True, (255, 50, 50))
        score_surf = font_sub.render(f"Final Score: {score}", True, (255, 255, 255))
        retry_surf = font_sub.render("Press R to Restart", True, (0, 225, 0))
        exit_surf = font_sub.render("Press Q to Quit to App Hub", True, (225, 225, 0))
        
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 150))
        screen.blit(score_surf, (300 - score_surf.get_width() // 2, 220))
        screen.blit(retry_surf, (300 - retry_surf.get_width() // 2, 300))
        screen.blit(exit_surf, (300 - exit_surf.get_width() // 2, 350))
        
        pyg.display.update()
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT: return "QUIT"
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_r: return "RESTART"
                if event.key == pyg.K_q: return "QUIT"

def run_snake_game():
    pyg.init()
    screen = pyg.display.set_mode((600, 500))
    pyg.display.set_caption("SNAKE GAME")

    block_size = 20
    colour = (225, 225, 0)
    food_colour = (225, 0, 0)
    clock = pyg.time.Clock()
    
    menu_choice = show_start_menu(screen)
    if menu_choice == "QUIT":
        pyg.quit()
        return

    game_running = True
    while game_running:
        snake_x = 300
        snake_y = 240
        x_change = 0
        y_change = 0
        snake_list = []
        snake_length = 1
        food_x, food_y = spawn_food(block_size)
        
        round_active = True
        while round_active:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    round_active = False
                    game_running = False

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_LEFT and x_change == 0:
                        x_change = -block_size
                        y_change = 0
                    elif event.key == pyg.K_RIGHT and x_change == 0:
                        x_change = block_size
                        y_change = 0
                    elif event.key == pyg.K_UP and y_change == 0:
                        y_change = -block_size
                        x_change = 0
                    elif event.key == pyg.K_DOWN and y_change == 0:
                        y_change = block_size
                        x_change = 0

            snake_x += x_change
            snake_y += y_change

            if snake_x == food_x and snake_y == food_y:
                food_x, food_y = spawn_food(block_size)
                snake_length += 1

            if snake_x >= 600 or snake_x < 0 or snake_y >= 500 or snake_y < 0:
                round_active = False 

            snake_head = [snake_x, snake_y]
            if (x_change != 0 or y_change != 0) and snake_head in snake_list:
                round_active = False

            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            screen.fill((0, 0, 0))
            draw_snake(screen, colour, snake_list, block_size)
            pyg.draw.rect(screen, food_colour, [food_x, food_y, block_size, block_size])
            
            pyg.display.update()
            clock.tick(15)

        if game_running:
            score = snake_length - 1
            save_high_score(score)
            choice = show_game_over_menu(screen, score)
            if choice == "QUIT":
                game_running = False

    pyg.quit()

def open_Space(root):
    root.withdraw()
    run_space_game()
    root.deiconify()
    for widget in root.winfo_children():
        widget.destroy()
    Home(root)

def spawn_enemies():
    enemies = []
    for row in range(3):
        for col in range(8):
            enemies.append([50 + col * 60, 50 + row * 40])
    return enemies

def show_space_start_menu(screen):
    font_title = pyg.font.SysFont("Arial", 45, bold=True)
    font_sub = pyg.font.SysFont("Arial", 20)
    
    menu_running = True
    while menu_running:
        screen.fill((10, 10, 25))
        title_surf = font_title.render("SPACE INVADERS", True, (0, 162, 232))
        start_surf = font_sub.render("Press S to Start Game", True, (0, 225, 0))
        exit_surf = font_sub.render("Press Q to Quit to Hub", True, (255, 100, 100))
        
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 150))
        screen.blit(start_surf, (300 - start_surf.get_width() // 2, 260))
        screen.blit(exit_surf, (300 - exit_surf.get_width() // 2, 320))
        pyg.display.update()
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT: return "QUIT"
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_s: return "PLAY"
                if event.key == pyg.K_q: return "QUIT"

def show_space_game_over(screen, score):
    font_title = pyg.font.SysFont("Arial", 40, bold=True)
    font_sub = pyg.font.SysFont("Arial", 20)
    
    menu_running = True
    while menu_running:
        screen.fill((20, 10, 10))
        title_surf = font_title.render("GAME OVER", True, (255, 50, 50))
        score_surf = font_sub.render(f"Final Score: {score}", True, (255, 255, 255))
        retry_surf = font_sub.render("Press R to Restart", True, (0, 225, 0))
        exit_surf = font_sub.render("Press Q to Quit to App Hub", True, (225, 225, 0))
        
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 150))
        screen.blit(score_surf, (300 - score_surf.get_width() // 2, 220))
        screen.blit(retry_surf, (300 - retry_surf.get_width() // 2, 300))
        screen.blit(exit_surf, (300 - exit_surf.get_width() // 2, 350))
        pyg.display.update()
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT: return "QUIT"
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_r: return "RESTART"
                if event.key == pyg.K_q: return "QUIT"

def run_space_game():
    pyg.init()
    screen = pyg.display.set_mode((600, 600))
    pyg.display.set_caption("SPACE INVADERS")

    menu_choice = show_space_start_menu(screen)
    if menu_choice == "QUIT":
        pyg.quit()
        return

    player_width, player_height = 40, 20
    player_speed = 7
    player_colour = (0, 162, 232)
    laser_width, laser_height = 4, 15
    laser_speed = -10
    laser_colour = (255, 242, 0)
    enemy_width, enemy_height = 30, 20
    enemy_colour = (255, 0, 128)

    clock = pyg.time.Clock()
    game_running = True

    while game_running:
        player_x = 300 - (player_width // 2)
        player_y = 540
        move_left = False
        move_right = False
        lasers = []
        enemies = spawn_enemies()
        score = 0
        enemy_drop_speed = 1
        
        round_active = True
        while round_active:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    round_active = False
                    game_running = False

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_LEFT: move_left = True
                    elif event.key == pyg.K_RIGHT: move_right = True
                    elif event.key == pyg.K_SPACE:
                        lasers.append([player_x + (player_width // 2) - (laser_width // 2), player_y])

                if event.type == pyg.KEYUP:
                    if event.key == pyg.K_LEFT: move_left = False
                    elif event.key == pyg.K_RIGHT: move_right = False

            if move_left and player_x > 0: player_x -= player_speed
            if move_right and player_x < 600 - player_width: player_x += player_speed

            for laser in lasers: laser[1] += laser_speed
            lasers = [l for l in lasers if l[1] > 0]

            for enemy in enemies:
                enemy[1] += enemy_drop_speed
                if enemy[1] + enemy_height >= player_y: round_active = False

            hit_lasers, hit_enemies = [], []
            for laser in lasers:
                for enemy in enemies:
                    if (laser[0] + laser_width > enemy[0] and laser[0] < enemy[0] + enemy_width and
                        laser[1] + laser_height > enemy[1] and laser[1] < enemy[1] + enemy_height):
                        hit_lasers.append(laser)
                        hit_enemies.append(enemy)
                        score += 10

            lasers = [l for l in lasers if l not in hit_lasers]
            enemies = [e for e in enemies if e not in hit_enemies]

            if len(enemies) == 0:
                enemies = spawn_enemies()
                enemy_drop_speed += 0.5

            screen.fill((10, 10, 25))
            pyg.draw.rect(screen, player_colour, [player_x, player_y, player_width, player_height])
            for l in lasers: pyg.draw.rect(screen, laser_colour, [l[0], l[1], laser_width, laser_height])
            for e in enemies: pyg.draw.rect(screen, enemy_colour, [e[0], e[1], enemy_width, enemy_height])

            font_hud = pyg.font.SysFont("Arial", 16)
            screen.blit(font_hud.render(f"SCORE: {score}", True, (255, 255, 255)), (10, 10))
            pyg.display.update()
            clock.tick(60)

        if game_running:
            choice = show_space_game_over(screen, score)
            if choice == "QUIT": game_running = False

    pyg.quit()

def open_Pig(root):
    root.withdraw()
    run_pig_game()
    root.deiconify()
    for widget in root.winfo_children():
        widget.destroy()
    Home(root)

def get_name_from_pygame(screen, prompt):
    name = ""
    typing = True
    font = pyg.font.SysFont("Arial", 32)
    clock = pyg.time.Clock()

    while typing:
        screen.fill((30, 20, 25))
        prompt_surf = font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_surf, (300 - prompt_surf.get_width() // 2, 150))
        name_surf = font.render(name, True, (0, 255, 0))
        screen.blit(name_surf, (300 - name_surf.get_width() // 2, 250))
        pyg.display.update()

        for event in pyg.event.get():
            if event.type == pyg.QUIT: return None
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_RETURN:
                    if len(name) > 0: typing = False
                elif event.key == pyg.K_BACKSPACE: name = name[:-1]
                else:
                    if len(name) < 12 and event.unicode.isalnum(): name += event.unicode
        clock.tick(30)
    return name

def show_pig_start_menu(screen):
    font_title = pyg.font.SysFont("Arial", 45, bold=True)
    font_sub = pyg.font.SysFont("Arial", 20)
    
    menu_running = True
    while menu_running:
        screen.fill((30, 20, 25))
        title_surf = font_title.render("THE PIG GAME", True, (255, 105, 180))
        start_surf = font_sub.render("Press S to Start Game", True, (0, 225, 0))
        exit_surf = font_sub.render("Press Q to Quit to Hub", True, (255, 100, 100))
        
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 150))
        screen.blit(start_surf, (300 - start_surf.get_width() // 2, 260))
        screen.blit(exit_surf, (300 - exit_surf.get_width() // 2, 320))
        pyg.display.update()
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT: return "QUIT"
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_s: return "PLAY"
                if event.key == pyg.K_q: return "QUIT"

def show_pig_game_over(screen, winner_name, score):
    font_title = pyg.font.SysFont("Arial", 40, bold=True)
    font_sub = pyg.font.SysFont("Arial", 20)
    
    menu_running = True
    while menu_running:
        screen.fill((20, 10, 10))
        title_surf = font_title.render(f"{winner_name} WINS!", True, (0, 255, 0))
        score_surf = font_sub.render(f"Winning Score: {score}", True, (255, 255, 255))
        retry_surf = font_sub.render("Press R to Restart", True, (0, 225, 0))
        exit_surf = font_sub.render("Press Q to Quit to App Hub", True, (225, 225, 0))
        
        screen.blit(title_surf, (300 - title_surf.get_width() // 2, 150))
        screen.blit(score_surf, (300 - score_surf.get_width() // 2, 220))
        screen.blit(retry_surf, (300 - retry_surf.get_width() // 2, 300))
        screen.blit(exit_surf, (300 - exit_surf.get_width() // 2, 350))
        pyg.display.update()
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT: return "QUIT"
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_r: return "RESTART"
                if event.key == pyg.K_q: return "QUIT"

def run_pig_game():
    pyg.init()
    screen = pyg.display.set_mode((600, 500))
    pyg.display.set_caption("THE PIG GAME")

    menu_choice = show_pig_start_menu(screen)
    if menu_choice == "QUIT":
        pyg.quit()
        return

    p1_name = get_name_from_pygame(screen, "Enter Player 1 Name:")
    if p1_name is None: return
    p2_name = get_name_from_pygame(screen, "Enter Player 2 Name:")
    if p2_name is None: return

    font_text = pyg.font.SysFont("Arial", 24)
    font_dice = pyg.font.SysFont("Arial", 60, bold=True)
    clock = pyg.time.Clock()
    game_running = True

    while game_running:
        scores = [0, 0]
        current_turn_score = 0
        current_player = 0
        last_roll = 0
        
        round_active = True
        while round_active:
            current_name = p1_name if current_player == 0 else p2_name
            
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    round_active = False
                    game_running = False

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_r:
                        last_roll = random.randint(1, 6)
                        if last_roll == 1:
                            current_turn_score = 0
                            current_player = 1 - current_player
                        else:
                            current_turn_score += last_roll
                    elif event.key == pyg.K_h:
                        scores[current_player] += current_turn_score
                        current_turn_score = 0
                        if scores[current_player] >= 100: round_active = False
                        else: current_player = 1 - current_player

            screen.fill((30, 20, 25))
            p1_surf = font_text.render(f"{p1_name}: {scores[0]} pts", True, (255, 255, 255))
            p2_surf = font_text.render(f"{p2_name}: {scores[1]} pts", True, (255, 255, 255))
            screen.blit(p1_surf, (50, 50))
            screen.blit(p2_surf, (400 - p2_surf.get_width() + 150, 50))
            
            turn_surf = font_text.render(f"{current_name}'s Turn", True, (255, 105, 180))
            running_surf = font_text.render(f"Turn Score: {current_turn_score}", True, (0, 255, 0))
            prompt_surf = font_text.render("Press [R] to Roll | Press [H] to Hold", True, (200, 200, 200))
            
            screen.blit(turn_surf, (300 - turn_surf.get_width() // 2, 160))
            screen.blit(running_surf, (300 - running_surf.get_width() // 2, 210))
            screen.blit(prompt_surf, (300 - prompt_surf.get_width() // 2, 420))
            
            if last_roll > 0:
                dice_color = (255, 50, 50) if last_roll == 1 else (255, 255, 255)
                dice_surf = font_dice.render(f"[{last_roll}]", True, dice_color)
                screen.blit(dice_surf, (300 - dice_surf.get_width() // 2, 280))
                
            pyg.display.update()
            clock.tick(30)

        if game_running:
            winner_name = p1_name if scores[0] >= 100 else p2_name
            choice = show_pig_game_over(screen, winner_name, max(scores))
            if choice == "QUIT": game_running = False

    pyg.quit()

def main():
    root = tk.Tk()
    root.title("App Hub")
    root.geometry("310x520")
    Home(root)
    root.mainloop()

if __name__ == "__main__" :
    main()
