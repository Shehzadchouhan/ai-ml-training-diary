# jarvis_state.py

# ---------------------------
# Custom fallback for @tool
# ---------------------------
# Some LiveKit versions don't provide a built-in `tool` decorator.
# We'll define a minimal one that just returns the original function.
def tool(func):
    return func


# ---------------------------
# Global Activation State
# ---------------------------
JARVIS_ACTIVE = True


def set_jarvis_active(state: bool):
    """Update the activation state of Jarvis."""
    global JARVIS_ACTIVE
    JARVIS_ACTIVE = state


# ---------------------------
# Tool Functions
# ---------------------------
@tool
async def deactivate_jarvis() -> str:
    """Temporarily deactivate Jarvis."""
    set_jarvis_active(False)
    return "🛑 Jarvis deactivated. Say 'activate Jarvis' to wake me again."


@tool
async def activate_jarvis() -> str:
    """Reactivate Jarvis."""
    set_jarvis_active(True)
    return "✅ Jarvis reactivated and ready to help!"
