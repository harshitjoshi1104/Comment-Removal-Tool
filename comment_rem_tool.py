############################
# Small tool to remove all the comments from c/c++ files

IS_LINE_COMMENT = False
IS_BLOCK_COMMENT = False
IS_COMMENT_ENABLED = False
stack = []


def transform_line(line):
    global IS_BLOCK_COMMENT
    global IS_LINE_COMMENT
    global IS_COMMENT_ENABLED
    global stack

    IS_LINE_COMMENT = False
    IS_COMMENT_ENABLED = IS_LINE_COMMENT | IS_BLOCK_COMMENT

    line = list(line)
    new_line = []

    i = 0
    while i < len(line):
        if IS_COMMENT_ENABLED and IS_LINE_COMMENT:
            i+=1
            continue

        if IS_COMMENT_ENABLED and IS_BLOCK_COMMENT:
            if i!=0 and line[i-1] + line[i] == "*/":
                IS_BLOCK_COMMENT = False
                IS_COMMENT_ENABLED = IS_LINE_COMMENT | IS_BLOCK_COMMENT
            i+=1
            continue


        if not IS_COMMENT_ENABLED:
            if i < len(line) - 1:
                if line[i] + line[i+1] == "/*":
                    if len(stack) == 0:
                        IS_BLOCK_COMMENT = True
                        IS_COMMENT_ENABLED = True
                        i+=2
                        continue

                elif line[i] + line[i+1] == "//":
                    if len(stack) == 0:
                        IS_LINE_COMMENT = True
                        IS_COMMENT_ENABLED = True
                        i+=2
                        continue

            if line[i] == "\"":
                if len(stack) and stack[-1] == "\"":
                    stack.pop()
                else:
                    stack.append("\"")

            elif line[i] == "\'":
                if len(stack) and stack[-1] == "\'":
                    stack.pop()
                else:
                    stack.append("\'")


            new_line.append(line[i])
            i+=1

    return "".join(new_line)


def read_file():
    file = open("dummy_code.c", 'r')
    content_of_file = file.read()
    file.close
    print("Read success!")
    return content_of_file


def write_to_file(content):
    file = open("dummy_code.c", "w")
    file.write(content)
    file.close()
    print("Written Successfully")



def main():
    content = read_file()
    content = content.split("\n")

    for i in range(len(content)):
        line = content[i]

        new_line = transform_line(line)

        content[i] = new_line

    content = "\n".join(content)

    write_to_file(content=content)


main()