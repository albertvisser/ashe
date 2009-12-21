import os,sys,shutil
import types
from Tkinter import *
import tkMessageBox
import tkFileDialog
import mytkSimpleDialog as tkSimpleDialog
import Tree
import BeautifulSoup as bs
TITEL = "Albert's Simple HTML-editor"
"""
keuze: GEEN validatie, hooguit met Tidy vanuit het hoofdmenu aanroepen
todo:
    insert keuzes afmaken
    paste under toevoegen
    save functie afmaken
"""
cut_obj = None
cut_el = None
id_tabel = {}

if os.name == 'ce':
    DESKTOP = False
else:
    DESKTOP = True

#----------------------------------------------------
# site-packages/treedemo/treedemo-complex laat wel het toevoegen van een child zien maar niet het
# toevoegen van een expandable child. Wel weer dat op het child ook een context menu mogelijk is
# het vasthouden in de databron van de tree zit er weer niet in
#
# site-packages/treedemo/treedemo-dnd is voor drag-en drop support, dat wil ik er tzt ook in hebben
# het vasthouden in de databron van de tree zit hier ook niet in
#
#----------------------------------------------------


#  routine om een nieuw id voor een tree element te bepalen
def bepaal_new_id(node,data):
    # bepaal de id's onder de parent
    """
    node is een MyNodes instantie
    data is een tuple bestaande uit een naam en een list van attribuut
    naam-waarde paren, bv. ('p', [('name', 'hallo'), ('type', 'snorkie')])
    -- tenminste, bij elementen, maar hoe zit het met tekst?
    daar is het een string (de tekst)
    """
    if type(data) is str:
        return "text",data
    tag_soort = data[0]
    tag_id = ""
    for naam,waarde in data[1]:
        if naam == "id":
            tag_id = waarde
        elif naam == "name" and not tag_id:
            tag_id = waarde
    if not tag_id:
        id_list = [x.id[1] for x in node.parent().children() if x.id[0] == tag_soort]
        if len(id_list) == 0:
            tag_id = '0'
        else:
            ## print id_list
            ## print max(id_list)
            ## print max(id_list,key=int)
            tag_id = str(int(max(id_list,key=int)) +1)
    return tag_soort,tag_id

# routines om een (BeautifulSoup) Tag of NavigableString onder een andere tag te hangen
def insert_start(parent,child):
    parent.insert(0,child)

def insert_pos(parent,child,pos):
    parent.insert(pos,child)

def insert_end(parent,child):
    parent.insert(len(parent),child)

def getshortname(x,attr=False):
    if attr:
        t = x[1]
        if t[-1] == "\n": t = t[:-1]
    else:
        t = x.split("\n",1)[0]
    w = 20
    if DESKTOP:
        w = 80
    if len(t) > w: t = t[:w].lstrip() + '...'
    if attr:
        return " = ".join((x[0],t))
    else:
        return t
def getidee(x):
    """bepaalt een id voor de widget node op basis van tagnaam en
    eventuele identificator van de html node.
    als die er niet is, kent-ie hem toe en zet hem in de html"""
    ## print type(x)
    try:
        idee = x["id"]
    except:
        pass
    else:
        return x.name,idee
    try:
        idee = x["name"]
    except:
        pass
    else:
        return x.name,idee
    try:
        idee = x["my_id"]
    except:
        pass
    else:
        return x.name,idee
    if isinstance(x,bs.NavigableString):
        idee = x.string
        return "text",idee
    if x.name in id_tabel:
        id_tabel[x.name] += 1
    else:
        id_tabel[x.name] = 0
    idee = str(id_tabel[x.name])
    x["my_id"] = idee
    return x.name,idee


def bepaal_xmlnode(x):
    """bepaal de xml node bij een widget node
    omdat getidee hem in de html tree overneemt is er altijd een aanwezig"""
    name = x.get_label()
    h = x.widget.data
    print 'bepaalxmlnode:',name,x.full_id(),
    if len(x.full_id()) == 1:
        ix = None
    else:
        s = []
        for i in x.full_id()[1:]:
            ix = 0
            for y in h.contents:
                ## print y
                if y == "\n":
                    pass # continue
                elif isinstance(y,bs.Declaration):
                    if type(i) is str and i == "dtd":
                        h = y
                        break
                elif isinstance(y,bs.NavigableString):
                    if i[0] == "text" and y.string == i[1]:
                        h = y
                        break
                elif y.name == i[0]:
                    try:
                        vgl = y["id"]
                    except:
                        try:
                            vgl = y["name"]
                        except:
                            vgl = y["my_id"]
                    if vgl == i[1]:
                        h = y
                        break
                ix += 1
    print ix
    return h,ix

class AttrDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        hfr = Frame(master)
        hfr.pack(fill=BOTH,expand=YES)

        frm = Frame(hfr)
        frm.pack(fill=X)
        Label(frm, text="Name:").pack(side=LEFT)
        self.e1 = Entry(frm)
        self.e1.insert(0,self.parent.e12[0])
        self.e1.pack(side=LEFT,expand=YES, fill=X)

        frm = Frame(hfr)
        frm.pack(fill=X)
        Label(frm, text="Value:").pack(side=LEFT)
        self.e2 = Entry(frm)
        self.e2.insert(0,self.parent.e12[1])
        self.e2.pack(side=LEFT,expand=YES, fill=X)

        return self.e1 # initial focus

    def validate(self):
        nam = self.e1.get()
        val = self.e2.get()
        if nam == "" or val == "":
            return False
        return True

    def apply(self):
        nam = self.e1.get()
        val = self.e2.get()
        self.result = nam, val

class MultiListbox(Frame):
    def __init__(self, master, lists, rows=0):
        Frame.__init__(self, master)
        self.lists = []
        for l,w in lists:
            frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                relief=FLAT, exportselection=FALSE)
            if rows != 0:
                lb.configure(height=rows)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = Frame(self); frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand']=sb.set

    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            apply(l.yview, args)

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

class ElementDialog(tkSimpleDialog.Dialog):
    # het tekstvak mag achterwege blijven,
    # moet niet op het bovenliggende tag"
    def body(self,master):
        tag = ''
        attrs = []
        if self.parent.e12[0] is not None:
            tag = self.parent.e12[0]
        if len(self.parent.e12) > 1:
            if self.parent.e12[1] is not None:
                attrs = self.parent.e12[1]
        h3 = 3
        wa = 8
        wv = 19
        hfr = master
        if DESKTOP:
            h3 = 4
            wa = 10
            wv = 40
            hfr = Frame(master)
            hfr.pack(expand=YES,fill=BOTH)

        frm = Frame(hfr) # ,borderwidth=2,relief=GROOVE)
        frm.pack()
        lb = Label(frm, text="element: ")
        self.e1 = Entry(frm,width=20)
        self.e1.insert(END,tag)
        if tag != '':
            self.e1.config(state=DISABLED)
        lb.pack(side=LEFT)
        self.e1.pack(side=LEFT)

        frm = Frame(hfr,borderwidth=2,relief=GROOVE)
        frm.pack(expand=YES,fill=BOTH)
        self.mlb = MultiListbox(frm, (('attribute', wa), ('value', wv)), rows=h3)
        for x,y in attrs:
            self.mlb.insert(END, (x, y))
        self.mlb.pack(expand=YES,fill=BOTH)
        sfr = Frame(frm)
        sfr.pack()
        t1,t2,t3 = "Edit","Add New","Delete"
        if DESKTOP:
            t1,t2,t3 = "Edit attribute",'Add new attribute','Delete selected'
        b1 = Button(sfr,text = t1, command = self.editattr)
        b1.pack(side=LEFT)
        b2 = Button(sfr,text = t2, command = self.addattr)
        b2.pack(side=LEFT)
        b3 = Button(sfr,text = t3, command = self.delattr)
        b3.pack(side=LEFT)

        if self.parent.e12[0] is None:
            return self.e1
        else:
            return self.mlb

    def valattr(self):
        # routine om te zorgen dat er alleen passende attributen worden opgegeven
        # beperken tot controle beide rubrieken ingevuld
        nam = self.e1.get()
        val = self.e2.get()
        if nam == "" or val == "":
            return False
        return True

    def addattr(self):
        #  toon hulpdialoogje om attribuut met waarde op te voeren
        self.e12 = "",""
        h = AttrDialog(self)
        if h.result is not None:
            ## x,y = h.result
            ## self.mlb.insert(END, (x, y))
            self.mlb.insert(END, h.result)

    def editattr(self):
        #  bepaal geselecteerde regel
        i =  self.mlb.curselection()
        ## print i, self.mlb.index(i)
        self.e12 = self.mlb.get(i[0])
        h = AttrDialog(self)
        if h.result is not None:
            ## x,y = h.result
            self.mlb.delete(i)
            ## self.mlb.insert(i, (x, y))
            self.mlb.insert(i, h.result)

    def delattr(self):
        # bepaal geselecteerde regel
        if tkMessageBox.askyesno(TITEL,"Weet u het zeker?"):
            i =  self.mlb.curselection()
            self.mlb.delete(i)

    def validate(self):
        # routine om te zorgen dat alleen bestaande/toegestane tags kunnen worden opgegeven
        # beperken tot controle tagnaam ingevuld
        nam = self.e1.get()
        if nam == "":
            return False
        return True

    def apply(self):
        e1 = self.e1.get()
        e2 = []
        for x in self.mlb.get(0,END):
            e2.append(x)
        self.result = e1, e2

class TextDialog(tkSimpleDialog.Dialog):
    def body(self,master):
        txt = ''
        self.pref = ''
        if self.parent.e12 is not None:
            txt = self.parent.e12.strip()
            i = self.parent.e12.find(txt)
            if i > -1:
                self.pref = self.parent.e12[:i]

        w2 = 25
        h2 = 5
        hfr = master
        if DESKTOP:
            w2 = 50
            h2 = 16
            hfr = Frame(master)
            hfr.pack(fill=BOTH,expand=YES)

        frm = Frame(hfr,borderwidth=2,relief=GROOVE)
        frm.pack(expand=YES,fill=BOTH)
        self.e2 = Text(frm,width=w2,height=h2,wrap=WORD)
        self.e2.insert(END,txt)
        self.e2.pack(fill=BOTH,expand=YES)

        return self.e2

    def apply(self):
        e2 = self.e2.get(1.0,END)
        if e2[-1] == "\n":
            e2 = e2[:-1]
        self.result = self.pref + e2

class MyNodes(Tree.Node):
    def __init__(self, *args, **kw_args):
        # call superclass
        apply(Tree.Node.__init__, (self,)+args, kw_args)
        # bind right-click
        if DESKTOP:
            self.widget.tag_bind(self.symbol, '<3>', self.popup_menu)
            self.widget.tag_bind(self.label, '<Button-3>', self.popup_menu)
        else:
            self.widget.tag_bind(self.symbol, '<1>', self.popup_menu)
            self.widget.tag_bind(self.label, '<Button-1>', self.popup_menu)
        self.widget.tag_bind(self.label, '<Double-Button-1>', self.edit)

    # pop up menu on right click
    def popup_menu(self, event):
        h,ix = bepaal_xmlnode(self)
        menu = Menu(self.widget, tearoff=0)
        if len(self.full_id()) == 1:
            has_doctype = False
            for x in [d for d in h.contents if d != '\n']:
                if isinstance(x,bs.Declaration) and x.startswith("DOCTYPE"):
                    has_doctype = True
                    break
            if not has_doctype:
                menu.add_command(label='Add doctype', command=self.add_dt)
        else:
            is_text = False
            try:
                x = h.name
            except:
                is_text = True

            menu.add_command(label='Edit', command=self.edit)
            menu.add_command(label='Cut', command=self.cut)
            if not is_text:
                if cut_obj:
                    menu.add_command(label='Paste Before', command=self.paste)
                    menu.add_command(label='Paste After', command=self.paste_aft)
                    menu.add_command(label='Paste Under', command=self.paste_under)
                else:
                    menu.add_command(label='Paste', command=self.paste,
                                     state='disabled')
                menu.add_command(label='Insert Before', command=self.ins_bef)
                menu.add_command(label='Insert After', command=self.ins_aft)
                insertmenu = Menu(self.widget,tearoff=False)
                menu.add_cascade(label="Insert Under", menu=insertmenu)
                insertmenu.add_command(label='Tag', command=self.ins_chld)
                insertmenu.add_command(label='Text', command=self.ins_text)
        menu.tk_popup(event.x_root, event.y_root)

    def add_dt(self): # add Doctype declaration
        self.widget.e12 = "DOCTYPE html PUBLIC "
        h = TextDialog(self.widget)
        if h.result is not None:
            name = h.result
            if name.startswith("DOCTYPE"):
                # in de html tree opvoeren
                h,ix = bepaal_xmlnode(self)
                h.insert(0,name)
                # zichtbaar maken
                n=self.widget.add_list(name=getshortname(name),
                                             id="dtd",
                                             flag=0)
                if not self.expandable():
                    self.expandable_flag = True
                self.insert_children(n) # ,d.result,elem=True)

    def edit(self,evt=None):
        # afhankelijk van item: element of attribute dialoog
        name = self.get_label()
        ## print name
        if len(self.full_id()) == 1:
            # wel mogelijk maken doctype toe te voegen
            tkMessageBox.showwarning('Helaas...','root element kan niet aangepast worden')
            return
        if name.startswith("DOCTYPE"):
            self.widget.e12 = name
            h = TextDialog(self.widget)
            if h.result is not None:
                # zichtbaar maken
                name = h.result
                self.set_label(getshortname(name))
                # aanpassen in html tree
                h,ix = bepaal_xmlnode(self)
                h.parent.replaceWith(name)
        else:
            h,ix = bepaal_xmlnode(self)
            is_text = False
            try:
                naam = h.name
            except:
                is_text = True
            if is_text:
                ## print h
                self.widget.e12 = h
                d = TextDialog(self.widget)
                if d.result is not None:
                    # in de html tree verwerken
                    h.replaceWith(d.result)
                    # zichtbaar maken
                    self.set_label(getshortname(d.result))
                    self.widget.frm.prnt.setmodified(True)
            else:
                self.widget.e12 = (h.name,h.attrs)
                d = ElementDialog(self.widget)
                if d.result is not None:
                    if d.result[0] != h.name:
                        h.name = d.result[0]
                        naam = d.result[0]
                        self.widget.frm.prnt.setmodified(True)
                    if d.result[1] != h.attrs:
                        h.attrs = d.result[1]
                        self.widget.frm.prnt.setmodified(True)
                        for x in h.attrs:
                            if x[0] in ("name","id"):
                                naam = '%s %s="%s"' % (naam,x[0],x[1])
                    # zichtbaar maken
                    self.set_label(naam)
                    # in de html tree verwerken (hopenlijk)
                    h.name = d.result[0]

    def cut(self):
        global cut_id, cut_name, cut_label, cut_expanded_icon, \
               cut_collapsed_icon, cut_expandable_flag, cut_obj, \
               cut_el

        cut_obj=1
        cut_id=self.id
        cut_expanded_icon=self.expanded_icon
        cut_collapsed_icon=self.collapsed_icon
        cut_expandable_flag=self.expandable_flag
        cut_name=self.get_label()
        # in de html tree verwerken
        h,ix = bepaal_xmlnode(self) # zoek de node
        h.extract()
        cut_el = h
        # zichtbaar maken
        self.delete()
        self.widget.frm.prnt.setmodified(True)

    def paste_under(self):
        global cut_el,cut_att
        # in de html tree verwerken
        h,ix = bepaal_xmlnode(self) # zoek de node,
        if cut_el is not None:
            insert_end(h,cut_el)
        # zichtbaar maken
        self.insert_children(
            self.widget.add_list(name=cut_name,
                                 id=cut_id,
                                 flag=cut_expandable_flag,
                                 expanded_icon=cut_expanded_icon,
                                 collapsed_icon=cut_collapsed_icon))
        cut_el = None
        cut_obj = None
        self.widget.frm.prnt.setmodified(True)

    def paste_aft(self):
        self.paste(before=False)

    def paste(self,evt=None,before=True):
        global cut_el,cut_att
        h,ix = bepaal_xmlnode(self) # zoek de node, , hoe bepaal je nu ix?
        if self == self.widget.root:
            # zichtbaar maken
            self.insert_children(
                self.widget.add_list(name=cut_name,
                                     id=cut_id,
                                     flag=cut_expandable_flag,
                                     expanded_icon=cut_expanded_icon,
                                     collapsed_icon=cut_collapsed_icon))
            # in de html tree verwerken
            if cut_el is not None:
                insert_start(h,cut_el)
        elif before:
            # zichtbaar maken
            self.insert_before(
                self.widget.add_list(name=cut_name,
                                     id=cut_id,
                                     flag=cut_expandable_flag,
                                     expanded_icon=cut_expanded_icon,
                                     collapsed_icon=cut_collapsed_icon))
            # in de html tree verwerken
            print "toevoegen op pos",ix-1
            if cut_el is not None:
                insert_pos(h,cut_el,ix - 1)
        else:
            # zichtbaar maken
            self.insert_after(
                self.widget.add_list(name=cut_name,
                                     id=cut_id,
                                     flag=cut_expandable_flag,
                                     expanded_icon=cut_expanded_icon,
                                     collapsed_icon=cut_collapsed_icon))
            # in de html tree verwerken
            print "toevoegen op pos",ix
            if cut_el is not None:
                insert_pos(h,cut_el,ix)
        cut_el = None
        cut_obj = None
        self.widget.frm.prnt.setmodified(True)

    def ins_bef(self):
        self.widget.e12 = (None,None)
        d = ElementDialog(self.widget)
        if d.result is not None:
            # zichtbaar maken
            new_id = bepaal_new_id(self,d.result)
            ## print "new id:",new_id
            n=self.widget.add_list(name=d.result[0],
                                         id=new_id,
                                         flag=0,
                                         expanded_icon=self.expanded_icon,
                                         collapsed_icon=self.collapsed_icon)
            self.insert_before(n) # ,d.result)
            # in de html tree verwerken
            h,ix = bepaal_xmlnode(self) # zoek de parent node
            new = bs.Tag(self.widget.data,d.result[0])
            for x,y in d.result[1]:
                new[x] = y
            insert_pos(h.parent,new,ix)
            self.widget.frm.prnt.setmodified(True)

    def ins_aft(self):
        self.widget.e12 = (None,None)
        d = ElementDialog(self.widget)
        if d.result is not None:
            # zichtbaar maken
            new_id = bepaal_new_id(self,d.result)
            print "new id:",new_id
            n=self.widget.add_list(name=d.result[0],
                                         id=new_id,
                                         flag=0,
                                         expanded_icon=self.expanded_icon,
                                         collapsed_icon=self.collapsed_icon)
            self.insert_after(n) # ,d.result)
            # in de html tree verwerken
            h,ix = bepaal_xmlnode(self) # zoek de parent node
            new = bs.Tag(self.widget.data,d.result[0])
            for x,y in d.result[1]:
                new[x] = y
            insert_pos(h.parent,new,ix-1)
            self.widget.frm.prnt.setmodified(True)

    def ins_chld(self):
        self.widget.e12 = (None,None)
        d = ElementDialog(self.widget)
        if d.result is not None:
            # zichtbaar maken
            new_id = bepaal_new_id(self,d.result)
            n=self.widget.add_list(name=d.result[0],
                                         id=new_id,
                                         flag=0,
                                         expanded_icon=self.expanded_icon,
                                         collapsed_icon=self.collapsed_icon)
            if not self.expandable():
                self.expandable_flag = True
            self.insert_children(n) # ,d.result,elem=True)
            # in de html tree verwerken
            h,ix = bepaal_xmlnode(self) # zoek de node,
            new = bs.Tag(self.widget.data,d.result[0])
            for x,y in d.result[1]:
                new[x] = y
            insert_end(h,new)
            self.widget.frm.prnt.setmodified(True)

    def ins_text(self):
        self.widget.e12 = None
        d = TextDialog(self.widget)
        if d.result is not None:
            # zichtbaar maken
            new_id = bepaal_new_id(self,d.result)
            n=self.widget.add_list(name=d.result,
                                         id=new_id,
                                         flag=0,
                                         ## expanded_icon=self.expanded_icon,
                                         ## collapsed_icon=self.collapsed_icon
                                         )
            if not self.expandable():
                self.expandable_flag = True
            self.insert_children(n) # ,d.result,elem=True)
            # in de html tree verwerken
            h,ix = bepaal_xmlnode(self) # zoek de node,
            insert_end(h,d.result)
            self.widget.frm.prnt.setmodified(True)

class XMLTree:
    def __init__(self, master, name, data):
        h0 = 202
        w0 = 218
        if DESKTOP:
            h0 = 600
            w0 = 500
        self.master = master
        frm = Frame(master,borderwidth=5,relief=RIDGE)
        frm.pack(fill=BOTH,expand=True)
        sby=Scrollbar(frm,orient=VERTICAL)
        sby.pack(side=RIGHT,fill=Y)
        sbx=Scrollbar(frm, orient=HORIZONTAL)
        sbx.pack(side=BOTTOM,fill=X)
        self.tree=Tree.Tree(frm,
                            height=h0,
                            width=w0,
                            background="white",
                            highlightthickness=0,
                            root_id="root",
                            root_label=data.name,
                            node_class=MyNodes,
                            ## drop_callback=dnd_update,
                            get_contents_callback=self.getelems)
        self.tree.frm = frm
        self.tree.frm.prnt = self
        self.tree.data = data
        ## print self.tree.data
        self.tree.pack(expand=True,fill=BOTH)
        self.tree.name = name
        self.tree.configure(yscrollcommand=sby.set)
        sby.configure(command=self.tree.yview)
        self.tree.configure(xscrollcommand=sbx.set)
        sbx.configure(command=self.tree.xview)
        self.tree.root.expand()
        self.frm = frm

    def getelems(self,node):   # expandeer element
        hier,ix = bepaal_xmlnode(node)
        x = hier.name # kan, is altijd expandable, dus altijd een tag
        self.master.parent.currentitem = ("element",hier.name, hier.text)
        for x,y in enumerate([h for h in hier.contents if h != '\n']):
            if isinstance(y,bs.Tag): ## if type(y) is types.InstanceType:
                naam = y.name
                idee = getidee(y)
                for n,v in y.attrs:
                    if n in ("name","id"):
                        naam = '%s %s="%s"' % (naam,n,v)
                if len([h for h in y.contents if h != '\n']) > 0: # or len([h for h in y.attrs if h[0] not in ("name","id")]) > 0:
                    v = 1
                else:
                    v = 0
                node.widget.add_node(name=naam,id=idee,flag=v,
                    collapsed_icon=node.widget.collapsed_icon)
            elif isinstance(y,bs.Declaration):
                idee = "dtd"
                naam = getshortname(y.strip())
                node.widget.add_node(name=naam,id=idee,flag=0)
            else:
                idee = getidee(y)
                naam = getshortname(y.strip())
                node.widget.add_node(name=naam,id=idee,flag=0)

    def setmodified(self,value):
        self.ismodified = value
        if value:
            self.master.parent.filemenu.entryconfig(self.master.parent.miSave,state=ACTIVE)
        else:
            self.master.parent.filemenu.entryconfig(self.master.parent.miSave,state=DISABLED)

class MainFrame:
    def __init__(self,fn=''):
        master = Tk()
        self.master = master
        # self.xmlfn = fn - wordt later ingesteld
        frm = Frame(master) # , width=224, height=208, bd=1
        frm.parent = self
        frm.pack(expand=True,fill=BOTH)
        self.frm = frm
        mb = Frame(frm)
        mb.pack(fill=X)

        # Create File menu
        fb = Menubutton(mb, text = 'File', padx=3, pady=2)
        fb.pack(side = LEFT)
        self.filemenu = Menu(fb, tearoff=0)
        fb['menu'] = self.filemenu
        # Populate File menu
        self.filemenu.add('command', label = 'New', command = self.newxml)
        self.filemenu.add('command', label = 'Open', command = self.openxml)
        # deze optie uitgrijzen als er geen file geladen of opgebouwd  is of het is niet gewijzigd:
        self.miSave = 2
        self.filemenu.add('command', label = 'Save', command = self.savexml)
        self.filemenu.entryconfig(self.miSave,state=DISABLED)
        # deze optie uitgrijzen als er geen file geladen of opgebouwd is
        self.miSaveAs = 3
        self.filemenu.add('command', label = 'Save As', command = self.savexmlas)
        self.filemenu.entryconfig(self.miSaveAs,state=DISABLED)
        # deze optie actief maken als er een dtd gemaakt of gewijzigd is
        ## self.miSaveDTD = 4
        ## self.filemenu.add('command', label = 'Save DTD', command = self.stub)
        ## self.filemenu.entryconfig(self.miSaveDTD,state=DISABLED)
        self.filemenu.add('command', label = 'Exit', command = self.quit)

        # Create  help menu
        hb = Menubutton(mb, text = 'Help',padx=2,pady=2)
        hb.pack(side = RIGHT)
        hm = Menu(hb, tearoff=0)
        hb['menu'] = hm
        # Populate help menu
        hm.add('command', label = 'About', command = self.stub)

        if fn == '':
            self.newxml()
            self.openxml()
        else:
            self.rt = bs.BeautifulSoup(''.join([x for x in file(self.xmlfn)]))
            self.xt = XMLTree(frm, self.xmlfn, self.rt)
            self.init_tree()
        master.title(TITEL)
        master.mainloop()

    def quit(self):
        self.master.destroy()

    def stub(self):
        pass

    def newxml(self):
        self.rt = bs.BeautifulSoup('<html></html>') # is altijd html
        if "xt" not in self.__dict__:
            self.xt = XMLTree(self.frm, '[untitled]', self.rt)
        self.xmlfn = ""
        self.init_tree()

    def openxml(self):
        h = tkFileDialog.askopenfilename(filetypes=[("HTML files","*.html")],
            initialdir=os.path.split(self.xmlfn)[0])
        if h != '':
            ## print h
            oldrt = self.rt
            try:
                self.rt = bs.BeautifulSoup(''.join([x for x in file(h)]))
            except:
                self.rt = oldrt
                h = tkMessageBox.showwarning('eh...','parsing ging fout')
            else:
                self.xmlfn = h
                ## self.xt = XMLTree(self.frm, self.xmlfn, self.rt)
                self.init_tree()

    def init_tree(self):
        """initialiseer scherm voor XMLTree instantie (self.xt)"""
        self.xt.tree.root.collapse()
        self.xt.tree.data = self.rt
        self.xt.tree.root.set_label(self.rt.name)
        self.xt.name = "(untitled)"
        self.xt.tree.root.expand()
        self.filemenu.entryconfig(self.miSaveAs,state=ACTIVE)
        self.master.title(" - ".join((TITEL,self.xt.name)))

    def savexml(self):
        shutil.copyfile(self.xmlfn,self.xmlfn + '.bak')
        f = open(self.xmlfn,'w')
        f.write(self.rt.renderContents())
        f.close()

    def savexmlas(self):
        h = tkFileDialog.asksaveasfilename(filetypes=[("HtML files","*.html")],
            initialdir=os.path.split(self.xmlfn),
            defaultextension=".html")
        if h:
            self.xmlfn = h
            self.savexml()

def main(inv):
    fn = ''
    if len(inv) > 1:
        fn = inv[1]
    h = MainFrame(fn)

if __name__ == "__main__":
    #print sys.argv
    main(sys.argv)