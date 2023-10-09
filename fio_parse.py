#!/usr/bin/env python3

import os
import json
import argparse
import tabulate


class FioResult:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_group(self):
        return self.json_data['jobs'][0]['job options']['name']

    def get_io_type(self):
        return self.json_data['jobs'][0]['job options']['rw']

    def get_io_bs(self):
        return self.json_data['jobs'][0]['job options']['bs']

    def get_read_iops(self):
        return self.json_data['jobs'][0]['read']['iops']

    def get_write_iops(self):
        return self.json_data['jobs'][0]['write']['iops']

    def get_read_bw(self):
        return self.json_data['jobs'][0]['read']['bw']

    def get_write_bw(self):
        return self.json_data['jobs'][0]['write']['bw']

    def get_read_lat(self):
        return self.json_data['jobs'][0]['read']['lat_ns']['mean']

    def get_write_lat(self):
        return self.json_data['jobs'][0]['write']['lat_ns']['mean']


# 中文映射表
trans_map = {
    "read": "顺序读",
    "write": "顺序写",
    "randread": "随机读",
    "randwrite": "随机写",
    "randrw": "随机读写(1:1)"
}


def parse_data(folder_path):
    # 输出内容
    r_dict = {}

    # 获取文件夹下的所有文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 检查文件是否为JSON文件
        if file.endswith('.json'):
            # 获取文件路径
            file_path = os.path.join(folder_path, file)

            # 使用json库读取文件内容
            with open(file_path, 'r') as f:
                data = FioResult(json.load(f))
                if data.get_io_bs() not in r_dict:
                    r_dict[data.get_io_bs()] = []
                r_dict[data.get_io_bs()].append([trans_map[data.get_io_type()], data.get_read_iops(),
                                                data.get_read_bw()/1024, data.get_read_lat()/1000/1000,
                                                data.get_write_iops(), data.get_write_bw()/1024,
                                                data.get_write_lat()/1000/1000])

    # 输出结果
    for io_bs in r_dict:
        table = tabulate.tabulate(r_dict[io_bs], headers=[
                                  f'IO类型({io_bs})', '读iops', '读带宽(MB)', '读延迟(ms)', '写iops', '写带宽(MB)', '写延迟(ms)'], tablefmt='pipe')
        print(table)
        print('\n')


def main():
    parser = argparse.ArgumentParser(description='Parse fio output')
    parser.add_argument('-d', '--output_dir', required=True, type=str, help='fio output dir')
    args = parser.parse_args()
    folder_path = args.output_dir
    parse_data(folder_path)


if __name__ == "__main__":
    main()
