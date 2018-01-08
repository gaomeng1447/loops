#Python 2.6
#CRDC EDVT team
#Update on Dec 28 2017 by gaomwang
#version 1.2
'''
The needed variables in configure file:
Std_Gui_Enable=0
Std_Corner_Run=1-4,2,4-1
Std_Loop_Numb=5
Std_Gui_File=/home/gaom/git/client/lib/formal_ios_RuShelf_rev1.GUI
Std_Gui_Case=1
'''

import pygtk
pygtk.require("2.0")
import gtk, gobject

import sys
import string
import time, datetime

from Anlyze_GUI import readGUI
from Anlyze_GUI import seqGUI
from Anlyze_GUI import readConfig
from Anlyze_GUI import getConfig
from Anlyze_GUI import total_corners
from Anlyze_GUI import transformer
import Print as pt

print sys.argv
filename =  sys.argv[1]
dic = readConfig(filename)
guifile = dic['Std_Gui_File']
###
guifile = transformer(guifile, dic['Std_Corner_Run'], dic['Std_Gui_Case'])
###
DIC_GUI_PY = readGUI(guifile)
DIC_Seq = seqGUI(DIC_GUI_PY)

Corner = DIC_GUI_PY['GUI']
LoopsinCorner = dic['Std_Loop_Numb']
Len = len(Corner)
PY = DIC_GUI_PY['PY']
Cname = DIC_GUI_PY['CNAME']#reserved for corner sequence
#Corner = [['corner1', 'case1', 'case2', 'case3'], ['corner2'],
#         ['corner3', 'case1'], ['corner4', 'case1', 'case2', 'case3']]
#gtask = Corner
Ntr = dic['Std_Corner_Run']
#print Ntr
#config_dic = getConfig(filename)
loops_config = dic['Std_Loop_Numb']


class GUI_Controller:
    """ The GUI class is the controller for our application """

    def __init__(self):
        # setup the main window
        ####
        self.root = gtk.Dialog()
        #self.root = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
        self.oops_L2 = 1
        self.root.set_title("EDVT Tools")
        self.root.set_border_width(3)
        self.root.set_default_size(400, 400)
        self.root.connect("destroy", self.destroy_cb)
        ####
        scrolled_window = gtk.ScrolledWindow()
        self.root.vbox.pack_start(scrolled_window, True, True, 0)
        scrolled_window.show()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_size_request(400, 400)
        # Get the model and attach it to the view
        self.StoreGC = InfoModel()
        self.DisplayGC = DisplayModel()
        self.mdl = self.StoreGC.get_model()

        self.view = self.DisplayGC.make_view(self.mdl)
        # Add our view into the main window
        scrolled_window.add_with_viewport(self.view)
        table = gtk.Table(1, 2, True)

        self.button1 = gtk.ToggleButton("Select All")
        self.button1.connect("toggled", self.select, "toggle button 1")
        self.button2 = gtk.ToggleButton("Run")
        self.button2.connect("toggled", self.callback, "toggle button 2")
        self.root.vbox.pack_start(table)
        table.attach(self.button1, 0, 1, 0, 1)
        table.attach(self.button2, 1, 2, 0, 1)
        self.root.show_all()
        self.root.show()
        return

    def runAcase(self, module_name, cornerName, loopName, dic=getConfig(filename)):
        while gtk.events_pending():
            gtk.main_iteration_do(False)
        str2exec = 'from ' + module_name + ' import test'
        exec(str2exec)
        dic['CornerName'] = cornerName
        dic['LoopName'] = loopName
        #print dic
        test(dic)

    def RUN(self, List_G):
        for id in range(0, Len):
            gth = len(List_G[id])#how many caseList
            oops_L1 = int(List_G[id][0][2])#at this corner, loops for caseList
            module_name = PY[id][0].split('.')[0]
            for LP2 in range(0, self.oops_L2):#repeat time is LP2 from default
                if List_G[id][0][1] == True:
                    Time = datetime.datetime.now()
                    CornerX = Cname[id]
                    Lth = oops_L1
                    print "module names is: %s" % (module_name)
                    self.runAcase(module_name, id+1, loopName=1)

            for LP1 in range(0, oops_L1):#repeat time is LP1 from spinbox
                Time = datetime.datetime.now()
                Lpth = LP1+1
                Cnth = Cname[id]
                pt.LoopBegin(Time, Lpth, Cnth)
                for dex in range(1, gth):
                    module_name = PY[id][dex].split('.')[0]
                    if List_G[id][dex][1] == True:
                        print "module names is: %s" % (module_name)
                        print "executing item name: %s"\
                              %(Corner[id][dex])
                        subcaseLoop = int(List_G[id][dex][2])
                        for subid in range(0, subcaseLoop):
                            print "subid is %d"%(subid)
                            self.runAcase(module_name, id+1, loopName=LP1+1)
                Lpth = LP1+1
                pt.LoopEnd(Lpth, Cnth)

    def callback(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        List_G = self.StoreGC.get_ts_value()

        target = widget.get_active()
        if target:
            self.button2.set_label('Stop')
            self.DisplayGC.renderer1.set_property('activatable', False)
            self.DisplayGC.renderer2.set_property('editable', False)
            self.RUN(List_G)
        else:
            self.button2.set_label('Run')
            self.DisplayGC.renderer1.set_property('activatable', True)
            self.DisplayGC.renderer2.set_property('editable', True)
        return

    def select(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        print 'below is the select result: '
        target = widget.get_active()
        if target:
            self.button1.set_label('Unselect All')
            self.SL(True)
        else:
            self.button1.set_label('Select All')
            self.SL(False)
        return

    def SL(self, tf):
        treeiter = self.mdl.get_iter_first()
        n_columns = self.mdl.get_n_columns()
        print n_columns
        while treeiter:
            values = self.mdl.set_value(treeiter, 1, tf)
            diter = self.mdl.iter_children(treeiter)
            while diter:
                dvalue = self.mdl.set_value(diter, 1, tf)
                diter = self.mdl.iter_next(diter)
            treeiter = self.mdl.iter_next(treeiter)
        return

    def destroy_cb(self, *kw):
        """ Destroy callback to shutdown the app """
        gtk.main_quit()
        return

    def run(self):
        """ run is called to set off the GTK mainloop """
        gtk.main()
        return


class InfoModel:
    """ The model class holds the information we want to display """

    def __init__(self):
        """ Sets up and populates our gtk.TreeStore """
        self.tree_store = gtk.TreeStore(gobject.TYPE_STRING,
                                        gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        # places the global people data into the list
        # we form a simple tree.
        #for item in tasks.keys():
        #    parent = self.tree_store.append(None, (item, True, '10'))
        #    self.tree_store.append(parent, (tasks[item], True, '1'))
        gLen = len(Corner)
        for item in range(0, gLen):
            parent = self.tree_store.append(None, (Corner[item][0], False, LoopsinCorner))
            cLen = len(Corner[item])
            if cLen > 1:
                for citem in range(1, cLen):
                    daught = self.tree_store.append(parent, (Corner[item][citem], False, '1'))
        return

    def get_ts_value(self):
        treeiter = self.tree_store.get_iter_first()
        n_columns = self.tree_store.get_n_columns()
        #print n_columns
        rtList = []
        while treeiter:
            arow = []
            values = self.tree_store.get(treeiter, *range(3))
            arow.append(list(values))

            diter = self.tree_store.iter_children(treeiter)

            while diter:
                dvalue = self.tree_store.get(diter, *range(n_columns))
                diter = self.tree_store.iter_next(diter)
                arow.append(list(dvalue))
            rtList.append(arow)
            treeiter = self.tree_store.iter_next(treeiter)
        return rtList

    def get_model(self):
        """ Returns the model """
        if self.tree_store:
            return self.tree_store
        else:
            return None


class DisplayModel:
    """ Displays the Info_Model model in a view """

    def make_view(self, model):
        """ Form a view for the Tree Model """
        self.view = gtk.TreeView(model)
        # setup the text cell renderer and allows these
        # cells to be edited.
        self.renderer = gtk.CellRendererText()
        self.renderer.set_property('editable', True)
        self.renderer.connect('edited', self.col0_edited_cb, model)
        # The toggle cellrenderer is setup and we allow it to be
        # changed (toggled) by the user.
        self.renderer1 = gtk.CellRendererToggle()
        self.renderer1.set_property('activatable', True)
        self.renderer1.set_property('radio', False)
        #self.renderer1.set_active(True)
        self.renderer1.connect('toggled', self.col1_toggled_cb, model)


        self.renderer2 = gtk.CellRendererText()
        self.renderer2.set_property('editable', True)
        self.renderer2.connect('edited', self.col2_edited_cb, model)
        # Connect column0 of the display with column 0 in our list model
        # The renderer will then display whatever is in column 0 of
        # our model .
        self.column0 = gtk.TreeViewColumn("Case Name  ", self.renderer, text=0)
        self.column0.set_resizable(True)
        # The columns active state is attached to the second column
        # in the model.  So when the model says True then the button
        # will show as active e.g on.
        self.column1 = gtk.TreeViewColumn("   Select   ", self.renderer1)
        self.column1.add_attribute(self.renderer1, "active", 1)
        self.column1.set_resizable(True)

        self.column2 = gtk.TreeViewColumn("Run_cycles   ", self.renderer2, text=2)
        self.column2.set_resizable(True)
        self.view.append_column(self.column0)
        self.view.append_column(self.column1)
        self.view.append_column(self.column2)
        return self.view

    def col0_edited_cb(self, cell, path, new_text, model):
        """
        Called when a text cell is edited.  It puts the new text
        in the model so that it is displayed properly.
        """
        print "Change colum 1 '%s' to '%s'" % (model[path][0], new_text)
        model[path][0] = new_text
        return

    def col1_toggled_cb(self, cell, path, model):
        """
        Sets the toggled state on the toggle button to true or false.
        """
        model[path][1] = not model[path][1]
        print "Toggle colum 2 '%s' to: %s" % (model[path][0], model[path][1],)
        return

    def col2_edited_cb(self, cell, path, new_text, model):
        """
        Called when a text cell
         is edited.  It puts the new text
        in the model so that it is displayed properly.
        """
        print "Change colum 3 '%s' to '%s'" % (model[path][2], new_text)
        model[path][2] = new_text
        return

class FromConfToGui:
    """ DisplSays the Info_Model model in a view """
    def __init__( self ):
        InfoModel()
        DisplayModel()

    def runGui(self):
        self.myGUI = GUI_Controller()
        self.myGUI.run()

    def runAcase(self, module_name, cornerName, loopName, dic=getConfig(filename)):
        md = module_name.split('.')[0]
        str2exec = 'from ' + md + ' import test'
        exec (str2exec)
        dic['CornerName'] = int(cornerName.split('Corner')[1])
        dic['LoopName'] = loopName
        test(dic)

    def runAcorner(self, cornerPY, cornerName):
        cLen = len(cornerPY)
        lcycle = int(dic['Std_Loop_Numb'])
        print cornerPY
        self.runAcase(cornerPY[0], cornerName, loopName=1)

        if cLen > 1:
            for id in range(0, lcycle):
                Time = datetime.datetime.now()
                Lpth = id + 1
                Cnth = cornerName
                pt.LoopBegin(Time, Lpth, Cnth)
                for idx in range(1, cLen):
                    self.runAcase(cornerPY[idx], Cnth, loopName=Lpth)
                pt.LoopEnd(Lpth, Cnth)

    def runCli(self):
        ctrList = total_corners(Ntr)
        print ctrList
        moduleList = DIC_Seq['PY']
        for cnr in ctrList:
            c_name = 'Corner' + str(cnr)
            moduleName = moduleList[cnr - 1]
            self.runAcorner(moduleName, c_name)
        return

    def runX(self):
        if dic['Std_Gui_Enable'] == '1':
            self.runGui()
        elif dic['Std_Gui_Enable'] == '0':
            self.runCli()
        else:
            print 'unknow status'



if __name__ == '__main__':
    myGUI = FromConfToGui()
    myGUI.runX()
