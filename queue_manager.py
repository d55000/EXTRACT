# queue_manager.py
import asyncio
from typing import Callable, Any

class QueueManager:
    """
    A simple async queue manager to process tasks sequentially.
    """
    def __init__(self, max_concurrent: int = 1):
        self.queue = asyncio.Queue()
        self.workers = [asyncio.create_task(self._worker()) for _ in range(max_concurrent)]

    async def _worker(self):
        while True:
            task, args, kwargs = await self.queue.get()
            try:
                await task(*args, **kwargs)
            except Exception as e:
                print(f"Task Error: {e}")
            finally:
                self.queue.task_done()

    async def add_task(self, task: Callable, *args: Any, **kwargs: Any):
        await self.queue.put((task, args, kwargs))

queue_manager = QueueManager()
