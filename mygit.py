#Проверяет существование
def isExist(path_to_folder):
    import os
    #путь до папки
    file_path=path_to_folder+"\\.mygitignore"

    return os.path.exists(file_path)

#Список конкретных названий файлов, которые нужно игнорировать.
def get_ignored_files(path_to_gitignore)->list[str]:
    ignored_files=[]

    with open(path_to_gitignore, "r") as file:
        for line in file:
           ignored_files.append(line.strip())
    return ignored_files


#Создаёт служебную папку `.mygit`, в которой будет храниться история
def init()->bool:
    import os

    if os.path.exists(".mygit"):
        return False

    os.mkdir(".mygit")

    #в sequence лежит id commit
    with open(".mygit\\.sequence", "w") as file:
        file.write("1")

    return True


#Сохраняет текущее состояние файлов проекта.При коммите:обходить текущую директорию.
# Игнорировать:папку `.mygit`, файлы и папки из `.mygitignore`
def commit(message:str)->bool:
    import os
    import shutil

    if not os.path.exists(".mygit"):
        return False

    ignored_files=get_ignored_files(".mygitignore")

    all_files=[]

    for root,dirs,files in os.walk("."):
        if ".mygit" in root:
            continue

        for file in files:
            file_path=os.path.join(root, file)

        is_ignored=False

        for ignored in ignored_files:
            if ignored in file_path:
                is_ignored=True
                break

        if not is_ignored:
            all_files.append(file_path)

        with open(".mygit\\.sequence", "r") as file:
            commit_id=int(file.read())

        commit_folder=".mygit\\commits\\"+str(commit_id)

        if not os.path.exists(commit_folder):
            os.mkdir(commit_folder)

        for file_path in all_files:
            shutil.copy(file_path, commit_folder)

        with open(".mygit\\.sequenсe", "w")as file:
            file.write(str(commit_id+1))

        return True

#Принудительно заменяет файлы из директории на их версию под номером <id>
def chekout(commit_id)->bool:
