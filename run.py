import os
import re
import subprocess


if __name__ == '__main__':
    input_dir = 'input'
    output_dir = 'output'
    filenames = os.listdir(input_dir)
    filenames = [f for f in filenames if not f.startswith('.') and os.path.isfile(os.path.join(input_dir, f))]

    pattern = re.compile(r"in(\d+)\.txt")
    for filename in filenames:
        match = pattern.match(filename)
        if match:
            num = match.group(1)
            input_path  = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f'out{num}_basic.txt')
            subprocess.run(['./basic.sh', input_path, output_path], check=True)
            output_path = os.path.join(output_dir, f'out{num}_effic.txt')
            subprocess.run(['./efficient.sh', input_path, output_path], check=True)
