# Galaxy Lancer

A vertical-scrolling space shooter built with Python and Pygame. Pilot a starship through waves of enemies and defeat the final boss across four difficulty levels.

## Features

- 4 difficulty modes: **EASY / NORMAL / HARD / FEARFUL**
- Two control schemes: keyboard (single player) or Joy-Con joystick (2 players)
- 5 enemy types with distinct movement patterns
- Multi-phase boss fight with escalating attack patterns
- Barrage special attack that trades shield for firepower
- Score multiplier based on selected difficulty

## Requirements

- Python 3.x
- pygame 2.6.1

```bash
pip install -r requirement.txt
```

## How to Run

**Keyboard (single player):**
```bash
python galaxy_lancer_KeyBoard.py
```

**Joy-Con / Joystick (2 players):**
```bash
python galaxy_lancer_JoyStick.py
```

> Connect all Joy-Con controllers **before** launching the joystick version. The game exits immediately if the controller count does not match the expected player count.

## Controls

### Keyboard

| Action | Key |
|---|---|
| Move | Arrow keys or WASD |
| Shoot | Space |
| Barrage (costs 10 shield) | Z |

### Joystick (Joy-Con)

| Action | Input |
|---|---|
| Move | Left stick |
| Shoot | Right trigger / button |
| Barrage | Bottom button |

> For 2-player mode, both players must connect the same type of Joy-Con (both left or both right).

## Gameplay

1. **Mode select** — Use Up/Down (or W/S) to choose difficulty, then press Space/Enter to confirm.
2. **Title screen** — Press Space to start.
3. **In game** — Survive enemy waves for 65 seconds, then face the boss.
4. **Boss** — Has a shield bar. At 25% HP remaining the boss moves to the center and enters a final attack phase.

### Shield System

- Your ship starts with **100 shield**.
- Taking damage from enemies or bullets reduces shield.
- Destroying non-boss enemies restores **1 shield** per kill.
- Using the barrage attack costs **10 shield** (minimum 10 required).
- Shield reaches 0 → **GAME OVER**.

### Scoring

| Event | Base Score |
|---|---|
| Enemy destroyed | 100 × (difficulty + 1) |
| Boss defeated | 10,000 × (difficulty + 1) |

Difficulty multipliers: EASY ×1, NORMAL ×2, HARD ×3, FEARFUL ×4.

## Difficulty Differences

| Mode | Player Speed | Background Speed | Enemy Spawn Rate | Boss HP |
|---|---|---|---|---|
| EASY | 25 | 10 | Lowest | 100 |
| NORMAL | 22 | 13 | Normal | 150 |
| HARD | 19 | 16 | High | 200 |
| FEARFUL | 16 | 22 | Highest | 250 |

## Project Structure

```
galaxy_lancer/
├── galaxy_lancer_KeyBoard.py   # Single-player keyboard version
├── galaxy_lancer_JoyStick.py   # 2-player Joy-Con version
├── requirement.txt
└── source/
    ├── image_gl/               # Sprites and backgrounds
    └── sound_gl/               # BGM and sound effects
```

## Credits

- **Kevin** — Development
- **Family** — Playtesting and feedback
