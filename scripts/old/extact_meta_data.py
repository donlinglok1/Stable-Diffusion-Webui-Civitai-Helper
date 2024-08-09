from PIL import Image
import os
import json
import re

input_dir = "D:\\\stable-diffusion-output\\gallery\\archive\\0630"
output_file = "D:\\\stable-diffusion-output\\gallery\\middle.txt"
output_file2 = "D:\\\stable-diffusion-output\\gallery\\result.txt"

with open(output_file, "w+", encoding='utf-8') as f:
    # Iterate over each file in the input directory
    for filename in os.listdir(input_dir):
        # Check if the file is a PNG file
        if filename.endswith(".png"):
            # Open the image file
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path)

            # Extract the metadata
            metadata = image.info

            # Write the metadata to the text file
            #f.write(f"File: {filename}\n")
            s = metadata['parameters'].replace('\n','').replace('\r','')
            replaced = re.sub('Negative prompt:.*$','',s)
            f.write(replaced)
            f.write("\n")

            # Close the image file
            image.close()

lines_seen = set() # holds lines already seen
outfile = open(output_file2, "w+", encoding='utf-8')
for line in open(output_file, "r", encoding='utf-8'):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()