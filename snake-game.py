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
        
        # Posisi makanan random
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        
        # Arah gerakan snake
        self.direction = 'RIGHT'
        self.change_to = self.direction
        
        # Score dan game state
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.pause = False
        
        # Efek visual
        self.trail = []
        self.particles = []
        
    def spawn_food(self):
        # Spawn makanan di posisi random yang gak nabrak snake
        while True:
            # Pastikan koordinat sesuai dengan grid UKURAN_KOTAK
            x = random.randrange(0, (LEBAR//UKURAN_KOTAK)) * UKURAN_KOTAK
            y = random.randrange(3, (TINGGI//UKURAN_KOTAK)) * UKURAN_KOTAK  # mulai dari y=60 biar gak nabrak UI
            if [x, y] not in self.snake_body:
                return [x, y]
    
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
            self.score += 10
            self.food_spawn = False
            # Bikin partikel efek makan
            self.create_eat_particles()
        else:
            # Hapus ekor kalau gak makan makanan
            self.snake_body.pop()
        
        # Spawn makanan baru kalau udah dimakan
        if not self.food_spawn:
            self.food_pos = self.spawn_food()
            self.food_spawn = True
    
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
    
    def update_particles(self):
        # Update partikel efek
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def check_collision(self):
        # Cek tabrakan dengan dinding
        if (self.snake_pos[0] < 0 or self.snake_pos[0] >= LEBAR or 
            self.snake_pos[1] < 0 or self.snake_pos[1] >= TINGGI):
            self.game_over = True
        
        # Cek tabrakan dengan badan sendiri
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over = True
    
    def draw_snake(self):
        # Gambar snake dengan efek gradient
        for i, pos in enumerate(self.snake_body):
            # Bikin efek fade dari kepala ke ekor
            alpha = max(50, 255 - (i * 10))
            alpha = min(255, alpha)
            
            if i == 0:  # Kepala snake
                # Bikin kepala lebih besar dan beda warna
                pygame.draw.rect(layar, HIJAU_NEON, 
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
            else:  # Badan snake
                # Gradient effect buat badan
                green_val = max(20, 255 - (i * 15))
                color = (0, green_val, 0)
                pygame.draw.rect(layar, color, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK))
                pygame.draw.rect(layar, HIJAU_NEON, 
                               pygame.Rect(pos[0], pos[1], UKURAN_KOTAK, UKURAN_KOTAK), 1)
    
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
    
    def draw_ui(self):
        # Background semi transparan buat UI
        ui_surface = pygame.Surface((LEBAR, 60))
        ui_surface.set_alpha(150)
        ui_surface.fill(HITAM)
        layar.blit(ui_surface, (0, 0))
        
        # Score
        score_text = font_sedang.render(f"Score: {self.score}", True, HIJAU_NEON)
        layar.blit(score_text, (20, 15))
        
        # High Score
        high_score_text = font_sedang.render(f"High: {self.high_score}", True, KUNING_NEON)
        layar.blit(high_score_text, (200, 15))
        
        # FPS
        fps = int(jam.get_fps())
        fps_text = font_kecil.render(f"FPS: {fps}", True, BIRU_NEON)
        layar.blit(fps_text, (LEBAR - 80, 20))
        
        # Snake length
        length_text = font_kecil.render(f"Length: {len(self.snake_body)}", True, UNGU_NEON)
        layar.blit(length_text, (350, 20))
    
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
        text_rect = game_over_text.get_rect(center=(LEBAR//2, TINGGI//2 - 100))
        layar.blit(game_over_text, text_rect)
        
        # Final Score
        final_score_text = font_sedang.render(f"Final Score: {self.score}", True, PUTIH)
        text_rect2 = final_score_text.get_rect(center=(LEBAR//2, TINGGI//2 - 50))
        layar.blit(final_score_text, text_rect2)
        
        # High Score
        if self.score > self.high_score:
            new_high_text = font_sedang.render("NEW HIGH SCORE!", True, KUNING_NEON)
            text_rect3 = new_high_text.get_rect(center=(LEBAR//2, TINGGI//2))
            layar.blit(new_high_text, text_rect3)
        else:
            high_text = font_sedang.render(f"High Score: {self.high_score}", True, HIJAU_NEON)
            text_rect3 = high_text.get_rect(center=(LEBAR//2, TINGGI//2))
            layar.blit(high_text, text_rect3)
        
        # Instructions
        restart_text = font_kecil.render("Press R to restart or Q to quit", True, BIRU_NEON)
        text_rect4 = restart_text.get_rect(center=(LEBAR//2, TINGGI//2 + 50))
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
                self.check_collision()
                self.update_particles()
            
            # Clear screen dengan gradient background
            layar.fill(HITAM)
            
            # Gambar grid
            self.draw_grid()
            
            # Gambar game elements
            if not self.game_over:
                self.draw_food()
                self.draw_snake()
                self.draw_particles()
                
                if self.pause:
                    self.show_pause()
            else:
                # Masih gambar snake dan food pas game over
                self.draw_food()
                self.draw_snake()
                self.show_game_over()
            
            # Gambar UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            jam.tick(8)  # FPS game (makin tinggi makin cepet)
        
        pygame.quit()
        sys.exit()

# Jalankan game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
