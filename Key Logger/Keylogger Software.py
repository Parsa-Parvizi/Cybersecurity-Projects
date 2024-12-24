import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pynput.keyboard import Listener
from pynput.mouse import Listener as MouseListener
import win32gui
from PIL import ImageGrab

# Configure logging
logging.basicConfig(filename="keylog.txt", level=logging.INFO, format="%(asctime)s: %(message)s")

def get_active_window_title():
    window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return window_title

def is_interesting_key_combo(key, modifiers):
    # Define logic to identify interesting key combinations (e.g., Ctrl+C, Ctrl+V)
    return key == "c" and modifiers == ["ctrl"]

def capture_screenshot():
    screenshot = ImageGrab.grab()
    # Optionally save the screenshot to a file
    screenshot.save(f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

def on_move(x, y):
    logging.info(f"Mouse moved to: ({x}, {y})")

def on_click(x, y, button, pressed):
    logging.info(f"Mouse {button} at ({x}, {y})")

def on_window_change():
    # Code to detect window change (using win32gui or other libraries)
    capture_screenshot()

def on_press(key):
    global start_time
    modifiers = [mod for mod in ['ctrl', 'shift', 'alt'] if getattr(key, mod)]
    try:
        key_str = str(key.char)
    except AttributeError:
        key_str = str(key)
    current_time = datetime.now()
    if not start_time:
        start_time = current_time

    # Get the title of the active window
    window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    # Taking screenshots (e.g. every 5 minutes)
    if (current_time - start_time).total_seconds() >= 300:  # 5 minutes
        screenshot = ImageGrab.grab()
        screenshot.save(f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        start_time = None  # Reset the screenshot timer

    # Filtering specific keys (e.g. Ctrl+C)
    if is_interesting_key_combo(key, modifiers):
        logging.info(f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}, Window: {window_title}, Modifiers: {modifiers}, Key Pressed: {key_str}")

    logging.info(f"Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}, Window: {window_title}, Modifiers: {modifiers}, Key Pressed: {key_str}")

    # Create a dictionary to store data for each event
    data = {
        'time': datetime.now(),
        'key': key_str,
        'modifiers': ','.join(modifiers),
        'window_title': window_title
    }

    # Append data to a list
    data_list.append(data)

def on_release(key):
    global start_time
    if start_time:
        hold_time = datetime.now() - start_time
        logging.info(f"Key Released: {str(key.char) if hasattr(key, 'char') else str(key)}, Hold Time: {hold_time.total_seconds():.2f} seconds")
        start_time = None

# Create an empty list to store data
data_list = []

# Initialize start_time outside the functions to avoid race condition
start_time = None

# Start listening for events
with Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
    with MouseListener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    ) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()

# Create a Pandas DataFrame from the data list
df = pd.DataFrame(data_list)