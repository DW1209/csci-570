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


def basic_algorithm(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # initialize the first row and column of the dp table
    for i in range(m + 1):
        dp[i][0] = i * delta_e
    for j in range(n + 1):
        dp[0][j] = j * delta_e

    # fill the dp table
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

    # traceback to find the alignment
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

    # handle the remaining characters
    while i > 0:
        str1_align += str1[i - 1]
        str2_align += '-'
        i -= 1
    while j > 0:
        str2_align += str2[j - 1]
        str1_align += '-'
        j -= 1
    
    # reverse the strings to get the correct order
    str1_align, str2_align = str1_align[::-1], str2_align[::-1]
    return str1_align, str2_align


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = float(memory_info.rss / 1024)
    return memory_consumed


def time_wrapper(str1, str2):
    start_time = time.time()
    dp = basic_algorithm(str1, str2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return dp, time_taken


if __name__ == '__main__':
    # check if the correct number of arguments is provided
    if len(sys.argv) != 3 or sys.argv[1] == '' or sys.argv[2] == '':
        print("Usage: python basic.py <input file> <output file>")
        sys.exit(1)

    # read the input file
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f'{input_file} does not exist.')
        sys.exit(1)
    with open(input_file, 'r') as f:
        lst = [line.strip() for line in f if line.strip()]

    # generate the string str1 and str2
    idx = len(lst) // 2
    str1 = generate_string(lst[0], lst[1:idx])
    str2 = generate_string(lst[idx], lst[idx + 1:])

    # measure the time and memory consumption
    dp, time_taken = time_wrapper(str1, str2)
    str1_align, str2_algin = top_down_pass(dp, str1, str2)
    memory_consumed = process_memory()

    # write the output to the output file
    output_file = sys.argv[2]
    with open(output_file, 'w') as f:
        f.write(f'{dp[-1][-1]}\n')
        f.write(f'{str1_align}\n')
        f.write(f'{str2_algin}\n')
        f.write(f'{time_taken}\n')
        f.write(f'{memory_consumed}\n')
