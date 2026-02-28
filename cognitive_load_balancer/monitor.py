# monitor.py
import time
import threading
import random

class ActivityMonitor:
    def __init__(self):
        self.key_presses = 0
        self.pauses_over_5_sec = 0
        self.last_press_time = time.time()
        self.start_time = time.time()
        self.is_running = True

    def _simulate_activity(self):
        """
        Simulates typing because cloud environments (Codespaces) 
        cannot track physical local keyboards.
        """
        while self.is_running:
            # 70% chance you are actively coding
            if random.random() > 0.3:
                self.key_presses += 1
                self.last_press_time = time.time()
                time.sleep(0.2) # Typing fast
            else:
                # 30% chance you are "stuck" and staring at the screen
                time.sleep(6.0) # Pause for 6 seconds
                self.pauses_over_5_sec += 1

    def start(self):
        print("⚠️ [NOTE] Running in Codespace/Headless mode.")
        print("⚠️ [NOTE] Simulating fake keystrokes and pauses for testing...")
        
        # Run the simulator in a background thread
        listener_thread = threading.Thread(target=self._simulate_activity)
        listener_thread.daemon = True
        listener_thread.start()

    def reset_metrics(self):
        """Reset metrics after task delegation to give the dev a fresh start."""
        self.key_presses = 0
        self.pauses_over_5_sec = 0
        self.last_press_time = time.time()
        self.start_time = time.time()