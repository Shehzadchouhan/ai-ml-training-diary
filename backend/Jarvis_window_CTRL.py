import os
import subprocess
import logging
import sys
import asyncio
from fuzzywuzzy import process
import subprocess
from jarvis_state import JARVIS_ACTIVE

try:
    import win32gui
    import win32con
except ImportError:
    win32gui = None
    win32con = None

try:
    import pygetwindow as gw
except ImportError:
    gw = None

from langchain.tools import tool

# Setup encoding and logger
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App command map
APP_MAPPINGS = {
    # Basic Windows apps
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "wordpad": "write",
    "command prompt": "cmd",
    "powershell": "powershell",
    "control panel": "control",
    "settings": "start ms-settings:",
    "explorer": "explorer",
    "calendar": r"C:\Users\Lenovo\OneDrive\Desktop\Calendar.lnk",
    
    # Browsers
    "chrome": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk",
    "edge": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "firefox": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Firefox.lnk",
    "youtube": r"C:\Users\Lenovo\OneDrive\Desktop\YouTube.lnk",
    
    # Microsoft Office apps (adjust if using Office 365 / custom path)
    "word": r"C:\Users\Lenovo\OneDrive\Desktop\Word.lnk",
    "excel": r"C:\Users\Lenovo\OneDrive\Desktop\Excel.lnk",
    "powerpoint": r"C:\Users\Lenovo\OneDrive\Desktop\PowerPoint.lnk",
    
    # Multimedia
    "vlc": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\VideoLAN\VLC media player.lnk",
    "whatsapp": r"C:\Users\Lenovo\OneDrive\Desktop\WhatsApp.lnk",
    
    # Development tools
    "vs code": r"C:\Users\Lenovo\OneDrive\Desktop\Visual Studio Code.lnk",
    "postman": r"C:\Users\Lenovo\OneDrive\Desktop\Postman.lnk",
    
    # Utilities / Alarms
    "alarm": r"C:\Users\Lenovo\OneDrive\Desktop\Alarms & Clock.lnk",
    
    # Add more apps below as needed
}


# -------------------------
# Global focus utility
# -------------------------
async def focus_window(title_keyword: str) -> bool:
    if not gw:
        logger.warning("⚠ pygetwindow")
        return False

    await asyncio.sleep(1.5)  # Give time for window to appear
    title_keyword = title_keyword.lower().strip()

    for window in gw.getAllWindows():
        if title_keyword in window.title.lower():
            if window.isMinimized:
                window.restore()
            window.activate()
            return True
    return False

# Index files/folders
async def index_items(base_dirs):
    item_index = []
    for base_dir in base_dirs:
        for root, dirs, files in os.walk(base_dir):
            for d in dirs:
                item_index.append({"name": d, "path": os.path.join(root, d), "type": "folder"})
            for f in files:
                item_index.append({"name": f, "path": os.path.join(root, f), "type": "file"})
    logger.info(f"✅ Indexed {len(item_index)} items.")
    return item_index


async def search_item(query, index, item_type):
    filtered = [item for item in index if item["type"] == item_type]
    choices = [item["name"] for item in filtered]
    if not choices:
        return None
    best_match, score = process.extractOne(query, choices)
    logger.info(f"🔍 Matched '{query}' to '{best_match}' with score {score}")
    if score > 70:
        for item in filtered:
            if item["name"] == best_match:
                return item
    return None
    

@tool
async def deactivate_jarvis() -> str:
    """Deactivate Jarvis temporarily."""
    global JARVIS_ACTIVE
    JARVIS_ACTIVE = False
    return "🛑 Jarvis deactivated. Say 'activate jarvis' to wake me up."

@tool
async def activate_jarvis() -> str:
    """Activate Jarvis."""
    global JARVIS_ACTIVE
    JARVIS_ACTIVE = True
    return "✅ Jarvis is now active."


@tool
async def open_app(app_title: str) -> str:
    """
    open_app a desktop app like Notepad, Chrome, VLC, etc.

    Use this tool when the user asks to launch an application on their computer.
    Example prompts:
    - "Notepad खोलो"
    - "Chrome open करो"
    - "VLC media player चलाओ"
    - "Calculator launch करो"
    """
    if not JARVIS_ACTIVE:
        return "❌ Jarvis is deactivated. Say 'activate jarvis' to wake me up."


    app_title = app_title.lower().strip()
    app_command = APP_MAPPINGS.get(app_title, app_title)
    try:
        # Use platform-native launch methods for reliability.
        if os.name == 'nt':
            # Prefer os.startfile when the mapping is a path or a shortcut/executable.
            try:
                if os.path.exists(app_command) or any(app_command.lower().endswith(ext) for ext in ('.lnk', '.exe', '.bat', '.cmd')):
                    os.startfile(app_command)
                else:
                    # Fallback to shell start for builtin commands like 'notepad' or 'calc'
                    subprocess.Popen(f'start "" "{app_command}"', shell=True)
            except Exception:
                # Final fallback: try to spawn the command directly
                subprocess.Popen(app_command, shell=True)
        else:
            # POSIX: attempt to run the command directly (or the path)
            try:
                subprocess.Popen([app_command])
            except Exception:
                subprocess.Popen(app_command, shell=True)

        # Give the OS a moment to start the app, then attempt to focus its window
        await asyncio.sleep(0.5)
        focused = await focus_window(app_title)
        if focused:
            return f"🚀 App launch हुआ और focus में है: {app_title}."
        else:
            return f"🚀 {app_title} Launch किया गया, लेकिन window पर focus नहीं हो पाया।"
    except Exception as e:
        return f"❌ {app_title} Launch नहीं हो पाया।: {e}"
    

@tool
async def close_app(app_name: str) -> str:
    """
    Closes an application by its window title or executable name.
    Works for normal apps and stubborn apps like Chrome, VS Code, etc.
    """
    if not JARVIS_ACTIVE:
        return "❌ Jarvis is deactivated. Say 'activate jarvis' to wake me up."
    

    if not win32gui:
        return "❌ win32gui module not available."

    closed = False
    app_name_lower = app_name.lower()

    # First: try closing by window title
    def enumHandler(hwnd, _):
        nonlocal closed
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if app_name_lower in title:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                closed = True

    win32gui.EnumWindows(enumHandler, None)

    # If not closed, try force-kill via taskkill
    if not closed:
        # Mapping of app names to process executable (optional: extend this list)
        TASK_MAPPINGS = {
            "chrome": "chrome.exe",
            "vs code": "Code.exe",
            "postman": "Postman.exe",
            "vlc": "vlc.exe",
            "spotify": "Spotify.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
        }