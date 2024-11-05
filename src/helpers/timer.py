import time

class Timer:
    def __init__(self):
        self.times = {}  # Dictionary to store start times for each label

    def start(self, label):
        """Start a timer with a given label."""
        self.times[label] = time.time()
        print(f"'{label}' started.")

    def stop(self, label):
        """Stop the timer with the given label and print the elapsed time."""
        if label not in self.times:
            print(f"Timer '{label}' was not started.")
            return None
        elapsed_time = time.time() - self.times.pop(label)
        print(f"'{label}' stopped. Elapsed time: {elapsed_time:.4f} seconds.")
        return elapsed_time

T = Timer()