import os
import sys
import time
import psutil
from resource import *


delta_e = 30
alpha = {
    'A': { 'A': 0,   'C': 110, 'G': 48,  'T': 94  },
    'C': { 'A': 110, 'C': 0,   'G': 118, 'T': 48  },
    'G': { 'A': 48,  'C': 118, 'G': 0,   'T': 110 },
    'T': { 'A': 94,  'C': 48,  'G': 110, 'T': 0   }
}


def generate_string(base, indices):
    string = base
    for idx in indices:
        string = base[0:int(idx) + 1] + base + base[int(idx) + 1:]
        base = string
    return string


def score(a, b):
    return alpha[a][b]


def forward_score(str1, str2):
    m, n = len(str1), len(str2)
    
    # Only need two rows of the DP table
    prev_row = [j * delta_e for j in range(n + 1)]
    curr_row = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr_row[0] = i * delta_e
        for j in range(1, n + 1):
            match = prev_row[j - 1] + score(str1[i - 1], str2[j - 1])
            delete = prev_row[j] + delta_e
            insert = curr_row[j - 1] + delta_e
            curr_row[j] = min(match, delete, insert)
        
        # Swap rows for next iteration
        prev_row, curr_row = curr_row, prev_row
    
    # Return the last row computed (which is prev_row after the swap)
    return prev_row


def backward_score(str1, str2):
    # Reverse the strings
    str1_rev = str1[::-1]
    str2_rev = str2[::-1]
    return forward_score(str1_rev, str2_rev)


def efficient_algorithm(str1, str2):
    m, n = len(str1), len(str2)
    
    # Base cases
    if m == 0:
        return '-' * n, str2
    if n == 0:
        return str1, '-' * m
    if m <= 5 or n <= 5:
        # For short strings, use the basic algorithm
        dp = basic_algorithm(str1, str2)
        return top_down_pass(dp, str1, str2)
    
    mid = m // 2
    str1_first_half = str1[:mid]
    str1_second_half = str1[mid:]
    forward_scores = forward_score(str1_first_half, str2)
    backward_scores = backward_score(str1_second_half, str2)
    
    # Find the optimal split point for str2
    split = 0
    min_score = float('inf')
    
    for j in range(n + 1):
        current_score = forward_scores[j] + backward_scores[n - j]
        if current_score < min_score:
            min_score = current_score
            split = j
    
    str1_a, str2_a = efficient_algorithm(str1_first_half, str2[:split])
    str1_b, str2_b = efficient_algorithm(str1_second_half, str2[split:])
    
    return str1_a + str1_b, str2_a + str2_b


def basic_algorithm(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * delta_e
    for j in range(n + 1):
        dp[0][j] = j * delta_e

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(
                dp[i - 1][j - 1] + alpha[str1[i - 1]][str2[j - 1]],
                dp[i - 1][j] + delta_e,
                dp[i][j - 1] + delta_e
            )

    return dp


def top_down_pass(dp, str1, str2):
    i, j = len(str1), len(str2)
    str1_align, str2_align = str(), str()

    while i > 0 and j > 0:
        if dp[i][j] == dp[i - 1][j - 1] + alpha[str1[i - 1]][str2[j - 1]]:
            str1_align += str1[i - 1]
            str2_align += str2[j - 1]
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + delta_e:
            str1_align += str1[i - 1]
            str2_align += '-'
            i -= 1
        else:
            str2_align += str2[j - 1]
            str1_align += '-'
            j -= 1

    while i > 0:
        str1_align += str1[i - 1]
        str2_align += '-'
        i -= 1
    while j > 0:
        str2_align += str2[j - 1]
        str1_align += '-'
        j -= 1
    
    str1_align, str2_align = str1_align[::-1], str2_align[::-1]
    return str1_align, str2_align


def calculate_alignment_score(str1_align, str2_align):
    score = 0
    for i in range(len(str1_align)):
        if str1_align[i] == '-' or str2_align[i] == '-':
            score += delta_e
        else:
            score += alpha[str1_align[i]][str2_align[i]]
    return score


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = float(memory_info.rss / 1024)
    return memory_consumed


def time_wrapper(str1, str2):
    start_time = time.time()
    str1_align, str2_align = efficient_algorithm(str1, str2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    
    # Calculate the alignment score
    alignment_score = calculate_alignment_score(str1_align, str2_align)
    
    return alignment_score, str1_align, str2_align, time_taken


if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3 or sys.argv[1] == '' or sys.argv[2] == '':
        print("Usage: python memory_efficient.py <input file> <output file>")
        sys.exit(1)

    # Read the input file
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f'{input_path} does not exist.')
        sys.exit(1)
    with open(input_path, 'r') as f:
        lst = [line.strip() for line in f if line.strip()]

    # Generate the string str1 and str2
    s1_base = lst[0]
    s2_base_idx = 1
    while s2_base_idx < len(lst) and lst[s2_base_idx].isdigit():
        s2_base_idx += 1
    s1_indices = lst[1:s2_base_idx]
    s2_base = lst[s2_base_idx]
    s2_indices = lst[s2_base_idx+1:]
    str1 = generate_string(s1_base, s1_indices)
    str2 = generate_string(s2_base, s2_indices)

    # Measure the time and memory consumption
    alignment_score, str1_align, str2_align, time_taken = time_wrapper(str1, str2)
    memory_consumed = process_memory()

    # Write the output to the output file
    output_path = sys.argv[2]
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(f'{alignment_score}\n')
        f.write(f'{str1_align}\n')
        f.write(f'{str2_align}\n')
        f.write(f'{time_taken}\n')
        f.write(f'{memory_consumed}\n')
