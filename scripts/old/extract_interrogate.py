from PIL import Image
import os
import re
import requests
import base64

base_url = 'http://localhost:7861'

def file_to_base64(filename):
    with open(filename, "rb") as file:
        data = file.read()

    base64_str = str(base64.b64encode(data), "utf-8")
    return "data:image/png;base64," + base64_str

def read_file(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())
    return lines

import time

def processImage(filename, output_filep, f, type):
    processedList = read_file(output_filep)

    if filename not in processedList:
        print(filename)
        # Check if the file is a PNG file
        if filename.endswith(".png"):
            # Open the image file
            image_path = os.path.join(filename)
            
            start = time.time()
            payload = {
                "image": file_to_base64(image_path),
                "model": type,
            }
            caption = requests.post(f"{base_url}/sdapi/v1/interrogate", json=payload).json()['caption']
            end = time.time()
            print(end - start)

            # Write the metadata to the text file
            s = caption
            word = re.sub('Negative prompt:.*$','',s)
            word = word.replace("Please see the description for details",'')
            word = word.replace("man",'')
            word = word.replace("gay",'')
            word = word.replace("penis",'')
            f.write(word)
            f.write("\n")
            
            with open(output_filep, "a+", encoding='utf-8') as f2:
                f2.write(filename)
                f2.write("\n")


keys = ['2022read','2023read']
def run(output_file, output_filep, output_file2, type):
    with open(output_file, "a+", encoding='utf-8') as f:
        for key in keys:
            input_dir = "D:\\\stable-diffusion-output\\gallery\\"+key

            for filename in os.listdir(input_dir):
                if os.path.isdir(input_dir+'\\'+filename):
                    for filename2 in os.listdir(input_dir+'\\'+filename):
                        if os.path.isdir(input_dir+'\\'+filename+'\\'+filename2):
                            processImage(filename2, output_filep,  f, type)
                        else:
                            processImage(input_dir+'\\'+filename+'\\'+filename2,  output_filep, f, type)
                else:
                    processImage(input_dir+'\\'+filename, output_filep, f, type)

    # remove duplicate
    lines_seen = set() # holds lines already seen
    outfile = open(output_file2, "w+", encoding='utf-8')
    for line in open(output_file, "r", encoding='utf-8'):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

run(
    "D:\\\stable-diffusion-output\\gallery\\history_deepdanbooru.raw.txt",
    "D:\\\stable-diffusion-output\\gallery\\history_deepdanbooru.processed.txt",
               "C:\\Users\\Kenneth Tu\\git\\stable-diffusion-webui\\wildcards\\history_deepdanbooru.txt",
               "deepdanbooru")

run(
    "D:\\\stable-diffusion-output\\gallery\\history_clip.raw.txt",
    "D:\\\stable-diffusion-output\\gallery\\history_clip.processed.txt",
               "C:\\Users\\Kenneth Tu\\git\\stable-diffusion-webui\\wildcards\\history_clip.txt",
               "clip")