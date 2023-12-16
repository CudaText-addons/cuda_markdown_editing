import re
import os
from cudatext import *
import cudatext_cmd as cmds

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
fn_section = 'markdown_editing'

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
    insert_busy = False

    def log(self,s):
        #print('MD:', s)
        pass

    def is_separ_line(self, ed, y, x):
        s = ed.get_text_line(y)
        #s0 = ed.get_text_line(y-1) if y>0 else ''
        return (s.startswith('---') and x>=3) or \
               (s.startswith('- - -') and x>=5) or \
               (s.startswith('* * *') and x>=5)

    def __init__(self):

        self.MAX_HASHES=6
        self.DOUBLE_MAX_HASHES=self.MAX_HASHES*2
        self.bullets_=ini_read(fn_config, fn_section, 'list_indent_bullets', '*+-')
        self.bullets=self.bullets_
        self.match_header_hashes=str_to_bool(ini_read(fn_config, fn_section, 'match_header_hashes', '0'))
        self.paired_chars=ini_read(fn_config, fn_section, 'paired_chars', '"*~`')
        self.need_doubling_res=self.match_header_hashes
        if self.bullets=='':
            self.bullets='*'
        self.bullets+=self.bullets[0]
        for i in '*-+':
            if not i in self.bullets:
                self.bullets+=i+i
        barr=[]
        for i in self.bullets:
            barr.append(i)
        self.barr=barr

    def config(self):

        ini_write(fn_config, fn_section, 'list_indent_bullets', self.bullets_)
        ini_write(fn_config, fn_section, 'match_header_hashes', bool_to_str(self.match_header_hashes))
        ini_write(fn_config, fn_section, 'paired_chars', self.paired_chars)
        file_open(fn_config)

        lines = [ed.get_text_line(i) for i in range(ed.get_line_count())]
        try:
            index = lines.index('['+fn_section+']')
            ed.set_caret(0, index)
        except:
            pass

    def on_key(self, ed_self, key, state):
        carets = ed_self.get_carets()
        #dont support multi-carets
        if len(carets)>1: return

        if key==51:
            # hash symbol
            caret = carets[0]
            if 's' in state:
                x1,y1,x2,y2=caret
                if y2!=-1 and  x2!=-1:
                    if x2>x1:
                        x2+=1
                    else:
                        x1+=1
                    if x2<x1:
                        x1,x2=x2,x1
                    if self.need_doubling_res:
                        str_old=ed_self.get_text_line(y2)
                        self.log(str_old[-1])
                        if not str_old[-1] in [' ','#']:
                          ins=' #'
                        else:
                          ins='#'
                        ed_self.insert(x2-1,y2,ins)
                    str_old=ed_self.get_text_line(y2)
                    if not (str_old[0]in [' ','#']):
                    	ed_self.insert(0,y2,' ')
                    ed_self.insert(0,y2,'#')
                    ln=ed_self.get_text_line(y1)
                    i=0
                    for ch in ln:
                        if ch=='#':
                            i+=1
                        else:
                            break
                    if i<=self.MAX_HASHES:
                        ed_self.set_caret(i,y1,len(ln),y1)
                    else:
                        while(len(ln)>0):
                            if ln[0]=='#':
                                ln=ln[1:]
                            elif ln[-1]=='#':
                                ln=ln[:-1]
                            else:
                                break
                            ed_self.set_text_line(y1,ln)
                            ed_self.set_caret(0,y1,len(ln),y1)
                    return False
                else:
                    y   = caret[1]
                    st  = ed_self.get_text_line(y)
                    sto = st
                    if len(st)>0:
                        self.log('k1')
                        while (len(st)>0)  and (st[0] in [' ','\t','#']):
                            self.log('k2')
                            st=st[1:]
                    else:
                    	return True
                    self.log('k3')
                    i=0
                    numres=0
                    st  = ed_self.get_text_line(y)
                    for i in st:
                    	self.log('k4')
                    	if i=='#':numres+=1
                    	else:break
                    if(numres>=self.MAX_HASHES):# and (not self.need_doubling_res)) or (numres>=self.DOUBLE_MAX_HASHES):
                        ed_self.set_text_line(y,' ')
                        ed_self.set_caret(0,y)
                        return False
                    else:
                        pass
        elif key==192:
            # ~   simbol
            if 's' in state:
                symm='~~'
            else:
                symm='`'
            caret = carets[0]
            x1,y1,x2,y2 = caret
            if (x2<x1 and y2==y1) or y2<y1:
                if x2!=-1 or y2!=-1:
                    x2,x1=x1,x2
                    y2,y1=y1,y2
            self.log('h1')
            if (x2 != -1) or (y2 != -1):
                self.log(str(x2)+' '+str(y2))
                if (y2>y1) or ((y2==y1) and (x2>x1)):
                    ed_self.insert(x2,y2,symm)
                    ed_self.insert(x1,y1,symm)
                else:
                    ed_self.insert(x2,y2,symm)
                    ed_self.insert(x1,y1,symm)
                if symm=='`':
                    if y2==y1:
                        ed_self.set_caret(x1+1,y1, x2+1,y2)
                    else:
                        ed_self.set_caret(x1+1,y1, x2,y2)
                else:
                    if y2==y1:
                        ed_self.set_caret(x1+2,y1, x2+2,y2)
                    else:
                        ed_self.set_caret(x1+2,y1, x2,y2)
                return False
        elif key==13:
            # Enter
            caret = carets[0]
            lnum=caret[1] # line number
            xnum=caret[0] # column
            str_old=ed_self.get_text_line(lnum)
            if not str_old: #None or empty str
                return
            len_old=len(str_old)

            if self.is_separ_line(ed_self, lnum, xnum):
                return

            str_add_f=''
            indent=1
            if str_old[0]=='>':
                p=''
                while len(str_old)>0:
                    if str_old[0] in [' ','>','\t']:
                        p+=str_old[0]
                        str_old=str_old[1:]
                    else:
                        break
                ed_self.insert(len_old,lnum,'\n'+p)
                ed_self.set_caret(len(p),lnum+1)
                return False
            if len(str_old)==0:
                return True
            self.log('st0'+str_old)
            resnum=0
            #if str_old[0]=='#':
            for i in str_old:
                if i=='#':
                    resnum+=1
                else:
                    break
            if self.need_doubling_res and resnum>0:
            	ed_self.insert(len(str_old),lnum,' '+'#'*resnum+'\n')
            	ed_self.set_caret(0,lnum+1)
            	return False
            while len(str_old)>0 and (str_old[0] in [' ','\t']):
                str_add_f+=str_old[0]
                str_old=str_old[1:]
                indent+=1
            if not str_old:
                return True
            self.log('nn'+str_old)
            if str_old[0] in '-+*':
                is_gfm = (str_old[2:5] in ['[ ]','[X]','[x]'])
                if len(str_old)==1 and str_old[0]=='-':
                    return True
                if str_old[0]=='-' and not str_old[1]==' ':
                    return True
                if str_old[0]=='*':
                    if '*' in str_old[1:] and not str_old[1]==' ':
                        return True
                x,y = ed_self.get_carets()[0][:2]
                empty=True
                for i in str_old:
                    if not i in [' ','\t']:
                        if not i in '*-+':
                            empty=False
                if empty:
                    ed_self.set_text_line(y,' '*x)
                    ed_self.set_caret(x-2,y)
                    return False
                x,y = ed_self.get_carets()[0][:2]
                ggf=(' [ ] ' if is_gfm else ' ')
                ed_self.insert(x,y,'\n'+str_add_f+str_old[0]+ggf)
                ed_self.set_caret(indent+len(ggf),ed_self.get_carets()[0][1]+1)
                return False
            num_arr=['1','2','3','4','5','6','7','8','9','0']
            if str_old[0] in num_arr:
                s=''
                i=0
                ll=len(str_old)
                str_old+=' '
                while(str_old[i] in num_arr) and (i<ll):
                    s=s+str_old[i]
                    i = i+1
                if (i<ll):
                    if(str_old[i]=='.'):
                        f=True
                        for k in range(i+1,len(str_old)):
                            if not str_old[k] in [' ','\t']:
                                f=False
                        if f:
                            ed_self.set_text_line(lnum,str_add_f)
                            ed_self.set_caret(indent-1 if indent>0 else 0,lnum)
                            return False
                        nm=int(s)
                        car = ed_self.get_carets()[0]
                        ed_self.insert(car[0],car[1],'\n'+str_add_f+str(nm+1)+'. ')
                        ed_self.set_caret(len(str_add_f+str(nm+1)+'. '),car[1]+1)
                        return False
        elif key==190:
            # > symbol
            caret = carets[0]
            if 's' in state:
                x1,y1,x2,y2=caret
                if x2==-1 and y2==-1:
                	return True
                if y2<y1:
                    y1, y2 = y2, y1
                for i in range(y1, y2+1):
                    ed_self.insert(0,i,'> ')
                return False
        elif key==32:
            # space
            caret = carets[0]
            x,y,x1,y1 = caret

            if x==0:
                return
            strt=ed_self.get_text_substr(x-1,y,x+1,y)
            if len(strt)<2:
                return True
            if strt[0]=='*' and strt[1]=='*':
                ed_self.delete(x,y,x+1,y)
            if strt[0] in['"',"'","`"] and strt[0]==strt[1]:
                ed_self.delete(x,y,x+1,y)
            if strt[0:2] in ['()','[]','{}']:
                ed_self.delete(x,y,x+1,y)
        elif key==8:
            # backspace
            caret = carets[0]
            x,y,x1,y1 = caret
            subst=ed_self.get_text_substr(x-1,y,x+1,y)
            if subst in ["''" , '""' , '{}' , '[]' , '()', '**', '``', '~~']:
                ed_self.delete(x-1,y,x+1,y)
                ed_self.set_caret(x-1,y)
                return False
        elif key==9:
            #tab symbol
            caret = carets[0]
            if ed_self.get_prop(PROP_TAB_COLLECT_MARKERS, '') and ed_self.markers(MARKERS_GET):
                return
            if not state in ('','s'):
                return True
            indent_size=ed_self.get_prop(PROP_INDENT_SIZE)
            str_old_num=caret[1]
            str_old=ed_self.get_text_line(str_old_num)
            if str_old=='':
            	return True
            if 's' in state:
                #str_old=str_old=ed_self.get_text_line(str_old_num)

                if str_old[0] in [' ','\t']:
                    if str_old[0]==' ':
                        str_old=str_old[1:]
                    str_old=str_old[1:]
                    i=''
                    while str_old[0] in [' ','\t']:
                        i=i+str_old[0]
                        str_old=str_old[1:]
                    sym=str_old[0]
                    if len(str_old)>0:
                        while str_old[0] in '0123456789':
                            str_old=str_old[1:]
                            if len(str_old)==0:
                                break
                    wt=str_old[1:]
                    if sym in '*-+':
                        j=len(self.barr)-1
                        while self.barr[j]!=sym:
                            j-=1
                        sym=self.barr[j-1]
                    else:
                        sym=self.bullets[0]+' '
                    ed_self.set_text_line(str_old_num,i+sym+wt)
                    ed_self.set_caret(len(i)+2, str_old_num)
                i=0
                return False

            if len(str_old)==0:
                return True
            str_old=ed_self.get_text_line(str_old_num)
            self.log('so='+str_old)
            if str_old[0] in '-=' :
                self.log('kpa')
                if str_old_num>0:#len(str_old)>=2:
                    preline=ed_self.get_text_line(str_old_num-1)
                    f=False
                    if len(preline)>0:
                        if preline[0].isalpha() or preline[0].isdigit():
                            f=True
                    if not f:
                        return True
                    same=True
                    for i in str_old:
                        if not i in [' ','\t','-','='] :
                            same=False
                    if same:
                        str_old=str_old[0]
                        x,y = ed_self.get_carets()[0][:2]
                        for i in range(len(str_old), len(ed_self.get_text_line(str_old_num-1))):
                            str_old+=str_old[0]
                        ed_self.set_text_line(y,str_old)
                        ed_self.set_caret(len(str_old),y)
                        return False
            str_syms='1234567890.'
            str_indent=''
            while len(str_old)>0 and (str_old[0] in [' ','\t']):
                str_indent+=str_old[0]
                str_old=str_old[1:]
            is_numbered=False
            if len(str_old)>0:
                while str_old[0] in str_syms:
                    is_numbered=True
                    str_old=str_old[2:]
                    if len(str_old)==0:
                        break
            self.log('kp0')
            if is_numbered:
                ed_self.set_text_line(str_old_num,str_indent+' '*indent_size+'1.'+str_old)
                ed_self.set_caret(len(ed_self.get_text_line(str_old_num)),str_old_num)
                return False
            #barr=['*','-','+','\\']
            def nextb(curb):
                i=0
                for j in self.barr:
                    if j==curb:
                        return self.barr[(i+1)%len(self.barr)]
                    else:
                        i+=1
                return barr[0]
            if len(str_old)==0:return
            self.log('kp1')
            if str_old[0]in self.barr:
                self.log('kp2')
                if str_old[0]=='*':
                    x,y=ed_self.get_carets()[0][:2]
                    strt=ed_self.get_text_line(y)
                    while(strt[0] in [' ','\t']):
                        strt=strt[1:]
                    strt=strt[1:]
                    if '*' in strt:
                        return False
                    else:
                        ed_self.insert(0,y,' '*indent_size)
                x,y = ed_self.get_carets()[0][:2]
                if str_old[2:]=='':
                    ed_self.set_text_line(y,str_indent+' '*indent_size+nextb(str_old[0])+' '+str_old[2:])
                ed_self.set_caret(x+indent_size,y)
                return False
            return True
        elif key in (56, 106):
        # * and NumPad *
            caret = carets[0]
            if 's' in state:
                x1,y1,x2,y2=caret
                if (x2!=-1 and y2!=-1) and((x2<x1 and y2==y1) or y2<y1):
                    x1,x2=x2,x1
                    y2,y1=y1,y2
                if x2==-1 and y2==-1:
                    #ed_self.insert(x1,y1,'**')
                    self.log('h2')
                    return True
                self.log('h2')
                ed_self.insert(x2,y2,'*')
                ed_self.insert(x1,y1,'*')
                if y2==y1:
                    ed_self.set_caret(x1+1,y1,x2+1,y2)
                else:
                    ed_self.set_caret(x1+1,y1,x2,y2)
                return False
        elif key==189:
            # _ symbol
            caret = carets[0]
            self.log(189)
            if 's' in state:
                x1,y1,x2,y2=caret
                if x2==-1 and y2==-1:
                    ed_self.insert(x1,y1,'__')
                    ed_self.set_caret(x1+1,y1)
                    return False
                if (x2<x1 and y2==y1) or y2<y1:
                    x1,x2=x2,x1
                    y1,y2=y2,y1
                ed_self.insert(x2,y2,'_')
                ed_self.insert(x1,y1,'_')
                if (y2==-1) and (x2==-1):
                    return False
                if y2==y1:
                    ed_self.set_caret(x1+1,y1,x2+1,y2)
                else:
                    ed_self.set_caret(x1+1,y1,x2,y2)
                return False
        else:
            self.log(key)

    def on_insert(self, ed_self, text):
        if self.insert_busy: return
        carets = ed.get_carets()
        if len(carets)>1: return
        x, y, x2, y2 = carets[0]

        if len(text)==1 and (text in self.paired_chars):
            self.log('dup char')
            #don't work on typing header
            if text=='#' and not self.need_doubling_res:
                return
            #don't work on typing list-char
            if text=='*' and (x==0):
                return
            #don't work after triple ticks
            if text=='`' and ed.get_text_line(y).startswith('``'):
                if x==1:
                    ed_self.set_caret(x+1, y, -1, -1)
                return

            self.insert_busy = True
            ed_self.insert(x, y, text)
            self.insert_busy = False
            #return value None: app will enter paired char

    def menu_ref(self):
        fnd = re.findall(r"(\[.*?\]):\s+<?(https?://[^>\s\n\r]+)", ed.get_text_all(), re.M)
        if not fnd:
            return msg_status(_('No references found'))
        items = [i[0]+': '+i[1] for i in fnd]
        res = dlg_menu(DMENU_LIST, items, caption=_('References'))
        if res is None:
            return
        s = fnd[res][0]
        ed.cmd(cmds.cCommand_TextInsert, s)
        msg_status(_('Reference inserted'))
