def isExist(path_to_folder):
    import os
    #путь до папки
    file_path=path_to_folder+"\\.mygitignore"

    return os.path.exists(file_path)


def get_ignored_files(path_to_gitignore)->list[str]:
    ignored_files=[]

    with open(path_to_gitignore, "r") as file:
        for line in file:
           ignored_files.append(line.strip())
    return ignored_files

def init()->bool:
    import os

    if os.path.exists(".myGit"):
        return False

    os.mkdir(".myGit")

    #в sequence лежит id commit
    with open(".myGit\\.sequence", "w") as file:
        file.write("1")

    return True