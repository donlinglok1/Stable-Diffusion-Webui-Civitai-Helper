import os

# 定義目標文件夾
target_directory = "E:\Lora"

# 選擇您感興趣的特定副檔名（例如 .txt 或 .jpg）
specific_extensions = {".info"}  # 替換為您想要的副檔名

# 篩選出特定副檔名的檔案
for root, dirs, files in os.walk(target_directory):
    results = []
    if(dirs == []):
        print(f"{root} {dirs}")
        for file in files:
            file_path = os.path.join(root, file)
            # 提取檔案副檔名
            file_name = os.path.splitext(file)[0]
            file_name = file_name.replace(".civitai", "")
            file_extension = os.path.splitext(file)[1]
            # 選擇您感興趣的特定副檔名（例如 .txt 或 .jpg）
            if file_extension in specific_extensions:
                try:
                    # 開啟檔案並讀取內容
                    with open(file_path, "r", encoding="utf-8") as file:
                        file_content = file.read()
                        
                        import json
                        # 解析 JSON 文本
                        try:
                            data = json.loads(file_content)
                            # 提取特定的鍵值（例如 "name"）
                            target_key = "trainedWords"
                            if target_key in data:
                                target_value = data[target_key]
                                for trainedWord in target_value:
                                    results.append(f"<lora:{file_name}:1.0> {trainedWord}")
                            else:
                                print(f"找不到鍵 {target_key}。")
                        except json.JSONDecodeError:
                            print("無法解析 JSON 文本。")
                        except Exception as e:
                            print(f"處理 JSON 時發生錯誤：{e}")
                except FileNotFoundError:
                    print(f"找不到檔案：{file_path}")
                except Exception as e:
                    print(f"讀取檔案時發生錯誤：{e}")

        # 定義目標檔案的路徑
        out_prompt_file = root.replace("E:\\Lora", "")
        file_path = "G:\git\stable-diffusion-webui\wildcards"+out_prompt_file+"\pro.txt"  # 替換為您想要創建的檔案路徑

        try:
            # 開啟檔案以寫入模式
            with open(file_path, "w", encoding="utf-8") as file:
                # 逐行寫入字串
                for line in results:
                    file.write(line + "\n")
                print(f"已成功寫入檔案：{file_path}")
        except Exception as e:
            print(f"寫入檔案時發生錯誤：{e}")