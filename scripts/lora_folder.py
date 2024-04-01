import os

ani_tags = ['anime']
real_tags = ['realistic']
Character_tags = ['']
Concept_tags = ['']
Costume_tags = ['']
Sex_tags = ['Sexy']
Style_tags = ['Style']

# 定義目標文件夾
#target_directory = "D:\Lora"

# 選擇您感興趣的特定副檔名（例如 .txt 或 .jpg）
specific_extensions = {".model"}  # 替換為您想要的副檔名

# 篩選出特定副檔名的檔案
for root, dirs, files in os.walk(target_directory):
    results = []
    #print(f"{root} {dirs}")
    for file in files:
        file_path = os.path.join(root, file)
        # 提取檔案副檔名
        file_name = os.path.splitext(file)[0]
        file_name = file_name.replace(".civitai.info", "")
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
                        baseModelKey = "baseModel"
                        if baseModelKey in data["modelVersions"][0]:
                            baseModelValue = data["modelVersions"][0][baseModelKey]
                            
                            tagsKey = "tags"
                            if tagsKey in data:
                                tagsValue = data[tagsKey]
                                
                                print(f"{baseModelValue} {tagsValue}。")
                                isDone = False
                                if baseModelValue=="Pony":
                                    target_folder += "\\pony"
                                elif baseModelValue=="XL":
                                    target_folder += "\\xl"

                                for tag in tags:
                                    if tag in ani_tags:
                                        target_folder += "\\ani"
                                    elif tag in real_tags:
                                        target_folder += "\\real"
                                    else
                                        target_folder += "\\man"
                                        
                                for tag in tags:
                                    if tag in Character_tags:
                                        target_folder += "\\Character"
                                        isDone = True
                                    if tag in Concept_tags:
                                        target_folder += "\\Concept"
                                        isDone = True
                                    if tag in Costume_tags:
                                        target_folder += "\\Costume"
                                        isDone = True
                                    if tag in Sex_tags:
                                        target_folder += "\\Sex"
                                        isDone = True
                                    if tag in Style_tags:
                                        target_folder += "\\Style"
                                        isDone = True

                            print(f"{target_folder}")
                        else:
                            print(f"找不到鍵 {baseModelKey}。")
                    except json.JSONDecodeError:
                        print("無法解析 JSON 文本。")
                    except Exception as e:
                        print(f"處理 JSON 時發生錯誤：{e}")
            except FileNotFoundError:
                print(f"找不到檔案：{file_path}")
            except Exception as e:
                print(f"讀取檔案時發生錯誤：{e}")
    break
