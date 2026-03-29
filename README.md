# Poker Fate - Color Game Auto Bot

A Python script to automate the Color Game mini-game in Poker Fate. This bot utilizes screen recognition and HSV (Hue, Saturation, Value) color analysis for maximum accuracy, combined with the Martingale betting strategy.

## Key Features

* **Automated Gameplay:** Automatically places bets, spins the knob, and reads the results.
* **Martingale Strategy:** If you lose, it doubles the bet (Rebet + 2X). If you win, it resets to the base bet.
* **Dynamic Color Selection:** Randomly selects a new color to bet on every time a win occurs.
* **HSV Color Detection:** Reads the ball results from the screen by converting RGB values to HSV, making it highly resilient to in-game reflections and shadows.
* **Failsafe Mechanism:** Includes an emergency stop feature that triggers immediately when the user moves the mouse to the absolute top-left corner of the screen.

## Prerequisites & System Requirements

* Python 3.x or higher
* Required libraries:
  ```bash
  pip install pyautogui pygetwindow opencv-python Pillow
  ```
* **Required Resolution:** You MUST set your game window or display resolution to **800x600**. The bot calculates click coordinates based on this specific aspect ratio and size. It will not click accurately if the resolution is different.

## Directory Structure

For the bot to function correctly, your project folder structure should look like this:

```text
your_project_folder/
│
├── main.py                # Main bot script
└── img/                   # Folder containing reference images
    ├── casual_btn.png
    ├── color_game_title.png
    ├── chip_10000.png     # Or any other configured chip value
    ├── twist_btn.png
    ├── clear_btn.png
    ├── rebet_btn.png
    └── 2x_btn.png
```

## How to Use

1. Ensure your game or desktop resolution is set to **800x600**.
2. Launch Poker Fate and navigate to the Color Game screen.
3. Open a Terminal or Command Prompt in your project folder.
4. Run the following command to start the bot:
   ```bash
   python main.py
   ```
5. The bot will automatically locate the "Poker Fate" game window and bring it to the foreground.
6. Let the bot run. Do not minimize the game window or let other windows overlap the game area.

## Configuration

You can customize the bot's behavior by modifying the variables in the `Settings` section of `main.py`:

* `CONFIDENCE_LEVEL`: Accuracy threshold for finding image buttons (Default is `0.85`).
* `MAX_WAIT_TIME`: Maximum time to wait for the ball results after spinning (Default is `7.0` seconds).
* `BASE_BET_DELAY`: Delay between each mouse click (Default is `0.5` seconds).
* `IMG_CHIP_BASE`: Filename of the base chip you want to bet with (e.g., `chip_1000.png` or `chip_10000.png`).

## Stopping the Bot

* **Method 1:** Quickly move your mouse cursor to the absolute top-left corner of your computer screen (Failsafe trigger).
* **Method 2:** Press `Ctrl + C` in the Terminal window where the script is running.

## Disclaimer

Using automated programs (Bots) may violate the game's terms of service. The developer of this script is not responsible for any account suspensions (Bans) or damages resulting from its use. Use it cautiously and at your own risk.
