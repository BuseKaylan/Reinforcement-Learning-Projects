# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 03:23:23 2024

@author: bkaylan
"""

import numpy as np

class car:
    def __init__(self, track_array):
        self.track_array = np.array(track_array)
        self.ACTION_SPACE = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.States = [(x, y, vx, vy) for x in range(track_array.shape[0]) 
                       for y in range(track_array.shape[1]) 
                       for vx in range(1, 6)  # Velocity ranges from 1 to 5
                       for vy in range(1, 6)]  # Velocity ranges from 1 to 5
        self.rewards = {(x, y): -5 if track_array[x, y] == 35 else 1 if track_array[x, y] == 70 else -1 
                        for x in range(track_array.shape[0]) 
                        for y in range(track_array.shape[1])}
        self.actions = {(x, y, vx, vy): self.ACTION_SPACE 
                        for x in range(track_array.shape[0]) 
                        for y in range(track_array.shape[1]) 
                        for vx in range(1, 6) 
                        for vy in range(1, 6) 
                        if track_array[x, y] != 35}
        self.initial_state()
        
        
    def reset(self):
        # Find the starting position of the car (83)
        start_position = np.where(self.track_array == 83)
        if len(start_position[0]) == 0:
            raise ValueError("Starting position (83) not found on the track.")
        start_idx = np.random.choice(len(start_position[0]))
        # Initialize velocity values randomly within the range of 1 to 5
        vx = np.random.randint(1, 6)
        vy = np.random.randint(1, 6)
        self.s = (start_position[0][start_idx], start_position[1][start_idx], vx, vy)
        return self.s

    def initial_state(self):
        return self.reset()

    def _is_terminal(self):
        return self.s[:2] in [(x, y) for x in range(self.track_array.shape[0]) 
                              for y in range(self.track_array.shape[1]) 
                              if self.track_array[x, y] == 70]

    def _reward(self):
        return self.rewards.get(self.s[:2], 0)

    def step(self, action):
    # Get the index of the current state
        i, j, vx, vy = self.s

    # Determine the change in position based on the action
        dx, dy = action

    # Update the index of the next state
        i += vx * dx
        j += vy * dy

    # Check if the next state is within the track boundaries
        if 0 <= i < self.track_array.shape[0] and 0 <= j < self.track_array.shape[1]:
        # Check if the next state is a wall (35)
            if self.track_array[i, j] == 35:
            # If next state is wall, reset to starting position
                return self.reset(), -5, False  # Returning reset state, reward, and done flag
            else:
            # If next state is not wall, update current state
                self.s = (i, j, min(vx + 1, 5), min(vy + 1, 5))  # Velocity ranges from 1 to 5
        else:
        # If next state is out of bounds, reset to starting position
            return self.reset(), -5, False  # Returning reset state, reward, and done flag

    # Calculate reward and check if terminal state is reached
        r = self._reward()
        done = self._is_terminal()
    
        return self.s, r, done  # Returning next state, reward, and done flag




