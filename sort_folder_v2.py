import sys
from pathlib import Path
import shutil
import os
import concurrent.futures

if len(sys.argv) != 2:
    print('Будь ласка введіть тільки 2 аргументи!')
    quit()

# шлях до файлу який вказали у консолі
folder = Path(sys.argv[1])

# словник за яким буде йти сортування файлів на категорії
name_folders = {
    ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'): 'documents',
    ('png', 'jpg', 'jpeg', 'svg'): 'images',
    ('mp3', 'wav', 'amr', 'ogg'): 'audio',
    ('mp4', 'avi', 'mov', 'mkv'): 'video',
    ('zip', 'gz', 'tar'): 'archive'
}


# функція для створення папок, у якіц будуть поміщені усі файли


def create_folders(parent_folder_path):
    folder_names = ['images', 'video',
                    'documents', 'audio', 'archive']

    for folder_name in folder_names:
        folder_path = os.path.join(parent_folder_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)


# функція, яка буде пейменовувати файл з кирилиці на латиницю і всі символи крім букв і цифр заміняти на '_'


def normalize(name):
    last_dot_index = name.rfind('.')
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
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


# основна функція, яка здійснює сортування файлів по папках


def sort_files(folder):
    folders = []
    files = []
    # проходимось по вказаній папці рекурсивною функцією і зберігаємо шляхи до файлів та папок у відповідні списки
    if os.path.exists(folder):
        for dirpath, dirnames, filenames in os.walk(folder):
            for file in filenames:
                files.append(os.path.join(dirpath, file))

            for folderr in dirnames:
                folders.append(os.path.join(dirpath, folder))

    # за допомогою циклу переносимо файливи у кореневу папку
    # використовуючи функцію normalize перейменовуємо файли
    for fl in files:
        new_name = normalize(os.path.basename(fl))
        path_drctr = os.path.join(folder, new_name)
        os.rename(fl, path_drctr)

    # знову проходимось по кореневій папці і перевіряємо усі папки і підпапки, якщо вони пусті то видаляємо їх
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            if not os.listdir(full_path):
                os.rmdir(full_path)

    # за допомогою цієї функції створюємо папки в які будемо сортувати файли
    create_folders(folder)

    # проходимось циклом по списку файлів
    for i in files:
        for key, value in name_folders.items():  # через словник беремо назви папок і розширення файлів
            if i.lower().endswith(key):
                filee = normalize(os.path.basename(i))
                if value == 'archive':  # якщо це архів, то розпаковуємо його у ще одну папку, яка має назву архіва, але без розширення
                    last_dot_index = filee.rfind('.')
                    folder_path = os.path.join(
                        f'{folder}\\archive', filee[:last_dot_index])
                    shutil.unpack_archive(f'{folder}\{filee}', folder_path)
                    os.remove(f'{folder}\{filee}')
                else:  # переміщаємо файл із кореневої папки у вказану за значенням словника
                    shutil.move(f'{folder}\{filee}',
                                f'{folder}\{value}\{filee}')


def flow(folder):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in folder.iterdir():
            executor.submit(sort_files, i)


if __name__ == '__main__':
    if folder.is_dir():
        flow(folder)
    else:
        print("This is not a folder")
