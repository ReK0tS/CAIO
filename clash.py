import yaml
import os
from pathlib import Path

# 读取目录下所有的yaml文件，并去重
def read_yaml_files(directory):
    all_proxies = []
    seen_proxies = set()  # 用于去重的集合
    for filename in os.listdir(directory):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if data and 'proxies' in data and isinstance(data['proxies'], list):
                    for proxy in data['proxies']:
                        if proxy['name'] not in seen_proxies:
                            all_proxies.append(proxy)
                            seen_proxies.add(proxy['name'])  # 添加到集合中，用于去重
    return all_proxies

# 创建三种功能的代理组
def create_proxy_groups(proxies):
    return [
        {
            'name': 'Manual Select',
            'type': 'select',
            'proxies': [proxy['name'] for proxy in proxies]
        },
        {
            'name': 'Auto Select',
            'type': 'url-test',
            'proxies': [proxy['name'] for proxy in proxies],
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 600
        },
        {
            'name': 'Failover',
            'type': 'fallback',
            'proxies': [proxy['name'] for proxy in proxies],
            'url': 'http://www.gstatic.com/generate_204',
            'interval': 600
        }
    ]

# 整合所有yaml文件并输出到output.yaml
def integrate_yaml_files(directory, output_path):
    proxies = read_yaml_files(directory)
    if not proxies:
        print("No proxies found. Please check your YAML files.")
        return
    
    proxy_groups = create_proxy_groups(proxies)
    output_config = {
        'proxies': proxies,
        'proxy-groups': proxy_groups
    }
    with open(output_path, 'w', encoding='utf-8') as file:
        yaml.dump(output_config, file, default_flow_style=False)
    print(f"Integrated configuration has been saved to {output_path}")

# 主程序
if __name__ == "__main__":
    directory_path = '/path/'  # 替换为包含yaml文件的目录路径
    output_file_path = '/path/output.yaml'  # 输出文件的路径
    integrate_yaml_files(directory_path, output_file_path)
