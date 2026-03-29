import os
import random
import time
import colorsys
import pygetwindow as gw
import pyautogui
from PIL import ImageDraw

COLORS = ['blue', 'green', 'grey', 'pink', 'red', 'yellow'] 
CONFIDENCE_LEVEL = 0.85      
MAX_WAIT_TIME = 7.0          
BASE_BET_DELAY = 0.5         

IMG_DIR = 'img'

IMG_CASUAL_BTN = os.path.join(IMG_DIR, 'casual_btn.png')
IMG_COLOR_TITLE = os.path.join(IMG_DIR, 'color_game_title.png')
IMG_CHIP_BASE = os.path.join(IMG_DIR, 'chip_1000.png')
IMG_TWIST_BTN = os.path.join(IMG_DIR, 'twist_btn.png')
IMG_CLEAR_BTN = os.path.join(IMG_DIR, 'clear_btn.png')
IMG_REBET_BTN = os.path.join(IMG_DIR, 'rebet_btn.png')
IMG_2X_BTN = os.path.join(IMG_DIR, '2x_btn.png')

def get_game_window(title="Poker Fate"):
    try:
        windows = gw.getWindowsWithTitle(title)
        if not windows:
            return None
        win = windows[0]
        if not win.isActive:
            win.activate()
            time.sleep(0.5)
        return (win.left, win.top, win.width, win.height)
    except Exception as e:
        print(f"ไม่พบหน้าต่างเกม: {e}")
        return None

def find_and_click(img_path, region=None, delay=0.5, retries=1, custom_confidence=None):
    conf = custom_confidence if custom_confidence else CONFIDENCE_LEVEL
    for _ in range(retries):
        try:
            location = pyautogui.locateCenterOnScreen(img_path, confidence=conf, region=region)
            if location:
                pyautogui.click(location)
                time.sleep(delay)
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)
    return False

def is_image_on_screen(img_path, region=None, custom_confidence=None):
    conf = custom_confidence if custom_confidence else CONFIDENCE_LEVEL
    try:
        location = pyautogui.locateOnScreen(img_path, confidence=conf, region=region)
        return location is not None
    except:
        return False

def click_bet_color(color, window_rect):
    win_left, win_top, win_width, win_height = window_rect
    
    positions = {
        'grey':   (0.1716, 0.5994),
        'green':  (0.2770, 0.6025),
        'blue':   (0.3836, 0.6025),
        'pink':   (0.1667, 0.6541),
        'yellow': (0.2770, 0.6557),
        'red':    (0.3873, 0.6541)
    }
    
    if color in positions:
        rel_x, rel_y = positions[color]
        target_x = win_left + int(win_width * rel_x)
        target_y = win_top + int(win_height * rel_y)
        
        pyautogui.click(target_x, target_y)
        time.sleep(BASE_BET_DELAY)

def classify_color_by_rgb(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    if s < 0.25 or v < 0.20:
        return 'grey'

    if h < 0.08 or h > 0.92:
        return 'red'
    elif 0.08 <= h < 0.22:
        return 'yellow'
    elif 0.22 <= h < 0.45:
        return 'green'
    elif 0.45 <= h < 0.70:
        return 'blue'
    elif 0.70 <= h <= 0.92:
        return 'pink'

    return 'unknown'

def scan_balls_result(window_rect):
    win_left, win_top, win_width, win_height = window_rect
    
    box_left = win_left + int(win_width * 0.08)
    box_top = win_top + int(win_height * 0.43)
    box_width = int(win_width * 0.52)
    box_height = int(win_height * 0.13)
    
    sct_img = pyautogui.screenshot(region=(box_left, box_top, box_width, box_height))
    
    y = int(box_height * 0.6) 
    x1 = int(box_width * 0.17) 
    x2 = int(box_width * 0.29)
    x3 = int(box_width * 0.43)
    
    r1, g1, b1 = sct_img.getpixel((x1, y))
    r2, g2, b2 = sct_img.getpixel((x2, y))
    r3, g3, b3 = sct_img.getpixel((x3, y))
    
    draw = ImageDraw.Draw(sct_img)
    r_dot = 4
    draw.ellipse((x1-r_dot, y-r_dot, x1+r_dot, y+r_dot), fill='red')
    draw.ellipse((x2-r_dot, y-r_dot, x2+r_dot, y+r_dot), fill='red')
    draw.ellipse((x3-r_dot, y-r_dot, x3+r_dot, y+r_dot), fill='red')
    sct_img.save("debug_vision.png")
    
    c1 = classify_color_by_rgb(r1, g1, b1)
    c2 = classify_color_by_rgb(r2, g2, b2)
    c3 = classify_color_by_rgb(r3, g3, b3)
    
    log_text = f"หลุม 1:{c1.upper()} | หลุม 2:{c2.upper()} | หลุม 3:{c3.upper()}"
    return [c1, c2, c3], log_text

def main():
    print("=============================================")
    print("เริ่มการทำงาน Color Game Bot (ระบบ HSV ขั้นสูง)")
    print(f"โฟลเดอร์รูปภาพ: {IMG_DIR}/")
    print("ระบบหยุดฉุกเฉิน: ลากเมาส์ไปที่มุมซ้ายบนสุดของจอ")
    print("=============================================")
    
    if not os.path.exists(IMG_DIR):
        print(f"Error: ไม่พบโฟลเดอร์ '{IMG_DIR}'")
        return

    pyautogui.FAILSAFE = True
    is_last_game_won = True
    round_count = 1
    
    current_color = random.choice(COLORS)

    while True:
        window_rect = get_game_window("Poker Fate")
        if not window_rect:
            print("กำลังรอหน้าต่างเกม 'Poker Fate'...")
            time.sleep(3)
            continue

        if not is_image_on_screen(IMG_COLOR_TITLE, region=window_rect):
            print("ไม่ได้อยู่หน้า Color Game กำลังกดเข้า Casual Game...")
            find_and_click(IMG_CASUAL_BTN, region=window_rect, delay=2.0)
            continue 

        print(f"\n--- เริ่มรอบที่ {round_count} ---")
        
        if is_last_game_won:
            current_color = random.choice(COLORS)
            print(f"ตาที่แล้วชนะ -> สุ่มสีใหม่ได้: {current_color.upper()} (วาง Base Bet 1000)")
            find_and_click(IMG_CLEAR_BTN, region=window_rect, delay=BASE_BET_DELAY)
            find_and_click(IMG_CHIP_BASE, region=window_rect, delay=BASE_BET_DELAY, custom_confidence=0.95)
            click_bet_color(current_color, window_rect)
        else:
            print(f"ตาที่แล้วแพ้ -> ใช้สูตรแทงทบ สีเดิม: {current_color.upper()}")
            clicked_rebet = find_and_click(IMG_REBET_BTN, region=window_rect, delay=BASE_BET_DELAY, retries=2)
            if clicked_rebet:
                clicked_2x = find_and_click(IMG_2X_BTN, region=window_rect, delay=BASE_BET_DELAY, retries=3)
                if not clicked_2x:
                    print("หาปุ่ม 2X ไม่เจอ")
            else:
                print("หาปุ่ม Rebet ไม่เจอ ลองหาปุ่ม 2X เผื่อเงินยังค้างอยู่บนโต๊ะ...")
                clicked_2x = find_and_click(IMG_2X_BTN, region=window_rect, delay=BASE_BET_DELAY, retries=2)
                if not clicked_2x:
                    print("ระบบรวน ไม่เจอทั้ง Rebet และ 2X -> ขอเริ่มนับ 1 ใหม่กันเหนียว")
                    find_and_click(IMG_CLEAR_BTN, region=window_rect, delay=BASE_BET_DELAY)
                    find_and_click(IMG_CHIP_BASE, region=window_rect, delay=BASE_BET_DELAY)
                    click_bet_color(current_color, window_rect)

        print("กำลังบิดตู้ (Twist)...")
        if not find_and_click(IMG_TWIST_BTN, region=window_rect, delay=0.5, retries=4, custom_confidence=0.75):
            print("หาปุ่ม Twist ไม่เจอ! กำลังเคลียร์เงินบนโต๊ะคืน...")
            find_and_click(IMG_CLEAR_BTN, region=window_rect, delay=1.0)
            time.sleep(1.5)
            continue

        print("รออนิเมชั่นลูกบอล... (หลับตา 3.5 วินาทีแรก)")
        time.sleep(3.5)

        print(f"กำลังสแกนหาลูกบอลสี {current_color.upper()}...")
        
        is_won = False
        scan_start_time = time.time()
        scan_timeout = MAX_WAIT_TIME - 3.5 
        final_log = ""
        
        while time.time() - scan_start_time < scan_timeout:
            detected_colors, log_text = scan_balls_result(window_rect)
            final_log = log_text 
            
            if current_color in detected_colors:
                is_won = True
                break 
            
            time.sleep(0.3)
            
        time_taken = round((time.time() - scan_start_time) + 3.5, 1)
        print(f"ระบบอ่านสีได้: {final_log}")
        
        # ปรับเงื่อนไขเวลาในการรอตามผลลัพธ์แพ้/ชนะ
        if is_won:
            print(f"ผลลัพธ์: ชนะ! (เจอลูกบอลสี {current_color.upper()} ในเวลารวม {time_taken} วิ)")
            is_last_game_won = True
            wait_clear_time = 4
        else:
            print(f"ผลลัพธ์: แพ้! (รอจนครบ {time_taken} วิแล้วไม่เจอลูกบอลสี {current_color.upper()})")
            is_last_game_won = False
            wait_clear_time = 3
            
        round_count += 1
        print(f"รอระบบเคลียร์โต๊ะ {wait_clear_time} วินาที...")
        time.sleep(wait_clear_time) 

if __name__ == "__main__":
    time.sleep(2) 
    try:
        main()
    except KeyboardInterrupt:
        print("\nผู้ใช้กดหยุดการทำงานของบอท (Ctrl+C)")
