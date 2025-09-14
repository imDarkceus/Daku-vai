from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import google, noise_cancellation

# Import your custom modules
from Daku_prompt import DakuPrompts
from daku_google_search import google_search, get_current_datetime
from daku_get_whether import get_weather
from daku_window_control import open_app, close_app, folder_file
from daku_file_opner import Play_file
from key_mou_ctr import (
    move_cursor_tool, mouse_click_tool, scroll_cursor_tool,
    type_text_tool, press_key_tool, swipe_gesture_tool,
    press_hotkey_tool, control_volume_tool
)
#from memory_loop import MemoryExtractor

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self, chat_ctx) -> None:
        super().__init__(
            chat_ctx=chat_ctx,
            instructions=DakuPrompts.BEHAVIOR,
            tools=[
                google_search,
                get_current_datetime,
                get_weather,
                open_app,
                close_app,
                folder_file,
                Play_file,
                move_cursor_tool,
                mouse_click_tool,
                scroll_cursor_tool,
                type_text_tool,
                press_key_tool,
                press_hotkey_tool,
                control_volume_tool,
                swipe_gesture_tool,
            ],
        )


async def entrypoint(ctx: agents.JobContext):
    # Initialize session with Gemini realtime LLM
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice = "Leda"
        ),
        preemptive_generation=True,
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(chat_ctx=session.history.items),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Startup greeting
    await session.generate_reply(
        instructions=DakuPrompts.STARTUP_REPLY
    )

    # Run your memory loop
   # conv_ctx = MemoryExtractor()
    #await conv_ctx.run(session.history.items)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
