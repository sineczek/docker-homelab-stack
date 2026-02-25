import os

def generate_env_examples_recursive():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.startswith('.env') and not file.endswith('.example'):
                env_path = os.path.join(root, file)
                example_path = env_path + ".example"
                with open(env_path, 'r') as f:
                    lines = f.readlines()

                example_lines = []
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        example_lines.append(line)
                    elif '=' in line:
                        key = line.split('=')[0].strip()
                        example_lines.append(f"{key}=")
                    else:
                        example_lines.append(line)

                with open(example_path, 'w') as f:
                    f.write('\n'.join(example_lines))

    print(".env.example were generated.")

if __name__ == "__main__":
    generate_env_examples_recursive()