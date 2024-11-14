import math
import time
class OneEuroFilter:
    def __init__(self, min_cutoff=1.0, beta=0.007, d_cutoff=1.0):
        # These parameters define the responsiveness and smoothness:
        # min_cutoff controls general smoothing, beta controls the response to fast movements
        # d_cutoff is for differentiating changes (e.g., speed adjustments)
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev = None
        self.dx_prev = 0.0
        self.last_time = None

    def smoothing_factor(self, cutoff):
        r = 2 * math.pi * cutoff
        return r / (r + 1)

    def exponential_smoothing(self, alpha, x, x_prev):
        return alpha * x + (1 - alpha) * x_prev

    def __call__(self, x, timestamp=None):
        # Use the current time if timestamp is not provided
        if timestamp is None:
            timestamp = time.time()

        if self.last_time is None:
            # First call, just initialize the previous values
            self.last_time = timestamp
            self.x_prev = x
            return x

        # Calculate time difference
        dt = timestamp - self.last_time
        self.last_time = timestamp

        # Estimate the derivative of the signal
        dx = (x - self.x_prev) / dt if dt > 0 else 0.0
        alpha_d = self.smoothing_factor(self.d_cutoff)
        dx_hat = self.exponential_smoothing(alpha_d, dx, self.dx_prev)

        # Adjust cutoff based on the speed of movement (adaptive response)
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        alpha = self.smoothing_factor(cutoff)

        # Apply the filter to the input value
        x_hat = self.exponential_smoothing(alpha, x, self.x_prev)

        # Update previous values
        self.x_prev = x_hat
        self.dx_prev = dx_hat

        return x_hat

