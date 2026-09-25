# GUI Plan

## Framework
- PySide6

## Layout
- Split View (Kiri-Kanan)
- Kiri 40%: Info + Options + Actions
- Kanan 60%: Progress + Log + Status
- QSplitter untuk resize

## Fitur MVP
- Input URL + Fetch Info
- Tampilkan metadata (thumbnail, judul, uploader, durasi)
- Pilih Video / Audio Only
- Format video: mp4, webm, mkv, mov, avi, wmv
- Format audio: mp3, m4a, opus, ogg, flac, wav
- Quality selector dinamis (lossy pakai kbps, lossless pakai bit depth)
- Progress bar real-time
- Log panel
- Threading (QThread) agar UI tidak freeze

## Format & Quality Matrix

### Video
| Format | Native? |
|--------|---------|
| mp4 | ✅ |
| webm | ✅ |
| mkv, mov, avi, wmv | Convert |

### Video Quality
144p, 240p, 360p, 480p, 720p, 1080p, 2K, 4K

### Audio — Lossy (kbps)
| Format | Options |
|--------|---------|
| mp3 | 96, 160, 256, 320 |
| m4a | 96, 128, 192, 256 |
| opus | 96, 160, 256, 320 |
| ogg | 96, 160, 256, 320 |

### Audio — Lossless (bit/sample rate)
| Format | Options |
|--------|---------|
| flac | 16/44.1, 24/48, 24/96 |
| wav | 16/44.1, 24/48, 24/96 |

### Badges
- 🟢 Best match (native, no re-encode)
- 🟡 Re-encode (sedikit penurunan)
- 🔵 Lossless (file besar, no loss)

## Struktur File

src/ytdl/gui/
├── init.py
├── app.py
├── main_window.py
├── workers.py
└── widgets/
├── init.py
├── url_bar.py
├── info_panel.py
├── options_panel.py
├── progress_panel.py
└── log_panel.py


## Roadmap
- GUI-1: setup + window kosong
- GUI-2: layout & widget statis
- GUI-3: integrasi core (fetch info)
- GUI-4: threading & download
- GUI-5: audio/video mode switch
- GUI-6: polish

## Notes
- Source YouTube lossy (~160 kbps Opus / ~128 kbps AAC)
- Convert ke FLAC/WAV = upsampling, bukan peningkatan kualitas
- File lossless bisa 50-100x lebih besar dari MP3