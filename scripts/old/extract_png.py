from PIL import Image
import os
import re

def processImage(filename, f):
    print(filename)
    # Check if the file is a PNG file
    if filename.endswith(".png"):
        # Open the image file
        image_path = os.path.join(filename)
        image = Image.open(image_path)

        # Extract the metadata
        metadata = image.info

        # Write the metadata to the text file
        #f.write(f"File: {filename}\n")
        s = metadata['parameters'].replace('\n','').replace('\r','')
        word = re.sub('Negative prompt:.*$','',s)
        word = word.replace("Please see the description for details",'')
        word = word.replace("man",'')
        word = word.replace("gay",'')
        word = word.replace("penis",'')
        f.write(word)
        f.write("\n")

        # Close the image file
        image.close()

keys = ['2023read', '2022read']
output_file = "D:\\\stable-diffusion-output\\gallery\\history.raw.txt"
output_file2 = "C:\\Users\\Kenneth Tu\\git\\stable-diffusion-webui\\wildcards\\history.txt"

with open(output_file, "w+", encoding='utf-8') as f:
    for key in keys:
        input_dir = "D:\\\stable-diffusion-output\\gallery\\"+key

        for filename in os.listdir(input_dir):
            if os.path.isdir(input_dir+'\\'+filename):
                for filename2 in os.listdir(input_dir+'\\'+filename):
                    if os.path.isdir(input_dir+'\\'+filename+'\\'+filename2):
                        processImage(filename2, f)
                    else:
                        processImage(input_dir+'\\'+filename+'\\'+filename2, f)
            else:
                processImage(input_dir+'\\'+filename, f)

# remove duplicate
lines_seen = set() # holds lines already seen
outfile = open(output_file2, "w+", encoding='utf-8')
for line in open(output_file, "r", encoding='utf-8'):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
