#!/usr/bin/env python3
import sys

input_file_name = None
output_file_name = "out.yaml"

i = 1
while i < len(sys.argv):
    if sys.argv[i][0] == "-":
        # flag
        if sys.argv[i] in [ "-o", "--output" ]:
            i += 1
            if i >= len(sys.argv):
                print("Output file is not specified")
                quit(1)

            output_file_name = sys.argv[i]
        else:
            print("Unexpected flag \"{}\"".format(sys.argv[i]))
    else:
        input_file_name = sys.argv[i]

    i += 1

if input_file_name == None:
    print("Input file is not specified")
    quit(1)

def read_lines(file):
    for i in file:
        yield i[0:-1]

class Token:
    def __init__(self, token_type, value, row, column):
        self.value = value
        self.type = token_type
        self.row = row
        self.column = column

    def __str__(self):
        return "{}: {}  ({}:{})".format(self.type, self.value, str(self.row), str(self.column))

tokens = []
with open(input_file_name, "r") as input_file:
    line_num = 1

    for line in read_lines(input_file):
        i = 0
        while i < len(line):
            char = line[i]
            if char in "\t\n\v\r ":
                i += 1
            elif char == '"':
                # string
                value = ""
                start = i
                i += 1

                while i < len(line) and not (line[i] == '"' and line[i-1] != "\\"):
                    value += line[i]
                    i += 1

                if i > len(line):
                    print("Unexpected end of line. Expected end of string at position ({}:{})", str(line_num), str(i + 1))
                    quit(1)

                tokens.append(Token("string", '"{}"'.format(value), line_num, start + 1))
                i += 1
            elif char in "1234567890":
                start = i
                value = ""
                
                while i < len(line) and line[i] in "1234567890":
                    value += line[i]
                    i += 1

                tokens.append(Token("number", value, line_num, start + 1))
            elif char == "{":
                tokens.append(Token("obj_start", char, line_num, i + 1))
                i += 1
            elif char == "[":
                tokens.append(Token("arr_start", char, line_num, i + 1))
                i += 1
            elif char == "}":
                tokens.append(Token("obj_end", char, line_num, i + 1))
                i += 1
            elif char == "]":
                tokens.append(Token("arr_end", char, line_num, i + 1))
                i += 1
            elif char == ".":
                tokens.append(Token("dot", char, line_num, i + 1))
                i += 1
            elif char == ",":
                tokens.append(Token("comma", char, line_num, i + 1))
                i += 1
            elif char == ":":
                tokens.append(Token("colon", char, line_num, i + 1))
                i += 1
            elif char == "t" or char == "f" or char == "n":
                # true or false or null
                value = ""
                start = i
                while i < len(line) and not line[i] in ":,.[{}]":
                    value += line[i]
                    i += 1

                if not value in [ "true", "false", "null" ]:
                    print('Unexpected "{}" at position ({}:{})'.format(value, str(line_num), str(start + 1)))
                    print(line)
                    print(" " * start + "^")
                    quit(1)

                tokens.append(Token("bool" if value != "null" else "null", value, line_num, start + 1))
            else:
                print('Unexpected character "{}" at position ({}:{})'.format(char, str(line_num), str(i + 1)))
                print(line)
                print(" " * i + "^")
                quit(1)
        line_num += 1

#print("Tokens:")
#print(*tokens, sep="\n")
#print()

# parsing
tokens_index = 0
nodes = []

class Node:
    def __init__(self, node_type, token, body):
        self.type = node_type
        self.row = token.row
        self.column = token.column
        self.value = token.value
        self.body = body

    def __str__(self):
        result = "{}: {} ({}:{})".format(self.type, self.value, str(self.row), str(self.column))
        result += "\n"
        for child in self.body:
            result += str(child) + "\n"

        return result.replace("\n", "\n\t")

def parse_item():
    global tokens, tokens_index
    token = tokens[tokens_index]
    node = None

    if token.type == "obj_start":
        node = Node("object", token, [])
        tokens_index += 1
        while tokens_index < len(tokens) and tokens[tokens_index].type != "obj_end":
            if tokens[tokens_index].type == "string":
                key = tokens[tokens_index]
                tokens_index += 1

                if tokens_index >= len(tokens) or tokens[tokens_index].type != "colon":
                    if tokens_index >= len(tokens):
                        tokens_index = -1
                    print("Expected colon at position ({}:{})".format(str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
                    quit(1)

                tokens_index += 1

                if tokens_index >= len(tokens):
                    if tokens_index >= len(tokens):
                        tokens_index = -1

                    print("Expected value at position ({}:{})".format(str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
                    quit(1)

                value = None
                if tokens[tokens_index].type in [ "obj_start", "arr_start" ]:
                    value = parse_item()
                else:
                    value = Node(tokens[tokens_index].type, tokens[tokens_index], [])
                    if tokens[tokens_index].type == "number" and tokens_index + 2 < len(tokens) and tokens[tokens_index + 1].type == "dot" and tokens[tokens_index + 2].type == "number":
                        tokens_index += 2
                        value.value += "." + tokens[tokens_index].value

                    tokens_index += 1

                if tokens_index >= len(tokens) or (tokens[tokens_index].type != "comma" and tokens[tokens_index].type != "obj_end"):
                    if tokens_index >= len(tokens):
                        tokens_index = -1

                    print("Expected comma at position ({}:{})".format(str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
                    quit(1)
                
                if tokens[tokens_index].type == "comma":
                    tokens_index += 1

                node.body.append(Node("key", key, [ value ]))
            else: 
                print('Unexpected "{}" at position ({}:{})'.format(tokens[tokens_index].value, str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
                quit(1)

        if tokens_index >= len(tokens) or tokens[tokens_index].type != "obj_end":
            if tokens_index >= len(tokens):
                tokens_index = -1

            print("Expected \"{}\" at position ({}:{})".format("}", str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
            quit(1)

        tokens_index += 1
    elif token.type == "arr_start":
        node = Node("array", token, [])
        tokens_index += 1

        while tokens_index < len(tokens) and tokens[tokens_index].type != "arr_end":
            if tokens[tokens_index].type in [ "string", "bool", "number", "null", "obj_start", "arr_start" ]:
                value = None

                if tokens_index >= len(tokens):
                    print("Unexpected end of file")
                    quit(1)

                if tokens[tokens_index].type in [ "obj_start", "arr_start" ]:
                    value = parse_item()
                else:
                    value = Node(tokens[tokens_index].type, tokens[tokens_index], [])
                    if tokens[tokens_index].type == "number" and tokens_index + 2 < len(tokens) and tokens[tokens_index + 1].type == "dot" and tokens[tokens_index + 2].type == "number":
                        tokens_index += 2
                        value.value += "." + tokens[tokens_index].value

                    tokens_index += 1

                if tokens_index >= len(tokens) or (tokens[tokens_index].type != "comma" and tokens[tokens_index].type != "arr_end"):
                    if tokens_index >= len(tokens):
                        tokens_index = -1

                    print("Expected comma at position ({}:{})".format(str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
                    quit(1)
                
                if tokens[tokens_index].type == "comma":
                    tokens_index += 1

                node.body.append(value)
            else: 
                print('Unexpected "{}" at position ({}:{})'.format(tokens[tokens_index].value, str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
                quit(1)

        if tokens_index >= len(tokens) or tokens[tokens_index].type != "arr_end":
            if tokens_index >= len(tokens):
                tokens_index = -1

            print("Expected \"{}\" at position ({}:{})".format("]", str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
            quit(1)

        tokens_index += 1
    else:
        print('Unexpected {} at position ({}:{})'.format(tokens[tokens_index].value, str(tokens[tokens_index].row), str(tokens[tokens_index].column)))
        quit(1)

    return node


while tokens_index < len(tokens):
    nodes.append(parse_item())

#print()
#print()
#print(*nodes, sep = "\n")

with open(output_file_name, "w") as output_file:
    def compile_node(node):
        if node.type == "object":
            for key in node.body:
                res = key.value[1:-1] + ": "
                if key.body[0].type in [ "array", "object" ]:
                    res += "\n"

                for i in compile_node(key.body[0]):
                    res += i

                res = res.replace("\n", "\n  ")
                yield res
        elif node.type == "array":
            for child in node.body:
                res = "- "

                if child.type in [ "array", "object" ]:
                    res += "\n"

                for i in compile_node(child):
                    if child.type in [ "array", "object" ]:
                        res += "  "
                    res += i

                yield res
        elif node.type == "null":
            yield ""
        else:
            if node.type == "string" and not '"' in node.value:
                yield node.value[1:-1] + "\n"
            else:
                yield node.value + "\n"

    for node in nodes:
        for line in compile_node(node):
            output_file.write(line.rstrip())
            output_file.write("\n")
    
