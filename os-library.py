import os

print("current directory:",os.getcwd()) 
if not os.path.exists("new_dir"):
    os.mkdir("new_dir")

os.chdir("new_dir")

print("current directory:",os.getcwd()) 
