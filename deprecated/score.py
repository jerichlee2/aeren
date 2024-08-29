import numpy as np

def calculate_constant_mse_max(category_bounds):
    total_mse_max = 0

    for category, bounds in category_bounds.items():
        min_value, max_value = bounds
        # Calculate the maximum difference
        max_diff = max_value - min_value
        
        # Use the middle of the range as the expected value
        expected_value = (min_value + max_value) / 2
        
        # Normalize the difference by the expected value to get the relative error
        normalized_diff = max_diff / expected_value if expected_value != 0 else 0
        
        # Square the normalized difference
        squared_diff = normalized_diff ** 2
        
        # Add to total MSE_max
        total_mse_max += squared_diff
    
    return total_mse_max

def calculate_score(today_value, goal_value, mse_max):
    # Calculate the MSE for today's values
    difference = today_value - goal_value
    normalized_diff = difference / (goal_value if goal_value != 0 else 1)
    mse = normalized_diff ** 2

    # Calculate the score using MSE and MSE_max
    score = 100 * (1 - (mse / mse_max))
    return max(0, min(100, score))
