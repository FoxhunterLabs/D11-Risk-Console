import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class ResetLatch:
    armed: bool = False
    armed_at: Optional[float] = None
    timeout_sec: int = 20

    def arm(self):
        self.armed = True
        self.armed_at = time.time()

    def disarm(self):
        self.armed = False
        self.armed_at = None

    def expired(self) -> bool:
        if not self.armed or self.armed_at is None:
            return False
        return (time.time() - self.armed_at) > self.timeout_sec

    def can_confirm(self) -> bool:
        if not self.armed:
            return False
        if self.expired():
            self.disarm()
            return False
        return True
