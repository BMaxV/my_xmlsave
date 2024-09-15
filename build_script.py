import subprocess
import os
# does this change working directory?

build=["rm -r dist",
    "python3 -m build --no-isolation -C--quiet",]
    #"cd dist/",
install=[
    "pip3 install my_save_function-0.1-py3-none-any.whl --force"
    ]

for x in build:
    a=x.split(" ")
    subprocess.run(a)

os.chdir("dist")

for x in install:
    a=x.split(" ")
    subprocess.run(a)
