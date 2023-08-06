import sys
from pathlib import Path
import os
import shutil
import concurrent.futures
print('Entry:', sys.argv)

if len(sys.argv) != 2:
    print("Argument != 2")
    quit()

path_1 = Path(sys.argv[1])


musics = []
videos = []
photos = []
documents = []
archives = []
others = []
know_ext = []
unknown_ext = []
directory_images = f"{path_1}/images"
directory_video = f"{path_1}/video"
directory_music = f"{path_1}/music"
directory_documents = f"{path_1}/documents"
directory_archives = f"{path_1}/archives"


def normalize(name):
    last_dot_index = name.rfind('.')
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    res = ''

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    for i in name.translate(TRANS)[:last_dot_index]:
        if i.isalpha() or i.isdigit():
            res += i
        else:
            res += '_'

    return res + name[last_dot_index:]


def sorted_folder(file):
    name = file.name
    trans_name = normalize(name)
    x = f"{path_1}\\{trans_name}"
    x_path = Path(x)
    y = os.rename(file, x)
    if file.is_dir():
        if x_path.name == "images" or x_path.name == "video" or x_path.name == "documents" or x_path.name == "music" or x_path.name == "archives":
            pass
        if not os.listdir(x):
            os.rmdir(x)
        else:
            sorted_folder(x_path)
    else:
        if x.endswith(".mp3") or x.endswith('.ogg') or x.endswith('.wav') or x.endswith('.amr'):
            musics.append(trans_name)
            if not os.path.exists(directory_music):
                os.makedirs(directory_music)
            shutil.move(x, directory_music)
            if x_path.suffix in know_ext:
                pass
            else:
                know_ext.append(x_path.suffix)
        elif x.endswith(".avi") or x.endswith('.mp4') or x.lower().endswith('.mov') or x.endswith('.mkv'):
            videos.append(trans_name)
            if not os.path.exists(directory_video):
                os.makedirs(directory_video)
            shutil.move(x, directory_video)
            if x_path.suffix in know_ext:
                pass
            else:
                know_ext.append(x_path.suffix)
        elif x.endswith('.jpeg') or x.endswith('.png') or x.endswith('.jpg') or x.endswith('.svg'):
            photos.append(trans_name)
            if not os.path.exists(directory_images):
                os.makedirs(directory_images)
            shutil.move(x, directory_images)
            if x_path.suffix in know_ext:
                pass
            else:
                know_ext.append(x_path.suffix)
        elif x.endswith('.doc') or x.endswith('.docx') or x.endswith('.txt') or x.endswith('.pdf') or x.endswith('xlsx') or x.endswith('.pptx') or x.endswith('.ppt'):
            documents.append(trans_name)
            if not os.path.exists(directory_documents):
                os.makedirs(directory_documents)
            shutil.move(x, directory_documents)
            if x_path.suffix in know_ext:
                pass
            else:
                know_ext.append(x_path.suffix)
        elif x.endswith('.zip') or x.endswith('.gz') or x.endswith('.tar'):
            archives.append(trans_name)
            if not os.path.exists(directory_archives):
                os.makedirs(directory_archives)
            unpack_folder = os.path.splitext(trans_name)[0]
            b = f"{directory_archives}/{unpack_folder}"
            unpack = shutil.unpack_archive(x, b)
            os.remove(x)
            if x_path.suffix in know_ext:
                pass
            else:
                know_ext.append(x_path.suffix)
        else:
            others.append(trans_name)
            if x_path.suffix in unknown_ext:
                pass
            else:
                unknown_ext.append(x_path.suffix)


def flow_sort(path_1):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in path_1.iterdir():
            executor.submit(sorted_folder, i)


if path_1.is_dir():
    flow_sort(path_1)
    print('Done!')
else:
    print("This is not a folder")
