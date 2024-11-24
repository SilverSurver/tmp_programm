import os
import shutil
import subprocess


def split_in_ors(command):
    return [i.strip() for i in command.strip().split('|')]

def split_in_ands(ors):
    return [[i.strip() for i in k.strip().split(' ')] for k in ors]


def contains_and(or_block, two):
    # or block: [and_one, and_two, and_three]
    for i in or_block:
        if not two.__contains__(i):
            return False
    return True

def add_or(tags,one,two,full_tags):
    put = False
    for i in one:
        if tags.__contains__(i) or full_tags.__contains__(i):
            put = True
            break

    if put:
        for i in two:
            if not (full_tags.__contains__(i) or tags.__contains__(i)):
                full_tags.append(i)


def add_and(tags,one,two,full_tags):
    put = False
    for i in one:
        if full_tags.__contains__(i):
            put = True
        else:
            put = False
            break

    if put:
        for i in two:
            if not full_tags.__contains__(i):
                full_tags.append(i)


def add(tags,full_tags):
    # tuhe bei or immer den vollen Namen überall rein, also auch bei weitereen:
    # add_or(tags, ['d'], ['doggo','immer_knuffig'], full_tags)
    add_or(tags, ['d'], ['doggo','knuffig'], full_tags)
    add_or(tags, ['kn','knuffig'], ['knuffig'], full_tags)
    add_or(tags, ['k'], ['kitty'], full_tags)
    add_or(tags, ['doggo', 'kitty'], ['cute'], full_tags)


    # bei dem hier müssen alle volle Namen enthalten
    add_and(tags, ['doggo', 'cute','knuffig'], ['sugar'], full_tags)

    ret = ''
    for i in full_tags:
            ret+=(i +' ')
    return ret


if __name__ == '__main__':
    directory = "../../../cute/"
    source = "../../../filter/"
    obj = []
    with open('file_name.txt','r') as file:
        for line in file:
            tmp = line.split(' ')
            one = tmp[0].strip()
            two = [i.strip() for i in tmp[1:]]
            obj.append((one,two))
        file.close()


    print(obj)

    cmd = input("command: ")


    while cmd != 'q':
        if cmd == 'f':
            filter = input('filter: ')
            ors = split_in_ors(filter)
            ands = split_in_ands(ors)

            for one,two in obj:
                for or_block in ands:
                    if contains_and(or_block,two):
                        # move
                        tmp = os.path.join(directory,one)
                        shutil.move(tmp,source)
                        break

            cmd = input("command: ")

            command  = "mv " + source +'* ' + directory
            subprocess.run(command, shell=True, check=True)

        elif cmd == 'a':
            # Specify the directory
            tag = input('tag: ')
            tags = tag.split(' ')
            to_add = []
            to_remove = []
            full_tags = []
            tags_ = add(tags,full_tags)
            # Iterate through all files in the directory
            for filename in os.listdir(directory):
                print(filename)
                if filename[-5] == ')':
                    to_remove.append(filename)
                elif not any(item[0] == filename for item in obj):
                    to_add.append(filename)


            with open('file_name.txt','a') as writer:
                for i in to_add:
                    wr = i+ ' ' + tags_ + '\n'
                    writer.write(wr)
                writer.close()


            for i in to_remove:
                os.remove(os.path.join(directory, i))

            cmd = input("command: ")