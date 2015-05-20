__author__ = 'user'

import os
import re
from db.Page import *
from config import  config
from helper import helper

# TODO LIST
#1. remove attribute noise in the text according rule on wikipedia.
#2. build table to store information used to compute the similarity of query and documents
#3. write program to compute information used to compute the similarity of query and documents





def split_document_to_fragment(document):
    """
    :param document: the text string
    :return: fragment_list, formatted as [{"title":"this is title content","content":"content"},{},{}]
    """


    document = re.sub("\[\[(Category|Wikipedia)\:(.*?)\|(.*?)\]\]","\g<2>,\n",document,flags=re.DOTALL)



    remove_list = ["<ref>.*?</ref>","{\|.*?\|}","<.*?>","{{.*?}}","\[\[File:.*?\]\]"]
    for remove in remove_list:
        document = re.sub(remove,"",document,flags=re.DOTALL)


    replace_list = ["\[\[(.*?)\]\]","'''''(.*?)'''''","'''(.*?)'''","''(.*?)''"]
    for replace in replace_list:
        document = re.sub(replace,"\g<1>",document,flags=re.DOTALL)


    document = re.sub("^\n","",document,flags=re.MULTILINE)
    document = re.sub("^----","",document,flags=re.MULTILINE)

    document = re.sub("^[\*|#](.*?)\n","\g<1>,\n",document,flags=re.MULTILINE)





    lines = document.split("\n")

    title = lines[0]
    sub_title = ""
    fragment_list = []

    fragment_content = ""
    for line in lines[1:]:
        is_split = re.match("==.*?==",line) is not None
        if is_split:
            fragment = {"title":title+"-"+sub_title,"content":fragment_content}
            fragment_list.append(fragment)
            fragment_content = ""
            sub_title = line.strip("=").strip()
        else:
            fragment_content += line



    fragment = {"title":title+"-"+sub_title,"content":fragment_content}
    fragment_list.append(fragment)


    #do some ending work
    for f in fragment_list:
        f["content"] = re.sub("\n","",f["content"])
        f["content"] = re.sub(" ","",f["content"])
    return fragment_list



## init work

def extract_from_db_to_file_system(number_limit = -1, min_page_len = 0):
    """
    :param number_limit: the number limit , if value equal -1, it means no limit
    :param min_page_len:
    :return:
    """
    folder = "temp"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    p = Page()
    counter = 1741794
    for r in p.get_pages(number_limit,min_page_len):
        print (counter -1741794) *1.0/670471
        file_path = folder + "/" + str(counter)+".md"
        f = open(file_path,"w")
        f.write(r.page_title.encode("utf8"))
        f.write("\n")
        f.write(r.page_content)
        f.close()
        counter += 1

def save_fragment_list_to_file_system(fragment_list):
    save_path = config.fragment_file_path_1
    result = False
    for fragment in fragment_list:
        file_name = fragment["title"]
        content = fragment["content"]
        if content == "":
            continue
        try:
            f = open(save_path+"/"+file_name,"w")
            f.write(content)
            f.close()
            result = True
        except:
            result = False
    return result

def split_documents_test(file_name):
    file_name_list = [file_name]

    file_counter = 0
    for file_name in file_name_list:
        print file_counter
        #ingore hidden file
        if file_name[0] == '.':
            continue
        file_counter += 1

        file_path = config.document_file_path + "/" + file_name
        doc_file  = open(file_path,"r")
        content = doc_file.read()

        fragment_list = split_document_to_fragment(content)

        save_fragment_list_to_file_system(fragment_list)

        log_text = "%d processed file %s"%(file_counter, file_path)
        print log_text
        helper.log(log_text)
        doc_file.close()


def split_documents(start = 0):
    file_name_list = os.listdir(config.document_file_path_1)
    file_counter = 0
    for file_name in file_name_list:

        #ingore hidden file
        if file_name[0] == '.':
            continue
        file_counter += 1
        if file_counter < start:
            print "skip %d"%file_counter
            continue



        file_path = config.document_file_path_1 + "/" + file_name
        doc_file  = open(file_path,"r")
        content = doc_file.read()

        fragment_list = split_document_to_fragment(content)
        save_fragment_list_to_file_system(fragment_list)

        log_text = "%d processed file %s"%(file_counter, file_path)
        if file_counter % 100 == 0:
            print file_counter

        helper.log(log_text)
        doc_file.close()













