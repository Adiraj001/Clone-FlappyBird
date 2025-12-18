# Flappy Bird 🐦🎮

## Overview

This is a **Python-based Flappy Bird game** developed using **Pygame**. Players control a bird, guiding it through obstacles while avoiding collisions to increase their score. The game features smooth controls, dynamic difficulty, engaging sound effects, and background music for an immersive experience.

## Features

* **Smooth controls** for precise gameplay
* **Dynamic obstacles** that increase challenge
* **Scoring system** to track progress
* **Adjustable speed** for different difficulty levels
* **Background music & sound effects** for engagement

## Requirements

Ensure you have the following dependencies installed:

* Python 3.x
* Pygame

You can install all dependencies via `requirements.txt` after creating a virtual environment.

## Installation & Setup

### 1. Clone the repository

### 2. Create a virtual environment (recommended)

```bash
conda create -n pygame python=3.13.5 -y
conda activate pygame
```


### 3. Activate the virtual environment

* **Windows:**

```bash
venv\Scripts\activate
```

* **macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies using `requirements.txt`

```bash
pip install -r requirements.txt
```

### 5. Run the game

```bash
python main.py
```

## How to Play

* Press **Space** or **Up Arrow** to make the bird flap.
* Navigate through the pipes without hitting them.
* Each successful pass increases your score.
* Press **'P'** to increase speed or **'O'** to reduce speed.
* Game over occurs if the bird collides with obstacles or the ground.

Enjoy the game and have fun! 🎉
