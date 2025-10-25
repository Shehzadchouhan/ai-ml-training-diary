import os
import subprocess
import sys
import logging
from fuzzywuzzy import process
from langchain.tools import tool
import platform

# Console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def Play_file(name: str, action: str = "open") -> str:
    """
    Opens a file or folder by fuzzy matching the name in Desktop, Downloads, Documents, and D drive.

    Example:
    - "Open my resume"
    - "Open college project folder"
    """

    # Folders to search in
    folders_to_index = [
        "C:/Users/Lenovo/Desktop",
        "C:/Users/Lenovo/Downloads",
        "C:/Users/Lenovo/Documents",
        "D:/"
    ]

    # Filter only existing ones
    folders_to_index = [f for f in folders_to_index if os.path.exists(f)]

    # Build a file/folder list
    all_items = []
    for base in folders_to_index:
        for root, dirs, files in os.walk(base):
            for f in files:
                all_items.append({"name": f.lower(), "path": os.path.join(root, f)})
            for d in dirs:
                all_items.append({"name": d.lower(), "path": os.path.join(root, d)})

    if not all_items:
        return "⚠ No files or folders found in the indexed locations."

    # Find best fuzzy match
    names = [item["name"] for item in all_items]
    best_match, score = process.extractOne(name.lower(), names)

    if score < 70:
        return f"❌ No close match found for '{name}'."

    # Get the matched item path
    item = next(i for i in all_items if i["name"] == best_match)
    path = item["path"]

    # Perform the action
    if action == "open":
        try:
            logger.info(f"📂 Opening: {path}")
            if sys.platform.startswith('win'):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path])
            else:
                subprocess.run(["xdg-open", path])
            return f"✅ Opened: {os.path.basename(path)}"
        except Exception as e:
            return f"❌ Failed to open file/folder: {e}"

    elif action == "close":
        return "⚠ Closing files is not supported in the simple version."

    else:
        return "⚠ Invalid action specified."



@tool
async def System_control(command: str) -> str:
    """
    Controls the system — shutdown, restart, or log off — using voice commands.
    Example:
    - "Shutdown the system"
    - "Restart computer"
    - "Log off my PC"
    """

    cmd = command.lower().strip()

    try:
        if "shutdown" in cmd:
            logger.info("🛑 System is shutting down...")
            if os.name == 'nt':  # Windows
                os.system("shutdown /s /t 5")
            elif sys.platform == 'darwin':  # macOS
                os.system("sudo shutdown -h now")
            else:  # Linux
                os.system("shutdown now")
            return "🛑 Shutting down your system in 5 seconds..."

        elif "restart" in cmd or "reboot" in cmd:
            logger.info("🔁 System is restarting...")
            if os.name == 'nt':
                os.system("shutdown /r /t 5")
            elif sys.platform == 'darwin':
                os.system("sudo shutdown -r now")
            else:
                os.system("reboot")
            return "🔁 Restarting your system..."

        elif "log off" in cmd or "sign out" in cmd:
            logger.info("👋 Logging off user...")
            if os.name == 'nt':
                os.system("shutdown /l")
            else:
                os.system("logout")
            return "👋 Logging off now..."

        else:
            return "⚠ Please say shutdown, restart, or log off clearly."

    except Exception as e:
        logger.error(f"❌ System control failed: {e}")
        return f"❌ Could not perform system control: {e}"