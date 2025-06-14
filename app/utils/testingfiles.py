import os
filedict = {}
for root,dirs,files in os.walk('userdata'):
    for file in files:
        relative_path = os.path.join(root,file)
        filedict[file]=relative_path

print(filedict)