import os
import shutil
import signal
import subprocess

def tag_arr_to_str(tags):
    ret = ''
    for tag in tags:
        ret+=(str(tag)+' ')
    return ret.strip()

def handle_put(dest_bwz_source,tx):
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
            if images.__contains__(filename):
                to_delte.append(filename)
                continue

            move_counter+=1
            full_path = os.path.join(source, filename)
            process = subprocess.Popen(f'gio open {full_path}', shell=True)
            tags = input("tags : ")
            tag_arr = tags.split(' ')
            wr = tag_arr_to_str(fill_tags(tag_arr))


            file.write(f"{filename} {wr}\n")

            process.kill()
            process.wait()

            subprocess.run("pkill xviewer", shell=True, check=True)

            shutil.move(full_path,dest_bwz_source)
        file.close()

        if len(to_delte) > 0:
            for image in to_delte:
                subprocess.run(f'rm {os.path.join(source,image)}', shell=True, check=True)



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

def fill_tags(tags):
    tags = add_or(['hund'], ['doggo'], tags)
    tags = add_or(['doggo','kitty'],['cute','sues'],tags)
    tags = add_and(['doggo','cute'],['super'],tags)
    tags = add_and(['kitty', 'cute'], ['super'], tags)
    tags = add_and(['k', 'j',], ['noice'], tags)

    return tags

def str_to_tag_arr(im_ta_str):
    tmp = im_ta_str.strip().split(' ')
    im = tmp[0]
    temp = tmp[1:]
    return im.strip() ,[i.strip() for i in temp]

def handle_update(tx,tmp):
    with open(tx,'r') as reading , open(tmp,'w') as writing:
        for line in reading:
            im,tags = str_to_tag_arr(line)
            tags = fill_tags(tags)
            writing.write(f"{im} {tag_arr_to_str(tags)}\n")
        reading.close()
        writing.close()

    with open(tmp, 'r') as reading, open(tx, 'w') as writing:
        for line in reading:
            writing.write(line)

        reading.close()
        writing.close()



if __name__ == '__main__':
    source = 'cute/'
    dest = 'filter/'
    tx = 'file_name.txt'
    tmp_file = 'temp.txt'
    cmd = input('cmd: ')
    while(cmd != 'q'):
        if cmd == 'p':
            handle_put(source,tx)
        elif cmd == 'f':
            if handle_filter(source,dest,tx):
                cmd = input('cmd: ')
                subprocess.run(f'mv {dest}* {source}',shell=True, check=True)
                continue
        elif cmd == 'u':
            handle_update(tx,tmp_file)

        cmd = input('cmd: ')