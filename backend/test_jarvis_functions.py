print("name - Mohd.Shehzad, group - G5, roll_no(URN) - 2302612")

import asyncio
from backend.Jarvis_file_opner import Play_file

# Helper to run async LangChain tools
async def run_tool(tool, param_name, value):
    print(f"\n🧠 Running tool: {tool.name} with {param_name}='{value}'")
    try:
        result = await tool.ainvoke({param_name: value})
        print("✅ Result:", result)
    except Exception as e:
        print("❌ Error:", e)

async def main():
    # Test 1: Open an app
    await run_tool(open_app, "app_title", "calculator")

    # Test 2: Close an app
    await run_tool(close_app, "window_title", "calculator")

    # Test 3: Open folder
    await run_tool(folder_file, "command", "Downloads")

    # Test 4: Play a file (replace with a real file name from D:/)
    await run_tool(Play_file, "name", "sample.mp3")

    print("\n✅ All tests executed! Check visually if actions worked.")

asyncio.run(main())
