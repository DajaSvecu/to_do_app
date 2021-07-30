import tkinter as tk
import sqlite3

class ToDoApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        tk.Label(self, text="To Do List", font=('Arial Bold', 20)).pack(fill='both')
        ToDoAppInput(self, self.add_todoitem_to_dtb).pack()

        self.con = sqlite3.connect('./Todoapp.db')
        self.cur = self.con.cursor()
        self.create_todoitems()

    def create_todoitems(self):
        to_do_items = self.cur.execute('SELECT Item FROM ToDoList;')
        for item in to_do_items:
            ToDoAppItem(self, item[0], self.delete_todoitem_from_dtb).pack(fill='both')
    
    def add_todoitem_to_dtb(self, item):
        self.cur.execute('INSERT INTO ToDoList (Item) VALUES ("{}");'.format(item))
        self.con.commit()
        ToDoAppItem(self, item, self.delete_todoitem_from_dtb).pack(fill='both')
       
    def delete_todoitem_from_dtb(self,item):
        self.cur.execute('DELETE FROM ToDoList WHERE Item="{}"'.format(item))
        self.con.commit()

class ToDoAppItem(tk.Frame):
    def __init__(self, parent, text, function, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Label(self, text=text).pack(side='left',padx=5,pady=5)
        tk.Button(self, text='DELETE', command=lambda txt=text, cb=function: self.delete_item(txt, cb)).pack(side='right', padx=5,pady=5)
        
    def delete_item(self, text, callback):
        callback(text)
        self.destroy()
        
class ToDoAppInput(tk.Frame):
    def __init__(self, parent, function, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.input = tk.Entry(self)
        self.input.pack(side='left',padx=10,pady=10)
        tk.Button(self, text='ADD', command=lambda cb=function: self.get_item(cb)).pack(side='left',padx=10,pady=10)
        
    def get_item(self, callback):
        item = self.input.get()
        self.input.delete(0, 'end')
        callback(item.capitalize())

if __name__ == "__main__":
    root = tk.Tk()
    root.title('To Do App')
    ToDoApp(root).pack(expand=True, fill='both', padx=20, pady=20)
    root.mainloop()