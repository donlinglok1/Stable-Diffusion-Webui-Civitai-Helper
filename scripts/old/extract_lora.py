import os
import json

sts = ["ani","real"]
keys = ["Character","Concept","Custome","Style"]
for st in sts:
    for key in keys:
        input_dir = "C:\\Users\\Kenneth Tu\\git\\stable-diffusion-webui\\models\\Lora\\"+st+"\\"+key
        output_file = "C:\\Users\\Kenneth Tu\\git\\stable-diffusion-webui\\wildcards\\"+st+"\\Lora_"+key+".txt"
        #find ./ -name "*.safetensors"  -printf "%f\n"

        with open(output_file, "w+", encoding='utf-8') as f:
            # Iterate over each file in the input directory
            for filename in os.listdir(input_dir):
                # Check if the file is a civitai.info file
                if filename.endswith(".civitai.info"):
                    with open(input_dir+'\\'+filename) as f2:
                        obj = json.load(f2)
                        str_list = obj["trainedWords"]
                        if len(str_list) > 0 :
                            for x in range(len(str_list)):
                                word = str_list[x]
                                word = word.replace("Please see the description for details",'')
                                word = word.replace("man",'')
                                word = word.replace("gay",'')
                                word = word.replace("penis",'')
                                replaced = '<lora:'+filename.replace(".civitai.info",'')+':0.8> '+word
                                f.write(replaced)
                                f.write("\n")
                        else:
                                replaced = '<lora:'+filename.replace(".civitai.info",'')+':0.8> '+filename.replace(".civitai.info",'')
                                f.write(replaced)
                                f.write("\n")
