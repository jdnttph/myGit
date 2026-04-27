import sys
from representation import correct_input
from mygit import init,commit,checkout

def main():
    args=sys.argv
    result=correct_input(args)
    if result==False:
        print("ERROR")
        return

    if args[1]=="init":
        init()

    if args[1]=="commit":
        commit(args[2])

    if args[1]=="checkout":
        checkout(int(args[2]))

if __name__ == "__main__":
    main()