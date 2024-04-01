import os

# 定義目標文件夾
targets = [
]

for file in targets:
    file = file.replace(".safetensors", "")
    import os
    os.remove(file+".safetensors")
    os.remove(file+".civitai.info")
    os.remove(file+".civitai.info.model")
    os.remove(file+".preview.png")