import os
import json

# Paths and filenames
source_dir = r"C:\Users\amine\bin\github-projects\PiKube-Kubernetes-Cluster\build\prometheus-conf\grafana-kubernetes-dashboards-raw"
destination_dir = r"C:\Users\amine\bin\github-projects\PiKube-Kubernetes-Cluster\build\prometheus-conf"

components = [
    "apiserver",
    "etcd",
    "kubelet",
    "kube-controller-manager",
    "kube-proxy",
    "kube-scheduler"
]

new_job = "kubelet"

# For Linux
# input_file_path = '/home/user/original/dashboard.json'
# output_file_path = '/home/user/modified/dashboard.json'

# For Windows
# In the script (using raw strings):
# input_file_path = r'C:\Users\user\original\dashboard.json'
# output_file_path = r'C:\Users\user\modified\dashboard.json'
#
# Or, using escape characters:
#
# input_file_path = 'C:\\Users\\user\\original\\dashboard.json'
# output_file_path = 'C:\\Users\\user\\modified\\dashboard.json'

new_job = "kubelet"

# # Process each dashboard file
# for component in components:
#     source_file = f"{source_path}/grafana-kubernetes-{component}-dashboard-raw.json"
#     destination_file = f"{destination_path}/grafana-kubernetes-{component}-dashboard.json"

#     try:
#         # Read the JSON data
#         with open(source_file, 'r') as file:
#             data = json.load(file)

#         # Modify the 'expr' field in each target in the JSON
#         count = 0
#         for panel in data.get('panels', []):
#             if 'targets' in panel:
#                 for target in panel['targets']:
#                     if 'expr' in target:
#                         expr = target['expr']
#                         # Check and replace the job label
#                         for comp in components:
#                             if f'job="{comp}"' in expr:
#                                 target['expr'] = expr.replace(f'job="{comp}"', f'job="{new_job}"')
#                                 count += 1

#         # Write the modified data back to a new file
#         with open(destination_file, 'w') as file:
#             json.dump(data, file, indent=4)

#         print(f"Processed {component}: {count} modifications made.")

#     except FileNotFoundError:
#         print(f"File not found: {source_file}")

# Function to process each file
def process_dashboard(component):
    filename = f"grafana-kubernetes-{component}-dashboard-raw.json"
    source_file = os.path.join(source_dir, filename)
    destination_file = os.path.join(destination_dir, filename.replace("-raw", ""))

    # Initialize modification count
    modification_count = 0

    # Read and modify the JSON file
    try:
        with open(source_file, 'r', encoding='utf-8') as file:
            data = file.read()
            modified_data = data.replace(f'job="{component}"', f'job="{new_job}"').replace(f'job=\"{component}\"', f'job=\"{new_job}\"').replace(f'job=\\"{component}\\"', f'job=\\"{new_job}\\"')

            # Count modifications
            modification_count = data.count(f'job="{component}"') + data.count(f'job=\"{component}\"')

        # Write the modified JSON back to a new file
        with open(destination_file, 'w', encoding='utf-8') as file:
            file.write(modified_data)
        print(f"Processed {filename}. Modifications made: {modification_count}")
    except FileNotFoundError as e:
        print(f"File not found: {source_file}. Please check the file path and name.")
    except Exception as e:
        print(f"An error occurred while processing {filename}: {e}")

# Process each component
for component in components:
    process_dashboard(component)