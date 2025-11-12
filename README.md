# Naver Sneaky Game

[![Workflow Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![License](https://img.shields.io/badge/license-Non--Commercial-blue.svg)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](#)

<p align="center">
  <img src="Screenshot 2025-11-12 225056.png" height="320px" alt="Naver Sneaky Game"/>
</p>

## Tentang

`Naver Sneaky Game` adalah implementasi permainan Snake sederhana yang dibuat dengan Python dan Pygame.
Tujuan proyek ini adalah sebagai latihan pemrograman dan demo efek visual (particle, glow, gradient).

Fitur utama:
- Kontrol WASD / panah untuk bergerak
- Efek partikel saat memakan makanan
- UI sederhana dengan skor, high-score, FPS dan panjang snake
- Pause (SPACE), restart (R) dan quit (Q)


## Cara memulai (Windows — PowerShell)

1. Pastikan Python 3.8+ terpasang dan dapat diakses di PATH.
2. Disarankan buat virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

3. Pasang dependensi (Pygame):

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

- Panah atas / W — Bergerak ke atas
- Panah bawah / S — Bergerak ke bawah
- Panah kiri / A — Bergerak ke kiri
- Panah kanan / D — Bergerak ke kanan
- SPACE — Pause / resume
- R — Restart (setelah game over)
- Q — Quit

## Pengembangan & Kontribusi

Kami menerima kontribusi kecil seperti:

- Perbaikan bug pada logika gerakan dan collision
- Penambahan fitur (level, power-up, multiple food types)
- Menambahkan test sederhana dan CI

Langkah singkat untuk berkontribusi:

1. Fork repositori
2. Buat branch fitur (`git checkout -b feat/nama-fitur`)
3. Tambahkan perubahan dengan deskripsi jelas
4. Buka Pull Request dan jelaskan tujuan perubahan

Untuk issue pertama, coba perbaikan kecil untuk `README.md` atau perbaiki teks/typo di `snake-game.py`.

## Testing singkat

Proyek ini tidak menyertakan test otomatis. Untuk pengujian manual:

- Pastikan game bisa berjalan tanpa crash selama 1-2 menit
- Coba konsumsi beberapa makanan untuk melihat efek partikel
- Verifikasi kontrol dan restart/pause

## Catatan pengembang

- File utama: `snake-game.py`
- Game menggunakan grid berukuran 20px untuk posisi objek

## Terima kasih

Terima kasih sudah melihat proyek ini — semoga bermanfaat untuk belajar Python dan Pygame!