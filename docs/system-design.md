# Design Notes: PySide6

## Source of Truth
- YAML frontmatter di design-system.md = source of truth
- Ignore inconsistencies di prose

## Qt Implementation Strategy
- **Warna**: Via QSS `background-color`, `color`, `border-color`
- **Typography**: Via `QFont` (load Plus Jakarta Sans + JetBrains Mono)
- **Radius**: Via QSS `border-radius`
- **Elevation**: Via QSS `border` + simple `box-shadow` (not multi-layer)
- **Custom widgets**: Hanya untuk progress bar & log panel (opsional)

## Layout Final
- 2-pane (bukan 3-pane)
- Kiri (40%): URL bar + Info + Options + Actions
- Kanan (60%): Progress + Log + Status
- Window margin: 12px
- Gutter: 16px

## Font Requirements
- Plus Jakarta Sans: https://fonts.google.com/specimen/Plus+Jakarta+Sans
- JetBrains Mono: https://fonts.google.com/specimen/JetBrains+Mono
- (Akan di-bundle di `assets/fonts/`)

## Color Mapping (dari YAML → QSS variable)
Lihat tabel konversi di bawah.

| Design Token | YAML Value | QSS Use |
|--------------|-----------|---------|
| surface | #111319 | Window background |
| surface-container | #1d2025 | Panel background |
| surface-container-high | #272a30 | Elevated card |
| primary | #adc6ff | Button primary, focus |
| on-surface | #e1e2ea | Text primary |
| on-surface-variant | #c1c6d7 | Text secondary |
| error | #ffb4ab | Error message |
| outline | #8b90a0 | Border subtle |
| outline-variant | #414755 | Border divider |