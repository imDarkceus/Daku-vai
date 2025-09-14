from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ChatContext, ChatMessage
from livekit.plugins import google, noise_cancellation

# Import your custom modules
from promp import instructions_prompt, Reply_prompts
from memory_loop import MemoryExtractor
from daku_reasoning import thinking_capability
load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self, chat_ctx) -> None:
        super().__init__(chat_ctx = chat_ctx,
                        instructions=instructions_prompt,
                        llm=google.beta.realtime.RealtimeModel(voice="Charon"),
                        tools=[thinking_capability]
                                )

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
    
    # Example tool logic for bus detection
    tool_result = detect_bus_from_camera()
    if tool_result["status"] == "success":
        for bus in tool_result["buses"]:
            reply_text = f"Boss, detect করেছি! 🚍 Bus No {bus['number']} — {bus['name']} । Route: {bus['route']}"
            await session.send_text(reply_text)
    elif tool_result["status"] == "no_match":
        await session.send_text("Boss, দুঃখিত — কোনো bus detect করতে পারলাম না।")
    else:
        await session.send_text(tool_result.get("message", "Camera feed problem, Boss!"))


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
