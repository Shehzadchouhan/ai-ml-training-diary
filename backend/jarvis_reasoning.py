from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from dotenv import load_dotenv
from Jarvis_google_search import google_search, get_current_datetime
from jarvis_get_whether import get_weather
from Jarvis_window_CTRL import open_app, close_app
from Jarvis_file_opner import Play_file
from jarvis_state import activate_jarvis, deactivate_jarvis
from keyboard_mouse_CTRL import (
    move_cursor_tool, mouse_click_tool, scroll_cursor_tool,
    type_text_tool, press_key_tool, swipe_gesture_tool,
    press_hotkey_tool, control_volume_tool
)
from langchain import hub
from livekit.agents import function_tool

load_dotenv()


@function_tool(
    name="thinking_capability",
    description=(
        "Main reasoning and decision-making tool for Jarvis. "
        "Handles queries like generating content, Google search, checking weather, "
        "opening/closing applications, playing files, and controlling system inputs. "
        "If the user asks to 'activate' or 'deactivate' Jarvis, it will directly call those tools."
    )
)
async def thinking_capability(query: str) -> dict:
    """
    AI reasoning and task execution for Jarvis.
    """

    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = hub.pull("hwchase17/react")

    # ✅ Define tools list
    tools = [
        google_search,
        get_current_datetime,
        get_weather,
        open_app,
        close_app,
        Play_file,
        move_cursor_tool,
        mouse_click_tool,
        scroll_cursor_tool,
        type_text_tool,
        press_key_tool,
        press_hotkey_tool,
        control_volume_tool,
        swipe_gesture_tool
    ]

    # ✅ Directly handle activate/deactivate requests before agent reasoning
    if any(word in query.lower() for word in ["activate jarvis", "wake up", "turn on jarvis"]):
        await activate_jarvis()
        return {"message": "Jarvis has been activated and is now listening."}

    if any(word in query.lower() for word in ["deactivate jarvis", "sleep", "turn off jarvis"]):
        await deactivate_jarvis()
        return {"message": "Jarvis has been deactivated and will stop responding until reactivated."}

    # ✅ Create reasoning agent
    agent = create_react_agent(llm=model, tools=tools, prompt=prompt)

    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    try:
        result = await executor.ainvoke({"input": query})
        return result
    except Exception as e:
        return {"error": f"Agent execution failed: {str(e)}"}
