#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import json

def run_fio(fio, group_name, device, runtime, io_type, bs):
    # 定义FIO命令
    fio_command = f"{fio} \
--name={group_name} \
--allow_file_create=0 \
--ioengine=libaio \
--filename={device} \
--rw={io_type} \
--iodepth=1 \
--bs={bs} \
--direct=1 \
--numjobs=1 \
--ramp_time=30 \
--runtime={runtime} \
--group_reporting \
--output-format=json \
-o {group_name}/{group_name}_{io_type}_{bs}.json"

    if not os.path.exists(f'./{group_name}'):
        os.mkdir(f'./{group_name}')

    # 运行FIO命令
    result = subprocess.run(fio_command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True, encoding='utf8')

    if result.returncode == 0:
        print(f"FIO task {group_name}_{io_type}_{bs} succeeded")
    else:
        print(f"FIO task {group_name}_{io_type}_{bs} failed")
        print(result.stderr)
        sys.exit(-1)


def main():
    parser = argparse.ArgumentParser(description='Disk fio test')
    parser.add_argument('-f', '--fiopath', default='fio', type=str, help='fio可执行文件路径')
    parser.add_argument('-g', '--group', required=True,type=str, help='测试组名称')
    parser.add_argument('-d', '--device', required=True,type=str, help='设备路径')
    parser.add_argument('-r', '--runtime', required=True, type=int, help='运行时间,单位秒')
    args = parser.parse_args()

    fio = args.fiopath
    group = args.group
    device = args.device
    runtime = args.runtime

    for bs in ['4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k']:
        for io_type in ['read', 'write', 'randread', 'randwrite', 'randrw']:
            run_fio(fio, f"{group}", device, runtime, io_type, bs)


if __name__ == "__main__":
    main()
