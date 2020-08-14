#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import platform
import os
import sys

REPLACE_LIST = [
    ["esp32", "esp32_v3.3"]
]

STDK_REF_PATH = os.path.dirname(os.path.abspath(__file__))
STDK_CORE_PATH = os.path.join(STDK_REF_PATH, "iot-core")

os.environ["STDK_REF_PATH"] = STDK_REF_PATH
os.environ["STDK_CORE_PATH"] = STDK_CORE_PATH

def print_usage():
    print("")
    print("Usage: ./setup.py [BSP_NAME]")
    print("--------------------------------------------------")
    print("  ex) ./build.py esp32_v4.x")
    print("")

def find_setup_script(bsp_name):
    if os.path.exists(os.path.join("tools", bsp_name, "setup_"+bsp_name+".py")):
        return os.path.join("tools", bsp_name, "setup_"+bsp_name+".py")
    if os.path.exists(os.path.join("tools", bsp_name, "setup_"+bsp_name+".sh")):
        return os.path.join("tools", bsp_name, "setup_"+bsp_name+".sh")
    print("Fail to find setup script")
    print_usage()
    exit()

def update_submodule(path):
    cwd = os.getcwd()
    ret_val = os.system("git submodule status " + path + " &> /dev/null")
    if not ret_val:
        os.system("git submodule sync " + path)
        os.system("git submodule init " + path)
        os.system("git submodule update " + path)
        os.chdir(path)
        os.system("git reset --hard HEAD")
        os.chdir(cwd)

update_submodule(STDK_CORE_PATH)

if len(sys.argv) == 1:
    print_usage()
    exit()

BSP_NAME = sys.argv[1]
EXTRA_ARGS = sys.argv[2:]

for item in REPLACE_LIST:
    if BSP_NAME == item[0]:
        BSP_NAME = item[1]

setup_script = find_setup_script(BSP_NAME)

BSP_PATH = os.path.join(STDK_REF_PATH, "bsp", BSP_NAME)
update_submodule(BSP_PATH)

setup_cmd = setup_script + " " + BSP_NAME
for args in EXTRA_ARGS:
    setup_cmd = setup_cmd + " " + args
ret_val = os.system(setup_cmd)
if ret_val:
    print_usage()
