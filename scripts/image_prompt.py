import os

# 定義目標文件夾
target_directory = "E:\stable-diffusion-output\gallery"

# 選擇您感興趣的特定副檔名（例如 .txt 或 .jpg）
specific_extensions = {".png"}  # 替換為您想要的副檔名

results = []

# 篩選出特定副檔名的檔案
for root, dirs, files in os.walk(target_directory):
    results = []
    if(dirs == []):
        #print(f"{root} {dirs}")
        for file in files:
            file_path = os.path.join(root, file)
            # 提取檔案副檔名
            file_name = os.path.splitext(file)[0]
            file_name = file_name.replace(".png", "")
            file_extension = os.path.splitext(file)[1]
            # 選擇您感興趣的特定副檔名（例如 .txt 或 .jpg）
            if file_extension in specific_extensions:
                from PIL import Image

                # 假設您有一個 PNG 圖像的路徑
                image_path = file_path  # 替換為您想要讀取的實際圖像路徑

                def check_image(image):
                    with Image.open(image) as f:
                        #print(f.info)
                        target_key = "parameters"
                        if target_key in f.info:
                            target_value = f.info[target_key]
                            target_value = target_value.split("Negative prompt:")[0]
                            target_value = target_value.replace("\n", "")
                            results.append(f"{target_value}")
                        else:
                            print(f"找不到鍵 {target_key}。")
                            
                check_image(image_path)

file_path = "image_prompt"  # 替換為您想要創建的檔案路徑

try:
    # 開啟檔案以寫入模式
    with open(file_path, "w", encoding="utf-8") as file:
        # 逐行寫入字串
        for line in results:
            file.write(line + "\n")
        print(f"已成功寫入檔案：{file_path}")
except Exception as e:
    print(f"寫入檔案時發生錯誤：{e}")