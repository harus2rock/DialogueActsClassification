import tkinter as tk
import gui_classify

def main():
    # _/_/_/ Systems_Classify
    # main
    root = tk.Tk()
    
    # title
    root.title('Dialogue Acts Classification')
    
    # size
    root.minsize(800,550)
    
    # App
    gui_classify.ClassifyApp(master=root)

    # show
    root.mainloop()

if __name__ == '__main__':
    main()