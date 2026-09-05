import asyncio
from typing import Dict, Any, Optional

class TaskStore:
    def __init__(self):
        self._active_tasks: Dict[str, Dict[str, Any]] = {}

    def add_task(self, task_hash: str, task_obj: asyncio.Task, msg_id: int) -> None:
        """افزودن وظیفه جدید به حافظه"""
        self._active_tasks[task_hash] = {"task": task_obj, "msg_id": msg_id}

    def remove_task(self, task_hash: str) -> Optional[int]:
        """توقف و حذف وظیفه از حافظه، و بازگرداندن آیدی پیام مرتبط"""
        if task_hash in self._active_tasks:
            task_data = self._active_tasks.pop(task_hash)
            task_data["task"].cancel()
            return task_data["msg_id"]
        return None

# نمونه سینگلتون (Singleton) برای استفاده در سطح اپلیکیشن
store = TaskStore()