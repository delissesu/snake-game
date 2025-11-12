# Naver Sneaky Game

[![Workflow Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![License](https://img.shields.io/badge/license-Non--Commercial-blue.svg)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](#)

<p align="center">
  <img src="images\preview.png" height="320px" alt="Naver Sneaky Game"/>
</p>
<br>
<p align="center">
  <img src="images\preview-2.png" height="320px" alt="Naver Sneaky Game"/>
</p>

## Tentang

`Naver Sneaky Game v2.0` adalah game Snake yang aku buat dengan Pygame dengan berbagai fitur dan vfx yang keren.

Tujuan dibuatnya game ini adalah sebagai latihanku yang sedang belajar pada algoritma game, AI pathfinding, dan demo vfx (particle, glow, gradient).

### Fitur utama:

**Gameplay:**
- Kontrol WASD / panah untuk bergerak
- Sistem Level Progresif — speed dan difficulty naik otomatis tiap 50 skor
- Combo System — makan makanan berturut-turut = bonus skor dengan multiplier
- Power-up (Shield & Speed Boost) dengan efek visual rotating diamond
- Obstacle dinamis yang spawn seiring level naik (tembok ungu dengan glow effect)
- AI Enemy Snake dengan algoritma pathfinding greedy best-first (muncul di level 3)

**Visual Effects:**
- Efek partikel saat memakan makanan, ambil power-up, dan level up
- Gradient color pada snake body dengan fade effect
- Glow effect pada makanan, obstacle, dan power-up
- Shield glow animation saat aktif
- UI dinamis dengan warna berubah setiap level
- Grid background untuk bantuan visual

**Game Mechanics:**
- Shield melindungi dari tabrakan (dinding, badan sendiri, obstacle, enemy)
- Speed Boost meningkatkan kecepatan 1.5x
- Obstacle bertambah tiap 2 level
- AI Enemy mengejar player menggunakan greedy algorithm
- Combo timer 60 frames — harus makan cepat untuk maintain combo


## Cara memulai (Windows — PowerShell)

1. Pastikan Python 3.8+ terpasang dan dapat diakses di PATH.
2. Disarankan buat virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

3. Pasang dependensi (Pygame):

```powershell
pip install -r requirements.txt
```

Atau manual:

```powershell
python -m pip install --upgrade pip; pip install pygame
```

4. Jalankan game:

```powershell
python "snake-game.py"
```

Jika kamu menemui error yang berhubungan dengan tampilan atau mixer audio, pastikan driver grafis sudah terpasang
dan coba jalankan dari terminal biasa (bukan melalui editor) untuk melihat pesan error lengkap.

## Kontrol

- **Panah atas / W** — Bergerak ke atas
- **Panah bawah / S** — Bergerak ke bawah
- **Panah kiri / A** — Bergerak ke kiri
- **Panah kanan / D** — Bergerak ke kanan
- **SPACE** — Pause / resume
- **R** — Restart (setelah game over)
- **Q** — Quit

## Gameplay Tips

1. **Level Up Strategy:** Tiap 50 skor = naik level. Speed bertambah, obstacle spawn lebih banyak.
2. **Combo System:** Makan makanan berturut-turut dalam 60 frames untuk bonus skor (combo x5 per level).
3. **Power-up Priority:** 
   - **Shield (biru)** — Melindungi dari 1x tabrakan (dinding, obstacle, enemy, badan sendiri)
   - **Speed Boost (kuning)** — 1.5x kecepatan selama 15 detik
4. **AI Enemy:** Muncul di level 3, mengejar player dengan pathfinding. Gunakan shield untuk bunuh enemy (+100 skor).
5. **Obstacle Avoidance:** Tembok ungu spawn tiap 2 level. Bisa dihancurkan dengan shield.
6. **Max Combo Challenge:** Coba pertahankan combo setinggi mungkin untuk high score!

## Pengembangan & Kontribusi

Kami menerima kontribusi seperti:

- Perbaikan bug pada logika gerakan, collision, dan AI pathfinding
- Penambahan fitur (leaderboard online, multiple enemy types, boss fight)
- Optimasi performa (spatial partitioning untuk collision detection)
- Menambahkan test otomatis dan CI/CD pipeline
- Sound effects dan background music
- Multiplayer mode (split screen atau online)

### Ingin berkontribusi?:

1. Fork repositori
2. Buat branch fitur (`git checkout -b feat/nama-fitur`)
3. Tambahkan perubahan dengan deskripsi jelas
4. Buka Pull Request dan jelaskan tujuan perubahan

Untuk issue pertama, coba:
- Perbaikan typo di `README.md` atau komentar di `snake-game.py`
- Tweak nilai difficulty (speed, obstacle count, enemy spawn level)
- Tambah warna tema baru untuk level tertentu

## Testing

Proyek ini tidak menyertakan test otomatis. Untuk pengujian manual:

- Pastikan game bisa berjalan tanpa crash selama 5+ menit
- Test semua power-up (shield, speed boost) dan verifikasi efeknya
- Coba capai level 3+ untuk trigger AI enemy spawn
- Verifikasi combo system bekerja (skor bonus muncul)
- Test collision dengan obstacle, enemy, dan dinding
- Pastikan shield melindungi dari semua jenis collision
- Verifikasi level up animation dan speed increase
- Test pause/resume dan restart functionality

### Checklist Testing:
- [ ] Game berjalan tanpa error
- [ ] Level system meningkatkan speed dan obstacle
- [ ] AI enemy muncul di level 3 dan mengejar player
- [ ] Power-up spawn random dan berfungsi
- [ ] Combo multiplier bekerja dengan benar
- [ ] Shield melindungi dari collision
- [ ] Speed boost meningkatkan kecepatan
- [ ] UI menampilkan info yang benar (level, combo, power-up timer)
- [ ] Particle effects muncul saat event tertentu
- [ ] Game over screen menampilkan stats lengkap

## Catatan pengembang

### Struktur Kode
- File utama: `snake-game.py`
- Game menggunakan grid berukuran 20px untuk posisi objek
- FPS base: 8 (meningkat seiring level sampai max 20)
- Speed boost multiplier: 1.5x

### Algoritma & Sistem

**Level Progression:**
- Level = (Score // 50) + 1
- Speed = base_speed + (level - 1) * 2 (max 20)
- Obstacle count = (level // 2) * 3 (max 15)
- Enemy spawn: Level 3

**AI Enemy Pathfinding:**
- Algoritma: Greedy Best-First Search
- Target: Player head position
- Avoidance: Dinding, badan sendiri, obstacle
- Max length: 5 segments (tidak bertambah)

**Combo System:**
- Timer: 60 frames per combo
- Bonus: combo_level * 5 skor
- Reset saat timer habis

**Power-up Spawn:**
- Check interval: 300 frames
- Spawn chance: 2% per frame setelah interval
- Max active: 2 power-up
- Lifetime: 300 frames sebelum hilang
- Types: Shield (200 frames), Speed (150 frames)

**Collision Detection:**
- Snake vs Wall
- Snake vs Self
- Snake vs Obstacle
- Snake vs Enemy
- Snake vs Food
- Snake vs Power-up

### Color Palette
```python
HIJAU_NEON = (57, 255, 20)    # Player snake
MERAH_NEON = (255, 20, 147)   # Food & Enemy
BIRU_NEON = (20, 191, 255)    # Shield & UI
KUNING_NEON = (255, 255, 20)  # Speed boost & Combo
UNGU_NEON = (191, 20, 255)    # Obstacle
```

### Performance Notes
- Particle system dibatasi lifetime untuk avoid memory leak
- Enemy AI hanya update 1x per frame (tidak perlu optimization lebih lanjut untuk single enemy)
- Collision detection O(n) di mana n = panjang snake (acceptable untuk gameplay normal)
- Future optimization: spatial grid untuk collision jika ada banyak entity

## Terima kasih

Terima kasih sudah melihat proyek ini — semoga bermanfaat untuk belajar Python dan Pygame!