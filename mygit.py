import os
import shutil

#Проверяет существование
def isExist(path_to_folder):
    #путь до папки
    file_path=os.path.join(path_to_folder,".mygitignore")

    return os.path.exists(file_path)

#Список конкретных названий файлов, которые нужно игнорировать.
def get_ignored_files(path_to_gitignore)->list[str]:
    ignored_files=[]

    if not os.path.exists(path_to_gitignore):
        return ignored_files

    with open(path_to_gitignore, "r") as file:
        for line in file:
           ignored_files.append(line.strip())
    return ignored_files


#Создаёт служебную папку `.mygit`, в которой будет храниться история
def init()->bool:

    if os.path.exists(".mygit"):
        return False

    os.mkdir(".mygit")

    #в sequence лежит id commit
    with open(os.path.join(".mygit",".sequence"), "w") as file:
        file.write("1")

    os.mkdir(os.path.join(".mygit", "commits"))
    os.mkdir(os.path.join(".mygit", ".message"))

    return True


#Сохраняет текущее состояние файлов проекта.При коммите:обходить текущую директорию.
# Игнорировать:папку `.mygit`, файлы и папки из `.mygitignore`
def commit(message:str)->bool:

    if not os.path.exists(".mygit"):
        return False

    ignored_files=get_ignored_files(".mygitignore")

    all_files=[]

    for root,dirs,files in os.walk("."):
        if ".mygit" in dirs:
            dirs.remove(".mygit")

        folder=os.path.relpath(root,".")

        one_of_ignored=False
        for ignored in ignored_files:
            if folder.startswith(ignored):
                one_of_ignored=True
                break

        if one_of_ignored:
            continue

        for file in files:
            file_path=os.path.join(root, file)
            if file not in ignored_files and file_path != ".mygitignore":
                all_files.append(file_path)

    with open(os.path.join(".mygit",".sequence"), "r") as file:
            commit_id=int(file.read())

    commit_folder=os.path.join(".mygit","commits",str(commit_id))


    if os.path.exists(commit_folder):
            raise Exception(f"Commit {commit_id} already exists")
    else:
        os.makedirs(commit_folder)

    with open(os.path.join(".mygit",".message",str(commit_id)),"w") as file:
        file.write(message)

    for file_path in all_files:
        rel_path=os.path.relpath(file_path, ".")

        dest_path=os.path.join(commit_folder, rel_path)

        dest_dir=os.path.dirname(dest_path)

        if dest_dir:
            os.makedirs(dest_dir,exist_ok=True)

        shutil.copy(file_path, dest_path)

    with open(os.path.join(".mygit",".sequence"), "w") as file:
            file.write(str(commit_id+1))

    return True

#Принудительно заменяет файлы из директории на их версию под номером <id>
def checkout(commit_id)->bool:

    if not os.path.exists(".mygit"):
        return False

    with open(os.path.join(".mygit",".sequence"), "r") as file:
        current_id=int(file.read())

    if commit_id >= current_id or commit_id < 1:
        return False


    commit_path=os.path.join(".mygit","commits",str(commit_id))

    if not os.path.exists(commit_path):
        return False

    shutil.copytree(commit_path, ".", dirs_exist_ok=True)

    return True