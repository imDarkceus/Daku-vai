import json
import os
from typing import Dict

MEMORY_FILE = "memory.json"

class DakuMemory:
    def __init__(self):
        # যদি ফাইল না থাকে তবে empty dict বানাই
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        self._load()

    def _load(self):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            self.memory: Dict[str, str] = json.load(f)

    def _save(self):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def remember(self, name: str, info: str) -> str:
        self.memory[name.lower()] = info
        self._save()
        return f"Boss, মনে রাখলাম {name} এর তথ্য।"

    def recall(self, name: str) -> str:
        info = self.memory.get(name.lower())
        if info:
            return f"{name} সম্পর্কে যা জানি: {info}"
        return f"Boss, দুঃখিত — {name} সম্পর্কে কোনো তথ্য খুঁজে পেলাম না।"

    def list_people(self) -> str:
        if not self.memory:
            return "Boss, আমার মনে কোনো নাম নেই এখনো।"
        names = ", ".join(self.memory.keys())
        return f"Boss, আমি যাদের মনে রেখেছি: {names}"
