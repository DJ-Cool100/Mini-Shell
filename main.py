import os
import re

# MINI SHELL PROGRAM


global isRunning
isRunning = True

RED    = "\033[31m"
GREEN  = "\033[32m"
BLUE   = "\033[34m"
RESET  = "\033[0m"


KEYWORDS = {"if", "else", "while", "return", "def"}
COLORS = {
    "keyword": "\033[34m",  # blue
    "number": "\033[35m",  # magenta
    "string": "\033[32m",  # green
    "comment": "\033[90m",  # gray
}

TOKEN_REGEX = [
    ("comment", r"#.*"),
    ("string", r"\".*?\""),
    ("number", r"\b\d+\b"),
    ("keyword", r"\b(if|else|while|return|func)\b"),
]


def highlight_line(line):
    for token_type, pattern in TOKEN_REGEX:
        color = COLORS[token_type]

        line = re.sub(
            pattern,
            lambda m: f"{color}{m.group(0)}{RESET}",
            line
        )
    return line


def text_edit(filename):
    buffer = []
    if not filename:
        print("No arguments provided")
    else:
        try:
            with open(filename, "r") as f:
                buffer = f.read().splitlines()
        except FileNotFoundError:
            buffer = []

        print("entering text editor. Type '.' alone and click enter to exit and save.")

        while True:
            line = input("> ")

            if line == ".":
                break

            cmd = get_command(line)

            if cmd == "ch":
                args = get_args(line)

                if len(args) < 2:
                    print("Usage: ch <line_number> <new_text>")
                    continue

                try:
                    index = int(args[0]) - 1

                    if index < 0 or index >= len(buffer):
                        print("Line number out of range")
                        continue

                    buffer[index] = " ".join(args[1:])

                except ValueError:
                    print("Line number must be an integer")

                continue  # prevents appending

            # normal text
            buffer.append(line)

        try:
            with open(filename, "w") as f:
                for line in buffer:
                    f.write(line + "\n")
            print(f"File '{filename}' saved successfully.")
        except PermissionError:
            print("Permission denied: cannot save file.")


def prompt():
    return input(">>>")


def get_command(user_in):
    return user_in.lower().split(" ")[0]


def get_args(user_in):
    return user_in.split(" ")[1:]


def open_file(filename):
    try:
        with open(filename, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("File does not exist")
    except PermissionError:
        print("Permission denied")
    except IsADirectoryError:
        print("That's a directory")


def exec_command(user_in):
    global isRunning
    command = get_command(user_in)

    match command:
        case "help":
            print("exit, ls, pwd, echo <args>, edit <file>, touch <file>, cd <absolute path>, cat <file>")
        case "exit":
            isRunning = False
        case "ls":
            for f in os.listdir('.'):
                print(f)
        case "pwd":
            print(os.getcwd())
        case "echo":
            message = " ".join(get_args(user_in))
            print(message)
        case "cd":
            args = get_args(user_in)
            if not args:
                print("No arguments provided")
            else:
                try:
                    os.chdir(args[0])
                except FileNotFoundError:
                    print("Directory does not exist")
                except NotADirectoryError:
                    print("Directory is not a directory")
                except PermissionError:
                    print("Permission denied")
        case "cat":

            args = get_args(user_in)
            if not args:
                print("No arguments provided")
            else:
                try:
                    with open(args[0], "r") as file:
                        for line in file:
                            print(highlight_line(line), end="")
                except FileNotFoundError:
                    print("File does not exist")
                except PermissionError:
                    print("Permission denied")
        case "edit":
            args = get_args(user_in)
            text_edit(args[0])
        case _:
            print("Unknown command")


while isRunning != False:
    command = prompt()
    exec_command(command)
