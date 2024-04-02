import os

# 定義目標文件夾
target_directory = "D:\Lora"

# 選擇您感興趣的特定副檔名（例如 .txt 或 .jpg）
specific_extensions = {".safetensors"}  # 替換為您想要的副檔名

# 篩選出特定副檔名的檔案
for root, dirs, files in os.walk(target_directory):
    results = []
    if(dirs == []):
        print(f"{root} {dirs}")
        for file in files:
            file_path = os.path.join(root, file)
            # 提取檔案副檔名
            file_name = os.path.splitext(file)[0]
            file_name = file_name.replace(".safetensors", "")
            file_extension = os.path.splitext(file)[1]
            # 選擇您感興趣的特定副檔名（例如 .txt 或 .jpg）
            if file_extension in specific_extensions:
                if not os.path.exists(root+"\\"+file_name+".preview.png"):
                    import os
                    os.remove(root+"\\"+file_name+".safetensors")
                    os.remove(root+"\\"+file_name+".civitai.info")
                    os.remove(root+"\\"+file_name+".civitai.info.model")