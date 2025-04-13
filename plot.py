import os
import matplotlib.pyplot as plt


if __name__ == '__main__':
    problem_sizes = [
        16, 64, 128, 256, 384, 
        512, 768, 1024, 1280, 1536, 
        2048, 2560, 3072, 3584, 3968
    ]

    pics_dir = 'pics'
    output_dir = 'output'
    b_time, b_mem = list(), list()
    e_time, e_mem = list(), list()

    # get the value of cpu time and memory usage
    for i in range(1, 16):
        for method in ['basic', 'effic']:
            filename = f'out{i}_{method}.txt'
            path = os.path.join(output_dir, filename)
            if not os.path.exists(path):
                print(f'{path} does not exist.')
                continue
            with open(path, 'r') as f:
                lines = f.readlines()
                time, mem = lines[3].strip(), lines[4].strip()
                if method == 'basic':
                    b_time.append(float(time))
                    b_mem.append(float(mem))
                else:
                    e_time.append(float(time))
                    e_mem.append(float(mem))

    # plot the cpu time
    plt.figure(figsize=(10, 6))
    plt.plot(problem_sizes, b_time, marker='o', label='Basic')
    plt.plot(problem_sizes, e_time, marker='s', label='Efficient')
    plt.xlabel('Problem Size (M + N)')
    plt.ylabel('CPU Time (MS)')
    plt.title('CPU Time vs Problem Size')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(pics_dir, 'time.png'))

    # plot the memory usage
    plt.figure(figsize=(10, 6))
    plt.plot(problem_sizes, b_mem, marker='o', label='Basic')
    plt.plot(problem_sizes, e_mem, marker='s', label='Efficient')
    plt.xlabel('Problem Size (M + N)')
    plt.ylabel('Memory Usage (KB)')
    plt.title('Memory Usage vs Problem Size')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(pics_dir, 'memory.png'))
