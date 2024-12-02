import os
import readline
import shutil
import subprocess

from pwnlib.term.readline import history


def tag_arr_to_str(tags):
    ret = ''
    for tag in tags:
        ret+=(str(tag)+' ')
    return ret.strip()

def handle_put(dest_bwz_source,tx,dict_or,dict_and):
    move_counter = 0
    source = 'download_folder/'
    images = []
    to_delte = []
    with open(tx,'r') as file:
        for line in file:
            image,_ = str_to_tag_arr(line)
            images.append(image.strip())
        file.close()

    with open(tx,'a') as file:
        for filename in os.listdir(source):
            if images.__contains__(filename) or filename[-6] == ')':
                to_delte.append(filename)
                continue

            move_counter+=1
            full_path = os.path.join(source, filename)
            process = subprocess.Popen(f'gio open {full_path}', shell=True)
            tags = input("tags : ")
            readline.write_history_file(".HISTORY")
            history.append(tags)
            if tags == 'show':
                for k in dict_or.keys():
                    print(str(k) + " ", end='')
                print()
                tags = input("tags: ")
                readline.write_history_file(".HISTORY")
                history.append(tags)
            tag_arr = tags.split(' ')
            wr = tag_arr_to_str(fill_tags(tag_arr,dict_or,dict_and))


            file.write(f"{filename} {wr}\n")

            process.kill()
            process.wait()

            subprocess.run("pkill xviewer", shell=True, check=True)

            shutil.move(full_path,dest_bwz_source)
        file.close()

        if len(to_delte) > 0:
            for image in to_delte:
                subprocess.run(f'rm "{os.path.join(source,image)}"', shell=True, check=True)



def filter_fits(filter_arr, tag_arr):
    for or_block in filter_arr:
        contains_all = False
        for and_el in or_block:
            if tag_arr.__contains__(and_el):
                contains_all = True
            else:
                contains_all = False
                break
        if contains_all:
            return True
    return False



def handle_filter(source,dest,tx):
    move_counter = 0
    filter = input('filter: ').strip()
    ors = [i.strip() for i in filter.split('|')]
    ands = [[i.strip() for i in or_block.strip().split(' ')] for or_block in ors]

    with open(tx,'r') as reading:
        for line in reading:
            image,tags = str_to_tag_arr(line)
            if filter_fits(ands,tags):
                shutil.move(os.path.join(source,image),dest)
                move_counter += 1

        reading.close()

    subprocess.run(f'gio open {dest}',shell=True,check=True)
    return move_counter > 0


def add_or(one,two,tags):
    put = False
    for tag in one:
        if tags.__contains__(tag):
            put = True
            break
    if put:
        for tag in two:
            if not tags.__contains__(tag):
                tags.append(tag)
    return tags

def add_and(one,two,tags):
    put = False
    for tag in one:
        if tags.__contains__(tag):
            put = True
        else:
            put = False
            break

    if put:
        for tag in two:
            if not tags.__contains__(tag):
                tags.append(tag)
    return tags

def fill_tags(tags,dict_or, dict_and):
    for key, value in dict_or.items():
        tags = add_or(key.strip().split('-'),value,tags)

    for key, value in dict_and.items():
        tags = add_or(key.strip().split('-'),value,tags)

    return tags

def str_to_tag_arr(im_ta_str):
    tmp = im_ta_str.strip().split(' ')
    im = tmp[0]
    temp = tmp[1:]
    return im.strip() ,[i.strip() for i in temp]

def handle_update(tx,tmp,dict_or,dict_and):
    with open(tx,'r') as reading , open(tmp,'w') as writing:
        for line in reading:
            im,tags = str_to_tag_arr(line)
            tags = fill_tags(tags,dict_or,dict_and)
            writing.write(f"{im} {tag_arr_to_str(tags)}\n")
        reading.close()
        writing.close()

    with open(tmp, 'r') as reading, open(tx, 'w') as writing:
        for line in reading:
            writing.write(line)

        reading.close()
        writing.close()


def handle_clear(dest):
    source = 'download_folder/'

    down_dir = os.listdir(source)
    dest_dir = os.listdir(dest)

    for file in down_dir:
        if file[-6] == ')' or dest_dir.__contains__(file):
            os.remove(os.path.join(source,file))


def read_in_dict(rules_or, rules_and, dict_or, dict_and):
    with open(rules_or,'r') as file:
        for line in file:
            if line.strip() == '':
                continue

            tmp = line.strip().split(' ')
            key = tmp[0]
            value = tmp[1:]
            dict_or[key] = value
        file.close()

    with open(rules_and, 'r') as file:
        for line in file:
            if line.strip() == '':
                continue

            tmp = line.strip().split(' ')
            key = tmp[0]
            value = tmp[1:]
            dict_and[key] = value
        file.close()



if __name__ == '__main__':
    readline.read_history_file(".HISTORY")
    source = 'cute/'
    dest = 'filter/'
    tx = 'file_name.txt'
    tmp_file = 'temp.txt'
    rules_or = "rules_or.txt"
    rules_and = "rules_and.txt"

    dict_or = {}
    dict_and = {}
    read_in_dict(rules_or,rules_and,dict_or, dict_and)
    print(dict_or)
    print(dict_and)

    cmd = input('cmd: ')

    while(cmd != 'q'):
        if cmd == 'p':
            handle_put(source,tx,dict_or,dict_and)
        elif cmd == 'f':
            if handle_filter(source,dest,tx):
                cmd = input('cmd: ')
                subprocess.run(f'mv {dest}* {source}',shell=True, check=True)
                continue
        elif cmd == 'u':
            handle_update(tx,tmp_file,dict_or,dict_and)
        elif cmd == 'c':
            handle_clear(source)

        cmd = input('cmd: ')