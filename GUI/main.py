import tkinter as tk
import ClassifyApp

def main():
    # _/_/_/ Systems_Classify
    # main
    root = tk.Tk()
    
    # title
    root.title('Dialogue Acts Classification')
    
    # size
    root.minsize(1000,600)
    
    # App
    ClassifyApp.ClassifyApp(master=root)

    # show
    root.mainloop()

if __name__ == '__main__':
    main()