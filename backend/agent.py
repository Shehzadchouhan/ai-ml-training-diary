from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ChatContext, ChatMessage
from livekit.plugins import google, noise_cancellation

# Custom imports
from jarvis_state import JARVIS_ACTIVE, set_jarvis_active,activate_jarvis, deactivate_jarvis
from Jarvis_prompts import instructions_prompt, Reply_prompts
from memory_loop import MemoryExtractor
from jarvis_reasoning import thinking_capability

load_dotenv()


# --------------------------
# Assistant Class
# --------------------------
class Assistant(Agent):
    def __init__(self, chat_ctx) -> None:
        super().__init__(
            chat_ctx=chat_ctx,
            instructions=instructions_prompt,
            llm=google.beta.realtime.RealtimeModel(voice="Charon"),
            tools=[
                thinking_capability,  
            ]  
        )

    async def on_message(self, message: ChatMessage):
        from jarvis_state import JARVIS_ACTIVE  # ensure updated state
        text = message.text.lower().strip()

        # Debug info
        print(f"[DEBUG] Jarvis Active: {JARVIS_ACTIVE} | Message: {text}")

        # If deactivated, listen only for reactivation
        if not JARVIS_ACTIVE:
            if "activate jarvis" in text or "wake up jarvis" in text:
                from jarvis_state import set_jarvis_active
                set_jarvis_active(True)
                await self.say("✅ Jarvis reactivated and ready to help!")
            else:
                print("🤫 Jarvis is deactivated, ignoring input...")
            return  # stop processing further

        # If active and user says deactivate
        if "deactivate jarvis" in text or "sleep jarvis" in text:
            from jarvis_state import set_jarvis_active
            set_jarvis_active(False)
            await self.say("🛑 Jarvis deactivated. Say 'activate Jarvis' to wake me again.")
            return

        # If active, process normally
        await super().on_message(message)


# --------------------------
# Entrypoint
# --------------------------
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        preemptive_generation=True
    )
    
    #getting the current memory chat
    current_ctx = session.history.items
    

    await session.start(
        room=ctx.room,
        agent=Assistant(chat_ctx=current_ctx), #sending currenet chat to llm in realtime
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )
    await session.generate_reply(
        instructions=Reply_prompts
    )
    conv_ctx = MemoryExtractor()
    await conv_ctx.run(current_ctx)
    


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

