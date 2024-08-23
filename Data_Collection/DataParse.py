import json

input_file = "D:/match_data.json"
output_prefix = 'raw_data'

with open(input_file, 'r') as file:
    data = json.load(file)
    
total_lines = 10000
num_files = total_lines // 500 + (1 if total_lines % 500 else 0)

for i in range(num_files):
    start = i * 500
    end = start + 500
    chunk = data[start:end]
    
    output_file = f"{output_prefix}_{i + 1}.json"
    with open(output_file, 'w') as outfile:
        json.dump(chunk, outfile, indent=4)
    print('file made')