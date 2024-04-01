# -*- coding: UTF-8 -*-
# This extension can help you manage your models from civitai. It can download preview, add trigger words, open model page and use the prompt from preview image
# repo: https://github.com/butaixianran/



import gradio as gr
import os

# -*- coding: UTF-8 -*-
# handle msg between js and python side
import os
import time
from ch_lib import util

# -*- coding: UTF-8 -*-
# handle msg between js and python side
import os
import json


# this is the default root path
root_path = os.getcwd()

# if command line arguement is used to change model folder, 
# then model folder is in absolute path, not based on this root path anymore.
# so to make extension work with those absolute model folder paths, model folder also need to be in absolute path
folders = {
    "ti": os.path.join(root_path, "embeddings"),
    "hyper": os.path.join(root_path, "models", "hypernetworks"),
    "ckp": os.path.join(root_path, "models", "Stable-diffusion"),
    "lora": os.path.join(root_path, "models", "Lora"),
}

exts = (".bin", ".pt", ".safetensors", ".ckpt")
info_ext = ".info"
vae_suffix = ".vae"


# get cusomter model path
def get_custom_model_folder():
    util.printD("Get Custom Model Folder")

    global folders

    if shared.cmd_opts.embeddings_dir and os.path.isdir(shared.cmd_opts.embeddings_dir):
        folders["ti"] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir and os.path.isdir(shared.cmd_opts.hypernetwork_dir):
        folders["hyper"] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir and os.path.isdir(shared.cmd_opts.ckpt_dir):
        folders["ckp"] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir and os.path.isdir(shared.cmd_opts.lora_dir):
        folders["lora"] = shared.cmd_opts.lora_dir





# write model info to file
def write_model_info(path, model_info):
    util.printD("Write model info to file: " + path)
    with open(os.path.realpath(path), 'w') as f:
        f.write(json.dumps(model_info, indent=4))


def load_model_info(path):
    # util.printD("Load model info from file: " + path)
    model_info = None
    with open(os.path.realpath(path), 'r') as f:
        try:
            model_info = json.load(f)
        except Exception as e:
            util.printD("Selected file is not json: " + path)
            util.printD(e)
            return
        
    return model_info


# -*- coding: UTF-8 -*-
# handle msg between js and python side
import os
import time
import json
import re
import requests

suffix = ".civitai"

url_dict = {
    "modelPage":"https://civitai.com/models/",
    "modelId": "https://civitai.com/api/v1/models/",
    "modelVersionId": "https://civitai.com/api/v1/model-versions/",
    "hash": "https://civitai.com/api/v1/model-versions/by-hash/"
}

model_type_dict = {
    "Checkpoint": "ckp",
    "TextualInversion": "ti",
    "Hypernetwork": "hyper",
    "LORA": "lora",
    "LoCon": "lora",
}



# get image with full size
# width is in number, not string
# return: url str
def get_full_size_image_url(image_url, width):
    return re.sub('/width=\d+/', '/width=' + str(width) + '/', image_url)


# use this sha256 to get model info from civitai
# return: model info dict
def get_model_info_by_hash(hash:str):
    util.printD("Request model info from civitai")

    if not hash:
        util.printD("hash is empty")
        return

    r = requests.get(url_dict["hash"]+hash, headers=util.def_headers, proxies=util.proxies)
    if not r.ok:
        if r.status_code == 404:
            # this is not a civitai model
            util.printD("Civitai does not have this model")
            return {}
        else:
            util.printD("Get error code: " + str(r.status_code))
            util.printD(r.text)
            return

    # try to get content
    content = None
    try:
        content = r.json()
    except Exception as e:
        util.printD("Parse response json failed")
        util.printD(str(e))
        util.printD("response:")
        util.printD(r.text)
        return
    
    if not content:
        util.printD("error, content from civitai is None")
        return
    
    return content



def get_model_info_by_id(id:str) -> dict:
    util.printD("Request model info from civitai")

    if not id:
        util.printD("id is empty")
        return

    r = requests.get(url_dict["modelId"]+str(id), headers=util.def_headers, proxies=util.proxies)
    if not r.ok:
        if r.status_code == 404:
            # this is not a civitai model
            util.printD("Civitai does not have this model")
            return {}
        else:
            util.printD("Get error code: " + str(r.status_code))
            util.printD(r.text)
            return

    # try to get content
    content = None
    try:
        content = r.json()
    except Exception as e:
        util.printD("Parse response json failed")
        util.printD(str(e))
        util.printD("response:")
        util.printD(r.text)
        return
    
    if not content:
        util.printD("error, content from civitai is None")
        return
    
    return content


def get_version_info_by_version_id(id:str) -> dict:
    util.printD("Request version info from civitai")

    if not id:
        util.printD("id is empty")
        return

    r = requests.get(url_dict["modelVersionId"]+str(id), headers=util.def_headers, proxies=util.proxies)
    if not r.ok:
        if r.status_code == 404:
            # this is not a civitai model
            util.printD("Civitai does not have this model version")
            return {}
        else:
            util.printD("Get error code: " + str(r.status_code))
            util.printD(r.text)
            return

    # try to get content
    content = None
    try:
        content = r.json()
    except Exception as e:
        util.printD("Parse response json failed")
        util.printD(str(e))
        util.printD("response:")
        util.printD(r.text)
        return
    
    if not content:
        util.printD("error, content from civitai is None")
        return
    
    return content


def get_version_info_by_model_id(id:str) -> dict:

    model_info = get_model_info_by_id(id)
    if not model_info:
        util.printD(f"Failed to get model info by id: {id}")
        return
    
    # check content to get version id
    if "modelVersions" not in model_info.keys():
        util.printD("There is no modelVersions in this model_info")
        return
    
    if not model_info["modelVersions"]:
        util.printD("modelVersions is None")
        return
    
    if len(model_info["modelVersions"])==0:
        util.printD("modelVersions is Empty")
        return
    
    def_version = model_info["modelVersions"][0]
    if not def_version:
        util.printD("default version is None")
        return
    
    if "id" not in def_version.keys():
        util.printD("default version has no id")
        return
    
    version_id = def_version["id"]
    
    if not version_id:
        util.printD("default version's id is None")
        return

    # get version info
    version_info = get_version_info_by_version_id(str(version_id))
    if not version_info:
        util.printD(f"Failed to get version info by version_id: {version_id}")
        return

    return version_info




# get model info file's content by model type and search_term
# parameter: model_type, search_term
# return: model_info
def load_model_info_by_search_term(model_type, search_term):
    util.printD(f"Load model info of {search_term} in {model_type}")
    # if model_type not in model.folders.keys():
    if model_type not in folders.keys():
        util.printD("unknow model type: " + model_type)
        return
    
    # search_term = subfolderpath + model name + ext. And it always start with a / even there is no sub folder
    base, ext = os.path.splitext(search_term)
    model_info_base = base
    if base[:1] == "/":
        model_info_base = base[1:]

    # model_folder = model.folders[model_type]
    # model_info_filename = model_info_base + suffix + model.info_ext
    model_folder = folders[model_type]
    model_info_filename = model_info_base + suffix + info_ext
    model_info_filepath = os.path.join(model_folder, model_info_filename)

    if not os.path.isfile(model_info_filepath):
        util.printD("Can not find model info file: " + model_info_filepath)
        return
    
    # return model.load_model_info(model_info_filepath)
    return load_model_info(model_info_filepath)





# get model file names by model type
# parameter: model_type - string
# parameter: filter - dict, which kind of model you need
# return: model name list
def get_model_names_by_type_and_filter(model_type:str, filter:dict) -> list:
    
    # model_folder = model.folders[model_type]
    model_folder = folders[model_type]

    # set filter
    # only get models don't have a civitai info file
    no_info_only = False
    empty_info_only = False

    if filter:
        if "no_info_only" in filter.keys():
            no_info_only = filter["no_info_only"]
        if "empty_info_only" in filter.keys():
            empty_info_only = filter["empty_info_only"]



    # get information from filter
    # only get those model names don't have a civitai model info file
    model_names = []
    for root, dirs, files in os.walk(model_folder, followlinks=True):
        for filename in files:
            item = os.path.join(root, filename)
            # check extension
            base, ext = os.path.splitext(item)
            # if ext in model.exts:
            if ext in exts:
                # find a model

                # check filter
                if no_info_only:
                    # check model info file
                    # info_file = base + suffix + model.info_ext
                    info_file = base + suffix + info_ext
                    if os.path.isfile(info_file):
                        continue

                if empty_info_only:
                    # check model info file
                    # info_file = base + suffix + model.info_ext
                    info_file = base + suffix + info_ext
                    if os.path.isfile(info_file):
                        # load model info
                        # model_info = model.load_model_info(info_file)
                        model_info = load_model_info(info_file)
                        # check content
                        if model_info:
                            if "id" in model_info.keys():
                                # find a non-empty model info file
                                continue

                model_names.append(filename)


    return model_names

def get_model_names_by_input(model_type, empty_info_only):
    return get_model_names_by_type_and_filter(model_type, {"empty_info_only":empty_info_only})
    

# get id from url
def get_model_id_from_url(url:str) -> str:
    util.printD("Run get_model_id_from_url")
    id = ""

    if not url:
        util.printD("url or model id can not be empty")
        return ""

    if url.isnumeric():
        # is already an id
        id = str(url)
        return id
    
    s = re.sub("\\?.+$", "", url).split("/")
    if len(s) < 2:
        util.printD("url is not valid")
        return ""
    
    if s[-2].isnumeric():
        id  = s[-2]
    elif s[-1].isnumeric():
        id  = s[-1]
    else:
        util.printD("There is no model id in this url")
        return ""
    
    return id


# get preview image by model path
# image will be saved to file, so no return
def get_preview_image_by_model_path(model_path:str, max_size_preview, skip_nsfw_preview):
    if not model_path:
        util.printD("model_path is empty")
        return

    if not os.path.isfile(model_path):
        util.printD("model_path is not a file: "+model_path)
        return

    base, ext = os.path.splitext(model_path)
    first_preview = base+".png"
    sec_preview = base+".preview.png"
    # info_file = base + suffix + model.info_ext
    info_file = base + suffix + info_ext

    # check preview image
    if not os.path.isfile(sec_preview):
        # need to download preview image
        util.printD("Checking preview image for model: " + model_path)
        # load model_info file
        if os.path.isfile(info_file):
            # model_info = model.load_model_info(info_file)
            model_info = load_model_info(info_file)
            if not model_info:
                util.printD("Model Info is empty")
                return

            if "images" in model_info.keys():
                if model_info["images"]:
                    for img_dict in model_info["images"]:
                        if "nsfw" in img_dict.keys():
                            if img_dict["nsfw"] and img_dict["nsfw"] != "None":
                                util.printD("This image is NSFW")
                                if skip_nsfw_preview:
                                    util.printD("Skip NSFW image")
                                    continue
                        
                        if "url" in img_dict.keys():
                            img_url = img_dict["url"]
                            if max_size_preview:
                                # use max width
                                if "width" in img_dict.keys():
                                    if img_dict["width"]:
                                        img_url = get_full_size_image_url(img_url, img_dict["width"])

                            util.download_file(img_url, sec_preview)
                            # we only need 1 preview image
                            break



# search local model by version id in 1 folder, no subfolder
# return - model_info
def search_local_model_info_by_version_id(folder:str, version_id:int) -> dict:
    util.printD("Searching local model by version id")
    util.printD("folder: " + folder)
    util.printD("version_id: " + str(version_id))

    if not folder:
        util.printD("folder is none")
        return

    if not os.path.isdir(folder):
        util.printD("folder is not a dir")
        return
    
    if not version_id:
        util.printD("version_id is none")
        return
    
    # search civitai model info file
    for filename in os.listdir(folder):
        # check ext
        base, ext = os.path.splitext(filename)
        # if ext == model.info_ext:
        if ext == info_ext:
            # find info file
            if len(base) < 9:
                # not a civitai info file
                continue

            if base[-8:] == suffix:
                # find a civitai info file
                path = os.path.join(folder, filename)
                # model_info = model.load_model_info(path)
                model_info = load_model_info(path)
                if not model_info:
                    continue

                if "id" not in model_info.keys():
                    continue

                id = model_info["id"]
                if not id:
                    continue

                # util.printD(f"Compare version id, src: {id}, target:{version_id}")
                if str(id) == str(version_id):
                    # find the one
                    return model_info
                    

    return





# check new version for a model by model path
# return (model_path, model_id, model_name, new_verion_id, new_version_name, description, download_url, img_url)
def check_model_new_version_by_path(model_path:str, delay:float=1) -> tuple:
    if not model_path:
        util.printD("model_path is empty")
        return

    if not os.path.isfile(model_path):
        util.printD("model_path is not a file: "+model_path)
        return
    
    # get model info file name
    base, ext = os.path.splitext(model_path)
    # info_file = base + suffix + info_ext
    info_file = base + suffix + model.info_ext
    
    if not os.path.isfile(info_file):
        return
    
    # get model info
    # model_info_file = model.load_model_info(info_file)
    model_info_file = load_model_info(info_file)
    if not model_info_file:
        return

    if "id" not in model_info_file.keys():
        return
    
    local_version_id = model_info_file["id"]
    if not local_version_id:
        return

    if "modelId" not in model_info_file.keys():
        return
    
    model_id = model_info_file["modelId"]
    if not model_id:
        return
    
    # get model info by id from civitai
    model_info = get_model_info_by_id(model_id)
    # delay before next request, to prevent to be treat as DDoS 
    util.printD(f"delay:{delay} second")
    time.sleep(delay)

    if not model_info:
        return
    
    if "modelVersions" not in model_info.keys():
        return
    
    modelVersions = model_info["modelVersions"]
    if not modelVersions:
        return
    
    if not len(modelVersions):
        return
    
    current_version = modelVersions[0]
    if not current_version:
        return
    
    if "id" not in current_version.keys():
        return
    
    current_version_id = current_version["id"]
    if not current_version_id:
        return

    util.printD(f"Compare version id, local: {local_version_id}, remote: {current_version_id} ")
    if current_version_id == local_version_id:
        return

    model_name = ""
    if "name" in model_info.keys():
        model_name = model_info["name"]
    
    if not model_name:
        model_name = ""


    new_version_name = ""
    if "name" in current_version.keys():
        new_version_name = current_version["name"]
    
    if not new_version_name:
        new_version_name = ""

    description = ""
    if "description" in current_version.keys():
        description = current_version["description"]
    
    if not description:
        description = ""

    downloadUrl = ""
    if "downloadUrl" in current_version.keys():
        downloadUrl = current_version["downloadUrl"]
    
    if not downloadUrl:
        downloadUrl = ""

    # get 1 preview image
    img_url = ""
    if "images" in current_version.keys():
        if current_version["images"]:
            if current_version["images"][0]:
                if "url" in current_version["images"][0].keys():
                    img_url = current_version["images"][0]["url"]
                    if not img_url:
                        img_url = ""


    
    return (model_path, model_id, model_name, current_version_id, new_version_name, description, downloadUrl, img_url)




# check model's new version
# parameter: delay - float, how many seconds to delay between each request to civitai
# return: new_versions - a list for all new versions, each one is (model_path, model_id, model_name, new_verion_id, new_version_name, description, download_url, img_url)
def check_models_new_version_by_model_types(model_types:list, delay:float=1) -> list:
    util.printD("Checking models' new version")

    if not model_types:
        return []

    # check model types, which cloud be a string as 1 type
    mts = []
    if type(model_types) == str:
        mts.append(model_types)
    elif type(model_types) == list:
        mts = model_types
    else:
        util.printD("Unknow model types:")
        util.printD(model_types)
        return []

    # output is a markdown document string to show a list of new versions on UI
    output = ""
    # new version list
    new_versions = []

    # walk all models
    # for model_type, model_folder in model.folders.items():
    for model_type, model_folder in folders.items():
        if model_type not in mts:
            continue

        util.printD("Scanning path: " + model_folder)
        for root, dirs, files in os.walk(model_folder, followlinks=True):
            for filename in files:
                # check ext
                item = os.path.join(root, filename)
                base, ext = os.path.splitext(item)
                # if ext in model.exts:
                if ext in exts:
                    # find a model
                    r = check_model_new_version_by_path(item, delay)

                    if not r:
                        continue

                    model_path, model_id, model_name, current_version_id, new_version_name, description, downloadUrl, img_url = r
                    # check exist
                    if not current_version_id:
                        continue

                    # check this version id in list
                    is_already_in_list = False
                    for new_version in new_versions:
                        if current_version_id == new_version[3]:
                            # already in list
                            is_already_in_list = True
                            break

                    if is_already_in_list:
                        util.printD("New version is already in list")
                        continue

                    # search this new version id to check if this model is already downloaded
                    target_model_info = search_local_model_info_by_version_id(root, current_version_id)
                    if target_model_info:
                        util.printD("New version is already existed")
                        continue

                    # add to list
                    new_versions.append(r)




    return new_versions




from ch_lib import downloader




# get model info by url
def get_model_info_by_url(model_url_or_id:str) -> tuple:
    util.printD("Getting model info by: " + model_url_or_id)

    # parse model id
    model_id = get_model_id_from_url(model_url_or_id)
    if not model_id:
        util.printD("failed to parse model id from url or id")
        return    

    model_info = get_model_info_by_id(model_id)
    if model_info is None:
        util.printD("Connect to Civitai API service failed. Wait a while and try again")
        import time
        time.sleep(10)
        return get_model_info_by_url(model_url_or_id)
    
    if not model_info:
        util.printD("failed to get model info from url or id")
        return
    
    # parse model type, model name, subfolder, version from this model info
    # get model type
    if "type" not in model_info.keys():
        util.printD("model type is not in model_info")
        return
    
    civitai_model_type = model_info["type"]
    if civitai_model_type not in model_type_dict.keys():
        util.printD("This model type is not supported:"+civitai_model_type)
        return
    
    model_type = model_type_dict[civitai_model_type]

    # get model type
    if "name" not in model_info.keys():
        util.printD("model name is not in model_info")
        return

    model_name = model_info["name"]
    if not model_name:
        util.printD("model name is Empty")
        model_name = ""

    # get version list
    if "modelVersions" not in model_info.keys():
        util.printD("modelVersions is not in model_info")
        return
    
    modelVersions = model_info["modelVersions"]
    if not modelVersions:
        util.printD("modelVersions is Empty")
        return
    
    version_strs = []
    for version in modelVersions:
        # version name can not be used as id
        # version id is not readable
        # so , we use name_id as version string
        version_str = version["name"]+"_"+str(version["id"])
        version_strs.append(version_str)

    # get folder by model type
    folder = folders[model_type]
    # get subfolders
    subfolders = util.get_subfolders(folder)
    if not subfolders:
        subfolders = []

    # add default root folder
    subfolders.append("/")

    util.printD("Get following info for downloading:")
    util.printD(f"model_name:{model_name}")
    util.printD(f"model_type:{model_type}")
    util.printD(f"subfolders:{subfolders}")
    util.printD(f"version_strs:{version_strs}")

    return (model_info, model_name, model_type, subfolders, version_strs)

# get version info by version string
def get_ver_info_by_ver_str(version_str:str, model_info:dict) -> dict:
    if not version_str:
        util.printD("version_str is empty")
        return
    
    if not model_info:
        util.printD("model_info is None")
        return
    
    # get version list
    if "modelVersions" not in model_info.keys():
        util.printD("modelVersions is not in model_info")
        return

    modelVersions = model_info["modelVersions"]
    if not modelVersions:
        util.printD("modelVersions is Empty")
        return
    
    # find version by version_str
    version = None
    for ver in modelVersions:
        # version name can not be used as id
        # version id is not readable
        # so , we use name_id as version string
        ver_str = ver["name"]+"_"+str(ver["id"])
        if ver_str == version_str:
            # find version
            version = ver

    if not version:
        util.printD("can not find version by version string: " + version_str)
        return
    
    # get version id
    if "id" not in version.keys():
        util.printD("this version has no id")
        return
    
    return version


# download model from civitai by input
# output to markdown log
def dl_model_by_input(model_info:dict, model_type:str, subfolder_str:str, version_str:str, dl_all_bool:bool, max_size_preview:bool, skip_nsfw_preview:bool) -> str:

    output = ""

    if not model_info:
        output = "model_info is None"
        util.printD(output)
        return output
    
    if not model_type:
        output = "model_type is None"
        util.printD(output)
        return output
    
    if not subfolder_str:
        output = "subfolder string is None"
        util.printD(output)
        return output
    
    if not version_str:
        output = "version_str is None"
        util.printD(output)
        return output
    
    # get model root folder
    if model_type not in folders.keys():
        output = "Unknow model type: "+model_type
        util.printD(output)
        return output
    
    model_root_folder = folders[model_type]


    # get subfolder
    subfolder = ""
    if subfolder_str == "/" or subfolder_str == "\\":
        subfolder = ""
    elif subfolder_str[:1] == "/" or subfolder_str[:1] == "\\":
        subfolder = subfolder_str[1:]
    else:
        subfolder = subfolder_str

    # get model folder for downloading
    model_folder = os.path.join(model_root_folder, subfolder)
    if not os.path.isdir(model_folder):
        output = "Model folder is not a dir: "+ model_folder
        util.printD(output)
        return output
    
    # get version info
    ver_info = get_ver_info_by_ver_str(version_str, model_info)
    if not ver_info:
        output = "Fail to get version info, check console log for detail"
        util.printD(output)
        return output
    
    version_id = ver_info["id"]


    if dl_all_bool:
        # get all download url from files info
        # some model versions have multiple files
        download_urls = []
        if "files" in ver_info.keys():
            for file_info in ver_info["files"]:
                if "downloadUrl" in file_info.keys():
                    download_urls.append(file_info["downloadUrl"])

        if not len(download_urls):
            if "downloadUrl" in ver_info.keys():
                download_urls.append(ver_info["downloadUrl"])


        # check if this model is already existed
        r = search_local_model_info_by_version_id(model_folder, version_id)
        if r:
            output = "This model version is already existed"
            util.printD(output)
            return output
        
        # download
        filepath = ""
        for url in download_urls:
            model_filepath = downloader.dl(url, model_folder, None, None)
            if not model_filepath:
                output = "Downloading failed, check console log for detail"
                util.printD(output)
                return output
            
            if url == ver_info["downloadUrl"]:
                filepath = model_filepath
    else:
        # only download one file
        # get download url
        try:
            url = ver_info["downloadUrl"]
            if not url:
                output = "Fail to get download url, check console log for detail"
                util.printD(output)
                return output
            
            # download
            filepath = downloader.dl(url, model_folder, None, None)
            if not filepath:
                output = "Downloading failed, check console log for detail"
                util.printD(output)
                return output
        except Exception as e:
            output = "Downloading failed, check console log for detail"
            util.printD(output)
            return output


    if not filepath:
        filepath = model_filepath
    
    # get version info
    version_info = get_version_info_by_version_id(version_id)
    if not version_info:
        output = "Model downloaded, but failed to get version info, check console log for detail. Model saved to: " + filepath
        util.printD(output)
        return output

    # write version info to file
    base, ext = os.path.splitext(filepath)
    info_file = base + suffix + info_ext
    write_model_info(info_file, version_info)
    try:
        info_model_file = base + suffix + info_ext + + ".model" 
        write_model_info(info_model_file, model_info)
    except Exception as e:
        util.printD(e)

    # then, get preview image
    get_preview_image_by_model_path(filepath, max_size_preview, skip_nsfw_preview)
    
    output = "Done. Model downloaded to: " + filepath
    util.printD(output)
    return output


# init

# root path
root_path = os.getcwd()

# extension path
#extension_path = scripts.basedir()

#model.get_custom_model_folder()


# Setting now can not be saved from extension tab
# All settings now must be saved from setting page.
def on_ui_settings():
    ch_section = ("civitai_helper", "Civitai Helper")
    # settings
    shared.opts.add_option("ch_max_size_preview", shared.OptionInfo(True, "Download Max Size Preview", gr.Checkbox, {"interactive": True}, section=ch_section))
    shared.opts.add_option("ch_skip_nsfw_preview", shared.OptionInfo(False, "Skip NSFW Preview Images", gr.Checkbox, {"interactive": True}, section=ch_section))
    shared.opts.add_option("ch_open_url_with_js", shared.OptionInfo(True, "Open Url At Client Side", gr.Checkbox, {"interactive": True}, section=ch_section))
    shared.opts.add_option("ch_proxy", shared.OptionInfo("", "Civitai Helper Proxy", gr.Textbox, {"interactive": True, "lines":1, "info":"format: socks5h://127.0.0.1:port"}, section=ch_section))
    shared.opts.add_option("ch_civiai_api_key", shared.OptionInfo("", "Civitai API Key", gr.Textbox, {"interactive": True, "lines":1, "info":"check doc:https://github.com/zixaphir/Stable-Diffusion-Webui-Civitai-Helper/tree/master#api-key"}, section=ch_section))

def on_ui_tabs():
    # init
    # init_py_msg = {
    #     # relative extension path
    #     "extension_path": util.get_relative_path(extension_path, root_path),
    # }
    # init_py_msg_str = json.dumps(init_py_msg)


    # get prompt textarea
    # check modules/ui.py, search for txt2img_paste_fields
    # Negative prompt is the second element
    #txt2img_prompt = modules.ui.txt2img_paste_fields[0][0]
    #txt2img_neg_prompt = modules.ui.txt2img_paste_fields[1][0]
    #img2img_prompt = modules.ui.img2img_paste_fields[0][0]
    #img2img_neg_prompt = modules.ui.img2img_paste_fields[1][0]


    # # get settings
    # max_size_preview = shared.opts.data.get("ch_max_size_preview", True)
    # skip_nsfw_preview = shared.opts.data.get("ch_skip_nsfw_preview", False)
    # open_url_with_js = shared.opts.data.get("ch_open_url_with_js", True)
    # proxy = shared.opts.data.get("ch_proxy", "")
    # civitai_api_key = shared.opts.data.get("ch_civiai_api_key", "")

    # util.printD("Settings:")
    # util.printD("max_size_preview: " + str(max_size_preview))
    # util.printD("skip_nsfw_preview: " + str(skip_nsfw_preview))
    # util.printD("open_url_with_js: " + str(open_url_with_js))
    # util.printD("proxy: " + str(proxy))

    # # set civitai_api_key
    # has_api_key = False
    # if civitai_api_key:
    #     has_api_key = True
    #     util.civitai_api_key = civitai_api_key
    #     util.def_headers["Authorization"] = f"Bearer {civitai_api_key}"

    # util.printD(f"use civitai api key: {has_api_key}")

    # # set proxy
    # if proxy:
    #     util.proxies = {
    #         "http": proxy,
    #         "https": proxy,
    #     }


    # # ====Event's function====
    # def scan_model(scan_model_types):
    #     return model_action_civitai.scan_model(scan_model_types, max_size_preview, skip_nsfw_preview)
    
    # def get_model_info_by_input(model_type_drop, model_name_drop, model_url_or_id_txtbox):
    #     return model_action_civitai.get_model_info_by_input(model_type_drop, model_name_drop, model_url_or_id_txtbox, max_size_preview, skip_nsfw_preview)

    # def dl_model_by_input(dl_model_info, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop, dl_all_ckb):
    #     return model_action_civitai.dl_model_by_input(dl_model_info, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop, dl_all_ckb, max_size_preview, skip_nsfw_preview)

    # def check_models_new_version_to_md(dl_model_info, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop, dl_all_ckb):
    #     return model_action_civitai.check_models_new_version_to_md(dl_model_info, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop, dl_all_ckb, max_size_preview, skip_nsfw_preview)

    # def open_model_url(js_msg_txtbox):
    #     return js_action_civitai.open_model_url(js_msg_txtbox, open_url_with_js)

    # def dl_model_new_version(js_msg_txtbox, max_size_preview):
    #     return js_action_civitai.dl_model_new_version(js_msg_txtbox, max_size_preview, skip_nsfw_preview)


    # def get_model_names_by_input(model_type, empty_info_only):
    #     names = civitai.get_model_names_by_input(model_type, empty_info_only)
    #     return model_name_drop.update(choices=names)

    # def get_model_info_by_url(url):
    #     r = model_action_civitai.get_model_info_by_url(url)

    #     model_info = {}
    #     model_name = ""
    #     model_type = ""
    #     subfolders = []
    #     version_strs = []
    #     if r:
    #         model_info, model_name, model_type, subfolders, version_strs = r

    #     return [model_info, model_name, model_type, dl_subfolder_drop.update(choices=subfolders), dl_version_drop.update(choices=version_strs)]

    # ====UI====
    with gr.Blocks(analytics_enabled=False) as civitai_helper:

        # model_types = list(model.folders.keys())
        # no_info_model_names = civitai.get_model_names_by_input("ckp", False)

        # # session data
        # dl_model_info = gr.State({})



        with gr.Box(elem_classes="ch_box"):
            with gr.Column():
                gr.Markdown("### Scan Models for Civitai")
                # with gr.Row():
                #     scan_model_types_ckbg = gr.CheckboxGroup(choices=model_types, label="Model Types", value=model_types)

                # # with gr.Row():
                # scan_model_civitai_btn = gr.Button(value="Scan", variant="primary", elem_id="ch_scan_model_civitai_btn")
                # # with gr.Row():
                # scan_model_log_md = gr.Markdown(value="Scanning takes time, just wait. Check console log for detail", elem_id="ch_scan_model_log_md")

        
        with gr.Box(elem_classes="ch_box"):
            with gr.Column():
                gr.Markdown("### Get Model Info from Civitai by URL")
                gr.Markdown("Use this when scanning can not find a local model on civitai")
                # with gr.Row():
                #     model_type_drop = gr.Dropdown(choices=model_types, label="Model Type", value="ckp", multiselect=False)
                #     empty_info_only_ckb = gr.Checkbox(label="Only Show Models have no Info", value=False, elem_id="ch_empty_info_only_ckb", elem_classes="ch_vpadding")
                #     model_name_drop = gr.Dropdown(choices=no_info_model_names, label="Model", value="ckp", multiselect=False)

                # model_url_or_id_txtbox = gr.Textbox(label="Civitai URL", lines=1, value="")
                # get_civitai_model_info_by_id_btn = gr.Button(value="Get Model Info from Civitai", variant="primary")
                # get_model_by_id_log_md = gr.Markdown("")

        with gr.Box(elem_classes="ch_box"):
            with gr.Column():
                gr.Markdown("### Download Model")
                # with gr.Row():
                #     dl_model_url_or_id_txtbox = gr.Textbox(label="Civitai URL", lines=1, value="")
                #     dl_model_info_btn = gr.Button(value="1. Get Model Info by Civitai Url", variant="primary")

                gr.Markdown(value="2. Pick Subfolder and Model Version")
                # with gr.Row():
                #     dl_model_name_txtbox = gr.Textbox(label="Model Name", interactive=False, lines=1, value="")
                #     dl_model_type_txtbox = gr.Textbox(label="Model Type", interactive=False, lines=1, value="")
                #     dl_subfolder_drop = gr.Dropdown(choices=[], label="Sub-folder", value="", interactive=True, multiselect=False)
                #     dl_version_drop = gr.Dropdown(choices=[], label="Model Version", value="", interactive=True, multiselect=False)
                #     dl_all_ckb = gr.Checkbox(label="Download All files", value=False, elem_id="ch_dl_all_ckb", elem_classes="ch_vpadding")
                
                # dl_civitai_model_by_id_btn = gr.Button(value="3. Download Model", variant="primary")
                # dl_log_md = gr.Markdown(value="Check Console log for Downloading Status")

        with gr.Box(elem_classes="ch_box"):
            with gr.Column():
                gr.Markdown("### Check models' new version")
                #with gr.Row():
                #    model_types_ckbg = gr.CheckboxGroup(choices=model_types, label="Model Types", value=["lora"])
                #    check_models_new_version_btn = gr.Button(value="Check New Version from Civitai", variant="primary")

                # check_models_new_version_log_md = gr.HTML("It takes time, just wait. Check console log for detail")

        with gr.Box(elem_classes="ch_box"):
            with gr.Column():
                gr.Markdown("### Other")
                # save_setting_btn = gr.Button(value="Save Setting")
                gr.Markdown(value="Settings are moved into Settings Tab->Civitai Helper section")


        # # ====Footer====
        # gr.Markdown(f"<center>version:{util.version}</center>")

        # # ====hidden component for js, not in any tab====
        # js_msg_txtbox = gr.Textbox(label="Request Msg From Js", visible=False, lines=1, value="", elem_id="ch_js_msg_txtbox")
        # py_msg_txtbox = gr.Textbox(label="Response Msg From Python", visible=False, lines=1, value="", elem_id="ch_py_msg_txtbox")

        # js_open_url_btn = gr.Button(value="Open Model Url", visible=False, elem_id="ch_js_open_url_btn")
        # js_add_trigger_words_btn = gr.Button(value="Add Trigger Words", visible=False, elem_id="ch_js_add_trigger_words_btn")
        # js_use_preview_prompt_btn = gr.Button(value="Use Prompt from Preview Image", visible=False, elem_id="ch_js_use_preview_prompt_btn")
        # js_dl_model_new_version_btn = gr.Button(value="Download Model's new version", visible=False, elem_id="ch_js_dl_model_new_version_btn")
        # js_remove_card_btn = gr.Button(value="Remove Card", visible=False, elem_id="ch_js_remove_card_btn")

        # # ====events====
        # # Scan Models for Civitai
        # scan_model_civitai_btn.click(scan_model, inputs=[scan_model_types_ckbg], outputs=scan_model_log_md)

        # # Get Civitai Model Info by Model Page URL
        # model_type_drop.change(get_model_names_by_input, inputs=[model_type_drop, empty_info_only_ckb], outputs=model_name_drop)
        # empty_info_only_ckb.change(get_model_names_by_input, inputs=[model_type_drop, empty_info_only_ckb], outputs=model_name_drop)

        # get_civitai_model_info_by_id_btn.click(get_model_info_by_input, inputs=[model_type_drop, model_name_drop, model_url_or_id_txtbox], outputs=get_model_by_id_log_md)

        # # Download Model
        # dl_model_info_btn.click(get_model_info_by_url, inputs=dl_model_url_or_id_txtbox, outputs=[dl_model_info, dl_model_name_txtbox, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop])
        # dl_civitai_model_by_id_btn.click(dl_model_by_input, inputs=[dl_model_info, dl_model_type_txtbox, dl_subfolder_drop, dl_version_drop, dl_all_ckb], outputs=dl_log_md)

        # # Check models' new version
        # check_models_new_version_btn.click(model_action_civitai.check_models_new_version_to_md, inputs=model_types_ckbg, outputs=check_models_new_version_log_md)

        # # js action
        # js_open_url_btn.click(open_model_url, inputs=[js_msg_txtbox], outputs=py_msg_txtbox)
        # js_add_trigger_words_btn.click(js_action_civitai.add_trigger_words, inputs=[js_msg_txtbox], outputs=[txt2img_prompt, img2img_prompt])
        # js_use_preview_prompt_btn.click(js_action_civitai.use_preview_image_prompt, inputs=[js_msg_txtbox], outputs=[txt2img_prompt, txt2img_neg_prompt, img2img_prompt, img2img_neg_prompt])
        # js_dl_model_new_version_btn.click(dl_model_new_version, inputs=[js_msg_txtbox], outputs=dl_log_md)
        # js_remove_card_btn.click(js_action_civitai.remove_model_by_path, inputs=[js_msg_txtbox], outputs=py_msg_txtbox)

    # the third parameter is the element id on html, with a "tab_" as prefix
    return (civitai_helper , "Civitai Helper", "civitai_helper"),





# script_callbacks.on_ui_settings(on_ui_settings)
# script_callbacks.on_ui_tabs(on_ui_tabs)



def get_model_info_by_url2(url):
    r = get_model_info_by_url(url)

    model_info = {}
    model_name = ""
    model_type = ""
    subfolders = []
    version_strs = []
    if r:
        model_info, model_name, model_type, subfolders, version_strs = r

    if len(version_strs) > 0:
        #rr = dl_model_by_input(model_info, model_type, 'ani\\newCharacter', version_strs[0], None, None, None)
        #rr = dl_model_by_input(model_info, model_type, 'ani\\newCostume', version_strs[0], None, None, None)
        #rr = dl_model_by_input(model_info, model_type, 'ani\\newConcept', version_strs[0], None, None, None)
        #rr = dl_model_by_input(model_info, model_type, 'ani\\newStyle', version_strs[0], None, None, None)
        rr = dl_model_by_input(model_info, model_type, 'ani\\newSex', version_strs[0], None, None, None)
        
        #rr = dl_model_by_input(model_info, model_type, 'real\\newCharacter', version_strs[0], None, None, None)
        #rr = dl_model_by_input(model_info, model_type, 'real\\newCostume', version_strs[0], None, None, None)
        #rr = dl_model_by_input(model_info, model_type, 'real\\newConcept', version_strs[0], None, None, None)
        #rr = dl_model_by_input(model_info, model_type, 'real\\newStyle', version_strs[0], None, None, None)
        #rr = dl_model_by_input(model_info, model_type, 'real\\newSex', version_strs[0], None, None, None)

        #rr = dl_model_by_input(model_info, model_type, 'new', version_strs[0], None, None, None)

        return [model_info, model_name, model_type]

import time
if __name__ == '__main__':
    str_list = [
        ]

    for x in range(len(str_list)):
        get_model_info_by_url2(str_list[x])
        time.sleep(5)

