import pygame
import random
import sys
import time

# Inisialisasi Pygame
pygame.init()

# Warna-warna keren
HITAM = (0, 0, 0)
HIJAU_NEON = (57, 255, 20)
MERAH_NEON = (255, 20, 147)
BIRU_NEON = (20, 191, 255)
KUNING_NEON = (255, 255, 20)
UNGU_NEON = (191, 20, 255)
PUTIH = (255, 255, 255)
ABU_GELAP = (40, 40, 40)
HIJAU_GELAP = (0, 100, 0)

# Setting window
LEBAR = 800
TINGGI = 600
UKURAN_KOTAK = 20

# Bikin window
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Naver Sneaky Game")

# Clock buat FPS
jam = pygame.time.Clock()

# Font buat text
font_besar = pygame.font.Font(None, 48)
font_sedang = pygame.font.Font(None, 32)
font_kecil = pygame.font.Font(None, 24)

class SnakeGame:
    def __init__(self):
        # Posisi awal snake - pastikan sesuai grid
        self.snake_pos = [100, 80]  # koordinat yang sesuai grid 20x20
        self.snake_body = [[100, 80], [80, 80], [60, 80]]  # badan snake juga sesuai grid
        
        # Score dan game state
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.pause = False
        
        # Level system - makin tinggi makin susah
        self.level = 1
        self.base_speed = 8
        self.current_speed = self.base_speed
        
        # Obstacle system
        self.obstacles = []
        self.max_obstacles = 0
        
        # Power-up system
        self.powerups = []
        self.powerup_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        
        # Combo system buat bonus skor
        self.combo = 0
        self.combo_timer = 0
        self.max_combo = 0
        
        # AI Enemy snake
        self.enemy_snake = None
        self.enemy_enabled = False
        self.enemy_particles = []
        
        # Efek visual
        self.trail = []
        self.particles = []
        self.level_up_particles = []
        
        # Posisi makanan random - setelah semua variable diinit
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        
        # Arah gerakan snake
        self.direction = 'RIGHT'
        self.change_to = self.direction
        
    def spawn_food(self):
        # Spawn makanan di posisi random yang gak nabrak snake, obstacle, sama enemy
        while True:
            # Pastikan koordinat sesuai dengan grid UKURAN_KOTAK
            x = random.randrange(0, (LEBAR//UKURAN_KOTAK)) * UKURAN_KOTAK
            y = random.randrange(3, (TINGGI//UKURAN_KOTAK)) * UKURAN_KOTAK  # mulai dari y=60 biar gak nabrak UI
            pos = [x, y]
            
            # Cek gak nabrak semua objek
            if pos not in self.snake_body and pos not in self.obstacles:
                if self.enemy_snake is None or pos not in self.enemy_snake['body']:
                    return pos
    
    def spawn_obstacle(self):
        # Spawn obstacle di posisi random yang aman
        while True:
            x = random.randrange(0, (LEBAR//UKURAN_KOTAK)) * UKURAN_KOTAK
            y = random.randrange(3, (TINGGI//UKURAN_KOTAK)) * UKURAN_KOTAK
            pos = [x, y]
            
            # Jangan spawn deket player atau makanan
            safe_distance = 60
            if (abs(pos[0] - self.snake_pos[0]) < safe_distance and 
                abs(pos[1] - self.snake_pos[1]) < safe_distance):
                continue
            if (abs(pos[0] - self.food_pos[0]) < 40 and 
                abs(pos[1] - self.food_pos[1]) < 40):
                continue
                
            if pos not in self.snake_body and pos not in self.obstacles:
                if self.enemy_snake is None or pos not in self.enemy_snake['body']:
                    return pos
    
    def spawn_powerup(self):
        # Spawn power-up random
        while True:
            x = random.randrange(0, (LEBAR//UKURAN_KOTAK)) * UKURAN_KOTAK
            y = random.randrange(3, (TINGGI//UKURAN_KOTAK)) * UKURAN_KOTAK
            pos = [x, y]
            
            if pos not in self.snake_body and pos not in self.obstacles and pos != self.food_pos:
                powerup_type = random.choice(['shield', 'speed'])
                return {'pos': pos, 'type': powerup_type, 'timer': 300}  # hilang setelah 300 frames
    
    def spawn_enemy_snake(self):
        # Bikin AI enemy snake di sisi yang jauh dari player
        if self.snake_pos[0] < LEBAR // 2:
            enemy_x = LEBAR - 100
        else:
            enemy_x = 100
            
        enemy_y = random.randrange(5, 15) * UKURAN_KOTAK
        
        self.enemy_snake = {
            'pos': [enemy_x, enemy_y],
            'body': [[enemy_x, enemy_y], [enemy_x - UKURAN_KOTAK, enemy_y]],
            'direction': random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        }
    
    def update_direction(self):
        # Update arah berdasarkan input
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
    
    def move_snake(self):
        # Gerakkan snake berdasarkan arah
        if self.direction == 'UP':
            self.snake_pos[1] -= UKURAN_KOTAK
        elif self.direction == 'DOWN':
            self.snake_pos[1] += UKURAN_KOTAK
        elif self.direction == 'LEFT':
            self.snake_pos[0] -= UKURAN_KOTAK
        elif self.direction == 'RIGHT':
            self.snake_pos[0] += UKURAN_KOTAK
        
        # Tambahin head baru di posisi yang baru
        self.snake_body.insert(0, list(self.snake_pos))
        
        # Cek apakah snake head sama dengan posisi makanan
        if (self.snake_pos[0] == self.food_pos[0] and 
            self.snake_pos[1] == self.food_pos[1]):
            # Tambah score dengan combo multiplier
            self.combo += 1
            bonus = self.combo * 5
            self.score += 10 + bonus
            self.combo_timer = 60  # reset combo timer
            
            if self.combo > self.max_combo:
                self.max_combo = self.combo
            
            self.food_spawn = False
            # Bikin partikel efek makan
            self.create_eat_particles()
            
            # Level up tiap 50 skor
            new_level = (self.score // 50) + 1
            if new_level > self.level:
                self.level_up()
        else:
            # Hapus ekor kalau gak makan makanan
            self.snake_body.pop()
        
        # Spawn makanan baru kalau udah dimakan
        if not self.food_spawn:
            self.food_pos = self.spawn_food()
            self.food_spawn = True
    
    def level_up(self):
        # Naik level - speed naik, obstacle bertambah
        self.level = (self.score // 50) + 1
        self.current_speed = min(20, self.base_speed + (self.level - 1) * 2)
        
        # Tambah obstacle tiap 2 level
        if self.level % 2 == 0:
            self.max_obstacles = min(15, (self.level // 2) * 3)
            while len(self.obstacles) < self.max_obstacles:
                self.obstacles.append(self.spawn_obstacle())
        
        # Spawn enemy di level 3
        if self.level == 3 and not self.enemy_enabled:
            self.enemy_enabled = True
            self.spawn_enemy_snake()
        
        # Bikin efek partikel level up yang keren
        for i in range(50):
            particle = {
                'x': self.snake_pos[0] + UKURAN_KOTAK//2,
                'y': self.snake_pos[1] + UKURAN_KOTAK//2,
                'dx': random.randint(-8, 8),
                'dy': random.randint(-8, 8),
                'life': 50,
                'color': random.choice([KUNING_NEON, UNGU_NEON, BIRU_NEON])
            }
            self.level_up_particles.append(particle)
    
    def update_ai_enemy(self):
        # AI enemy snake bergerak pake greedy best-first (chase player)
        if not self.enemy_snake or not self.enemy_enabled:
            return
        
        enemy_pos = self.enemy_snake['pos']
        target = self.snake_pos  # target player
        
        # Hitung jarak ke player
        dx = target[0] - enemy_pos[0]
        dy = target[1] - enemy_pos[1]
        
        # Pilih arah yang paling deket ke player
        possible_moves = []
        
        if abs(dx) > abs(dy):
            if dx > 0:
                possible_moves.append('RIGHT')
            elif dx < 0:
                possible_moves.append('LEFT')
            if dy > 0:
                possible_moves.append('DOWN')
            elif dy < 0:
                possible_moves.append('UP')
        else:
            if dy > 0:
                possible_moves.append('DOWN')
            elif dy < 0:
                possible_moves.append('UP')
            if dx > 0:
                possible_moves.append('RIGHT')
            elif dx < 0:
                possible_moves.append('LEFT')
        
        # Coba gerakan, hindari badan sendiri dan obstacle
        for move in possible_moves:
            test_pos = list(enemy_pos)
            if move == 'UP':
                test_pos[1] -= UKURAN_KOTAK
            elif move == 'DOWN':
                test_pos[1] += UKURAN_KOTAK
            elif move == 'LEFT':
                test_pos[0] -= UKURAN_KOTAK
            elif move == 'RIGHT':
                test_pos[0] += UKURAN_KOTAK
            
            # Cek apakah gerakan aman
            if (0 <= test_pos[0] < LEBAR and 0 <= test_pos[1] < TINGGI and
                test_pos not in self.enemy_snake['body'][:-1] and
                test_pos not in self.obstacles):
                self.enemy_snake['direction'] = move
                break
        
        # Gerakkan enemy
        direction = self.enemy_snake['direction']
        if direction == 'UP':
            enemy_pos[1] -= UKURAN_KOTAK
        elif direction == 'DOWN':
            enemy_pos[1] += UKURAN_KOTAK
        elif direction == 'LEFT':
            enemy_pos[0] -= UKURAN_KOTAK
        elif direction == 'RIGHT':
            enemy_pos[0] += UKURAN_KOTAK
        
        # Update body enemy
        self.enemy_snake['body'].insert(0, list(enemy_pos))
        
        # Enemy gak makan makanan, jadi panjangnya tetap
        if len(self.enemy_snake['body']) > 5:  # enemy max length
            self.enemy_snake['body'].pop()
    
    def update_powerups(self):
        # Update timer power-up
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
        
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
        
        # Spawn power-up random
        self.powerup_timer += 1
        if self.powerup_timer > 300 and len(self.powerups) < 2 and random.random() < 0.02:
            self.powerups.append(self.spawn_powerup())
            self.powerup_timer = 0
        
        # Update timer tiap power-up
        for powerup in self.powerups[:]:
            powerup['timer'] -= 1
            if powerup['timer'] <= 0:
                self.powerups.remove(powerup)
        
        # Cek collision dengan power-up
        for powerup in self.powerups[:]:
            if (self.snake_pos[0] == powerup['pos'][0] and 
                self.snake_pos[1] == powerup['pos'][1]):
                if powerup['type'] == 'shield':
                    self.shield_active = True
                    self.shield_timer = 200
                elif powerup['type'] == 'speed':
                    self.speed_boost_active = True
                    self.speed_boost_timer = 150
                
                # Efek partikel ambil power-up
                self.create_powerup_particles(powerup['pos'], powerup['type'])
                self.powerups.remove(powerup)
                self.score += 20
    
    def update_combo(self):
        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo = 0
    
    def create_eat_particles(self):
        # Bikin efek partikel waktu makan
        for i in range(10):
            particle = {
                'x': self.food_pos[0] + UKURAN_KOTAK//2,
                'y': self.food_pos[1] + UKURAN_KOTAK//2,
                'dx': random.randint(-5, 5),
                'dy': random.randint(-5, 5),
                'life': 30,
                'color': random.choice([KUNING_NEON, MERAH_NEON, BIRU_NEON])
            }
            self.particles.append(particle)
    
    def create_powerup_particles(self, pos, powerup_type):
        # Bikin efek partikel waktu ambil power-up
        color = BIRU_NEON if powerup_type == 'shield' else KUNING_NEON
        for i in range(20):
            particle = {
                'x': pos[0] + UKURAN_KOTAK//2,
                'y': pos[1] + UKURAN_KOTAK//2,
                'dx': random.randint(-7, 7),
                'dy': random.randint(-7, 7),
                'life': 40,
                'color': color
            }
            self.particles.append(particle)
    
    def update_particles(self):
        # Update partikel efek
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Update level up particles
        for particle in self.level_up_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.level_up_particles.remove(particle)
        
        # Update enemy particles
        for particle in self.enemy_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.enemy_particles.remove(particle)
    
    def check_collision(self):
        # Cek tabrakan dengan dinding (kalau gak ada shield)
        if (self.snake_pos[0] < 0 or self.snake_pos[0] >= LEBAR or 
            self.snake_pos[1] < 0 or self.snake_pos[1] >= TINGGI):
            if not self.shield_active:
                self.game_over = True
            else:
                # Shield melindungi, tapi langsung habis
                self.shield_active = False
                self.shield_timer = 0
        
        # Cek tabrakan dengan badan sendiri
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                if not self.shield_active:
                    self.game_over = True
                else:
                    self.shield_active = False
                    self.shield_timer = 0
        
        # Cek tabrakan dengan obstacle
        if self.snake_pos in self.obstacles:
            if not self.shield_active:
                self.game_over = True
            else:
                # Shield hancurin obstacle
                self.obstacles.remove(self.snake_pos)
                self.shield_active = False
                self.shield_timer = 0
        
        # Cek tabrakan dengan enemy snake
        if self.enemy_snake and self.snake_pos in self.enemy_snake['body']:
            if not self.shield_active:
                self.game_over = True
            else:
                # Bunuh enemy kalau ada shield
                self.enemy_snake = None
                self.enemy_enabled = False
                self.shield_active = False
                self.shield_timer = 0
                self.score += 100  # bonus bunuh enemy
    
    def draw_snake(self):
        # Gambar snake dengan efek gradient
        for i, pos in enumerate(self.snake_body):
            # Bikin efek fade dari kepala ke ekor
            alpha = max(50, 255 - (i * 10))
            alpha = min(255, alpha)
            
            if i == 0:  # Kepala snake
                # Bikin kepala lebih besar dan beda warna
                snake_color = HIJAU_NEON
                
                # Kalau ada shield, warna biru
                if self.shield_active:
                    snake_color = BIRU_NEON
                # Kalau speed boost, warna kuning
                elif self.speed_boost_active:
                    snake_color = KUNING_NEON
                
                pygame.draw.rect(layar, snake_color, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK))
                pygame.draw.rect(layar, PUTIH, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK), 2)
                
                # Mata snake
                eye_size = 3
                eye1_x = pos[0] + 5
                eye1_y = pos[1] + 5
                eye2_x = pos[0] + 15
                eye2_y = pos[1] + 5
                pygame.draw.circle(layar, HITAM, (eye1_x, eye1_y), eye_size)
                pygame.draw.circle(layar, HITAM, (eye2_x, eye2_y), eye_size)
                
                # Shield glow effect
                if self.shield_active:
                    glow_size = int(time.time() * 10) % 10
                    pygame.draw.rect(layar, (50, 150, 255), 
                                   pygame.Rect(pos[0] - glow_size, pos[1] - glow_size, 
                                             UKURAN_KOTAK + glow_size*2, UKURAN_KOTAK + glow_size*2), 2)
            else:  # Badan snake
                # Gradient effect buat badan
                green_val = max(20, 255 - (i * 15))
                color = (0, green_val, 0)
                
                if self.shield_active:
                    color = (0, green_val // 2, green_val)
                elif self.speed_boost_active:
                    color = (green_val, green_val, 0)
                
                pygame.draw.rect(layar, color, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK))
                pygame.draw.rect(layar, HIJAU_NEON, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK), 1)
    
    def draw_enemy_snake(self):
        # Gambar AI enemy snake
        if not self.enemy_snake:
            return
        
        for i, pos in enumerate(self.enemy_snake['body']):
            if i == 0:  # Kepala enemy
                pygame.draw.rect(layar, MERAH_NEON, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK))
                pygame.draw.rect(layar, PUTIH, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK), 2)
                
                # Mata enemy (merah)
                eye_size = 3
                pygame.draw.circle(layar, (255, 0, 0), (pos[0] + 5, pos[1] + 5), eye_size)
                pygame.draw.circle(layar, (255, 0, 0), (pos[0] + 15, pos[1] + 5), eye_size)
            else:
                # Badan enemy dengan gradient merah
                red_val = max(50, 255 - (i * 20))
                color = (red_val, 0, 0)
                pygame.draw.rect(layar, color, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK))
                pygame.draw.rect(layar, MERAH_NEON, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK), 1)
    
    def draw_obstacles(self):
        # Gambar obstacle dengan efek glow ungu
        pulse = int(time.time() * 5) % 10
        for obs in self.obstacles:
            # Obstacle utama
            pygame.draw.rect(layar, UNGU_NEON, 
                           pygame.Rect(obs[0], obs[1], UKURAN_KOTAK, UKURAN_KOTAK))
            
            # Glow effect
            glow_color = (100 + pulse * 10, 0, 100 + pulse * 10)
            pygame.draw.rect(layar, glow_color, 
                           pygame.Rect(obs[0] - 2, obs[1] - 2, UKURAN_KOTAK + 4, UKURAN_KOTAK + 4), 2)
    
    def draw_powerups(self):
        # Gambar power-up dengan animasi rotating
        rotation = int(time.time() * 100) % 360
        
        for powerup in self.powerups:
            pos = powerup['pos']
            ptype = powerup['type']
            
            # Warna sesuai tipe
            color = BIRU_NEON if ptype == 'shield' else KUNING_NEON
            
            # Animasi pulse
            pulse = int(time.time() * 10) % 20
            size_offset = pulse // 5
            
            # Gambar bentuk diamond (rotated square)
            center_x = pos[0] + UKURAN_KOTAK // 2
            center_y = pos[1] + UKURAN_KOTAK // 2
            size = UKURAN_KOTAK // 2 + size_offset
            
            points = [
                (center_x, center_y - size),
                (center_x + size, center_y),
                (center_x, center_y + size),
                (center_x - size, center_y)
            ]
            
            pygame.draw.polygon(layar, color, points)
            pygame.draw.polygon(layar, PUTIH, points, 2)
            
            # Glow effect
            glow_size = size + 5
            glow_points = [
                (center_x, center_y - glow_size),
                (center_x + glow_size, center_y),
                (center_x, center_y + glow_size),
                (center_x - glow_size, center_y)
            ]
            glow_color = (color[0]//3, color[1]//3, color[2]//3)
            pygame.draw.polygon(layar, glow_color, glow_points, 1)
    
    def draw_food(self):
        # Gambar makanan dengan animasi berkedip
        pulse = int(time.time() * 10) % 20
        size_offset = pulse // 10
        
        food_rect = pygame.Rect(self.food_pos[0] - size_offset, 
                               self.food_pos[1] - size_offset,
                               UKURAN_KOTAK + (size_offset * 2), 
                               UKURAN_KOTAK + (size_offset * 2))
        
        pygame.draw.ellipse(layar, MERAH_NEON, food_rect)
        pygame.draw.ellipse(layar, PUTIH, food_rect, 2)
        
        # Efek glow
        glow_rect = pygame.Rect(self.food_pos[0] - 2, self.food_pos[1] - 2,
                               UKURAN_KOTAK + 4, UKURAN_KOTAK + 4)
        pygame.draw.ellipse(layar, (100, 0, 0), glow_rect)
    
    def draw_particles(self):
        # Gambar partikel efek
        for particle in self.particles:
            size = max(1, particle['life'] // 5)
            pygame.draw.circle(layar, particle['color'], 
                             (int(particle['x']), int(particle['y'])), size)
        
        # Gambar level up particles
        for particle in self.level_up_particles:
            size = max(2, particle['life'] // 8)
            pygame.draw.circle(layar, particle['color'], 
                             (int(particle['x']), int(particle['y'])), size)
        
        # Gambar enemy particles
        for particle in self.enemy_particles:
            size = max(1, particle['life'] // 6)
            pygame.draw.circle(layar, particle['color'], 
                             (int(particle['x']), int(particle['y'])), size)
    
    def draw_ui(self):
        # Background semi transparan buat UI
        ui_surface = pygame.Surface((LEBAR, 60))
        ui_surface.set_alpha(150)
        ui_surface.fill(HITAM)
        layar.blit(ui_surface, (0, 0))
        
        # Score
        score_text = font_sedang.render(f"Score: {self.score}", True, HIJAU_NEON)
        layar.blit(score_text, (20, 15))
        
        # Level dengan warna yang berubah tiap level
        level_colors = [HIJAU_NEON, BIRU_NEON, KUNING_NEON, MERAH_NEON, UNGU_NEON]
        level_color = level_colors[(self.level - 1) % len(level_colors)]
        level_text = font_sedang.render(f"Lv.{self.level}", True, level_color)
        layar.blit(level_text, (200, 15))
        
        # Combo meter
        if self.combo > 0:
            combo_text = font_kecil.render(f"COMBO x{self.combo}!", True, KUNING_NEON)
            layar.blit(combo_text, (300, 20))
        
        # Power-up indicators
        x_offset = 420
        if self.shield_active:
            shield_text = font_kecil.render(f"SHIELD {self.shield_timer//10}", True, BIRU_NEON)
            layar.blit(shield_text, (x_offset, 20))
            x_offset += 120
        
        if self.speed_boost_active:
            speed_text = font_kecil.render(f"SPEED {self.speed_boost_timer//10}", True, KUNING_NEON)
            layar.blit(speed_text, (x_offset, 20))
        
        # FPS
        fps = int(jam.get_fps())
        fps_text = font_kecil.render(f"FPS: {fps}", True, BIRU_NEON)
        layar.blit(fps_text, (LEBAR - 80, 5))
        
        # Snake length
        length_text = font_kecil.render(f"Len: {len(self.snake_body)}", True, UNGU_NEON)
        layar.blit(length_text, (LEBAR - 80, 30))
    
    def draw_grid(self):
        # Gambar grid tipis buat bantuan visual
        for x in range(0, LEBAR, UKURAN_KOTAK):
            pygame.draw.line(layar, (20, 20, 20), (x, 0), (x, TINGGI))
        for y in range(0, TINGGI, UKURAN_KOTAK):
            pygame.draw.line(layar, (20, 20, 20), (0, y), (LEBAR, y))
    
    def show_game_over(self):
        # Overlay gelap
        overlay = pygame.Surface((LEBAR, TINGGI))
        overlay.set_alpha(180)
        overlay.fill(HITAM)
        layar.blit(overlay, (0, 0))
        
        # Text Game Over
        game_over_text = font_besar.render("GAME OVER!", True, MERAH_NEON)
        text_rect = game_over_text.get_rect(center=(LEBAR//2, TINGGI//2 - 120))
        layar.blit(game_over_text, text_rect)
        
        # Final Score
        final_score_text = font_sedang.render(f"Final Score: {self.score}", True, PUTIH)
        text_rect2 = final_score_text.get_rect(center=(LEBAR//2, TINGGI//2 - 70))
        layar.blit(final_score_text, text_rect2)
        
        # Level reached
        level_text = font_sedang.render(f"Level Reached: {self.level}", True, BIRU_NEON)
        text_rect_level = level_text.get_rect(center=(LEBAR//2, TINGGI//2 - 40))
        layar.blit(level_text, text_rect_level)
        
        # Max combo
        if self.max_combo > 0:
            combo_text = font_sedang.render(f"Max Combo: x{self.max_combo}", True, KUNING_NEON)
            text_rect_combo = combo_text.get_rect(center=(LEBAR//2, TINGGI//2 - 10))
            layar.blit(combo_text, text_rect_combo)
        
        # High Score
        if self.score > self.high_score:
            new_high_text = font_sedang.render("NEW HIGH SCORE!", True, KUNING_NEON)
            text_rect3 = new_high_text.get_rect(center=(LEBAR//2, TINGGI//2 + 30))
            layar.blit(new_high_text, text_rect3)
        else:
            high_text = font_sedang.render(f"High Score: {self.high_score}", True, HIJAU_NEON)
            text_rect3 = high_text.get_rect(center=(LEBAR//2, TINGGI//2 + 30))
            layar.blit(high_text, text_rect3)
        
        # Instructions
        restart_text = font_kecil.render("Press R to restart or Q to quit", True, BIRU_NEON)
        text_rect4 = restart_text.get_rect(center=(LEBAR//2, TINGGI//2 + 70))
        layar.blit(restart_text, text_rect4)
    
    def show_pause(self):
        # Overlay pause
        overlay = pygame.Surface((LEBAR, TINGGI))
        overlay.set_alpha(150)
        overlay.fill(HITAM)
        layar.blit(overlay, (0, 0))
        
        pause_text = font_besar.render("PAUSED", True, KUNING_NEON)
        text_rect = pause_text.get_rect(center=(LEBAR//2, TINGGI//2))
        layar.blit(pause_text, text_rect)
        
        continue_text = font_sedang.render("Press SPACE to continue", True, PUTIH)
        text_rect2 = continue_text.get_rect(center=(LEBAR//2, TINGGI//2 + 50))
        layar.blit(continue_text, text_rect2)
    
    def reset_game(self):
        # Reset semua variable game
        if self.score > self.high_score:
            self.high_score = self.score
        
        # Reset posisi snake sesuai grid yang benar
        self.snake_pos = [100, 80]
        self.snake_body = [[100, 80], [80, 80], [60, 80]]
        self.food_pos = self.spawn_food()
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.game_over = False
        self.particles = []
        
        # Reset level dan difficulty
        self.level = 1
        self.current_speed = self.base_speed
        self.obstacles = []
        self.max_obstacles = 0
        
        # Reset power-ups
        self.powerups = []
        self.powerup_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        
        # Reset combo
        self.combo = 0
        self.combo_timer = 0
        self.max_combo = 0
        
        # Reset enemy
        self.enemy_snake = None
        self.enemy_enabled = False
        self.enemy_particles = []
        self.level_up_particles = []
    
    def run(self):
        # Main game loop
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Handle pause first - bisa dipause kapan aja (kecuali game over)
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.pause = not self.pause
                    
                    # Movement controls - cuma bisa gerak kalau game gak over dan gak pause
                    elif not self.game_over and not self.pause:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.change_to = 'UP'
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.change_to = 'DOWN'
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.change_to = 'LEFT'
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.change_to = 'RIGHT'
                    
                    # Game over controls
                    elif self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_q:
                            running = False
            
            if not self.game_over and not self.pause:
                # Update game logic
                self.update_direction()
                self.move_snake()
                self.update_ai_enemy()
                self.update_powerups()
                self.update_combo()
                self.check_collision()
                self.update_particles()
            
            # Clear screen dengan gradient background
            layar.fill(HITAM)
            
            # Gambar grid
            self.draw_grid()
            
            # Gambar game elements
            if not self.game_over:
                self.draw_obstacles()
                self.draw_powerups()
                self.draw_food()
                self.draw_enemy_snake()
                self.draw_snake()
                self.draw_particles()
                
                if self.pause:
                    self.show_pause()
            else:
                # Masih gambar semua objek pas game over
                self.draw_obstacles()
                self.draw_food()
                self.draw_enemy_snake()
                self.draw_snake()
                self.show_game_over()
            
            # Gambar UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            
            # Speed dinamis - speed boost bikin 2x lebih cepat
            actual_speed = self.current_speed
            if self.speed_boost_active:
                actual_speed = int(self.current_speed * 1.5)
            
            jam.tick(actual_speed)  # FPS game (makin tinggi makin cepet)
        
        pygame.quit()
        sys.exit()

# Jalankan game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
