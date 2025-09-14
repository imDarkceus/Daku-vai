from livekit.agents import function_tool
from daku_memory import DakuMemory
from daku_bus_detect import detect_bus_from_camera
memory = DakuMemory()

@function_tool()
async def remember_person(name: str, info: str) -> str:
    """
    Save personal info about someone.
    Example: "remember Rahim is my best friend, works in Dhaka."
    """
    return memory.remember(name, info)

@function_tool()
async def recall_person(name: str) -> str:
    """
    Retrieve stored info about a person by name.
    Example: "tell me about Rahim" → returns stored info.
    """
    return memory.recall(name)

@function_tool()
async def list_known_people() -> str:
    """
    List all names stored in memory.
    Example: "who do you know?" → returns list.
    """
    return memory.list_people()

@function_tool()
async def detect_bus_tool():
    result = detect_bus_from_camera()
    return result