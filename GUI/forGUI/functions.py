def listbox_selected(self, *args):
    try:
        print(self.lb_utterances.curselection())
    except:
        print('None member')

def length_changed(self, *args):
    g = self.length.get()
    print(g)

