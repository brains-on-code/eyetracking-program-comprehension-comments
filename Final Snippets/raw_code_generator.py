import os
from os.path import isfile

import pandas as pd


def main():
    # read all java files in directory and strip unnecessary code such as imports, and class names
    # just leave the function and the main method
    only_files = [f for f in os.listdir() if f.endswith('.java') and isfile(f)]

    # create directory
    if not os.path.exists('Raw Code'):
        os.makedirs('Raw Code')

    for file_name in only_files:
        # read file
        with open(file_name, 'r') as file:
            data = file.readlines()
        # remove imports
        data = [line for line in data if not line.startswith('import')]
        # remove class name
        data = [line for line in data if not line.startswith('public class')]
        # remove last bracket
        data = data[:-1]
        # remove one tab from each line
        data = [line[4:] for line in data]

        # add empty line before main method
        for i in range(len(data)):
            if 'public static void main' in data[i]:
                data.insert(i, '\n')
                break

        # write file
        with open('Raw Code/'+file_name, 'w') as file:
            file.writelines(data)


if __name__ == '__main__':
    main()
