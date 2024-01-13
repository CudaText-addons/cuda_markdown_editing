import re
from cudatext import *

pattern1 = re.compile(r'^(#*) ([\d\. ]*)', 0)
pattern2 = re.compile(r'^([\d\. ]*)', 0)

treeid = app_proc(PROC_GET_CODETREE, '')

def add_index(text, index):

    if pattern1.match(text):
        newtext = pattern1.sub(rf'\1 {index}', text)
    elif pattern2.match(text):
        newtext = pattern2.sub(rf'{index}', text)
    else:
        newtext = text
    return newtext

def index_headers():

    #h1,h2,h3,h4,h5,h6 = 1,1,1,1,1,1
    for h1,item1 in enumerate(tree_proc(treeid, TREE_ITEM_ENUM_EX, id_item=0) or []):
        #print(item1,h1+1)
        x1,y1,x2,y2=tree_proc(treeid, TREE_ITEM_GET_RANGE, id_item=item1['id'])
        text = ed.get_text_line(y1)
        newtext = add_index(text,str(h1+1)+'. ')
        ed.set_text_line(y1, newtext)
        if item1['sub_items']:
            for h2,item2 in enumerate(tree_proc(treeid, TREE_ITEM_ENUM_EX, id_item=item1['id'])):
                #print(item2,h2)
                x1,y1,x2,y2=tree_proc(treeid, TREE_ITEM_GET_RANGE, id_item=item2['id'])
                text = ed.get_text_line(y1)
                newtext = add_index(text,str(h1+1)+'.'+str(h2+1)+'. ')
                ed.set_text_line(y1, newtext)
                if item2['sub_items']:
                    for h3,item3 in enumerate(tree_proc(treeid, TREE_ITEM_ENUM_EX, id_item=item2['id'])):
                        x1,y1,x2,y2=tree_proc(treeid, TREE_ITEM_GET_RANGE, id_item=item3['id'])
                        text = ed.get_text_line(y1)
                        newtext = add_index(text,str(h1+1)+'.'+str(h2+1)+'.'+str(h3+1)+'. ')
                        ed.set_text_line(y1, newtext)
                        if item3['sub_items']:
                            for h4,item4 in enumerate(tree_proc(treeid, TREE_ITEM_ENUM_EX, id_item=item3['id'])):
                                x1,y1,x2,y2=tree_proc(treeid, TREE_ITEM_GET_RANGE, id_item=item4['id'])
                                text = ed.get_text_line(y1)
                                newtext = add_index(text,str(h1+1)+'.'+str(h2+1)+'.'+str(h3+1)+'.'+str(h4+1)+'. ')
                                ed.set_text_line(y1, newtext)
                                if item4['sub_items']:
                                    for h5,item5 in enumerate(tree_proc(treeid, TREE_ITEM_ENUM_EX, id_item=item4['id'])):
                                        x1,y1,x2,y2=tree_proc(treeid, TREE_ITEM_GET_RANGE, id_item=item5['id'])
                                        text = ed.get_text_line(y1)
                                        newtext = add_index(text,text,str(h1+1)+'.'+str(h2+1)+'.'+str(h3+1)+'.'+str(h4+1)+'.'+ str(h5+1)+'. ')
                                        ed.set_text_line(y1, newtext)
                                        if item5['sub_items']:
                                            for h6,item6 in enumerate(tree_proc(treeid, TREE_ITEM_ENUM_EX, id_item=item5['id'])):
                                                x1,y1,x2,y2=tree_proc(treeid, TREE_ITEM_GET_RANGE, id_item=item6['id'])
                                                text = ed.get_text_line(y1)
                                                newtext = add_index(text,str(h1+1)+'.'+str(h2+1)+'.'+str(h3+1)+'.'+str(h4+1)+'.'+str(h5+1)+'.'+ str(h6+1)+'. ')
                                                ed.set_text_line(y1, newtext)
    
