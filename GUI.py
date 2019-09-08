import tkinter as tk
from tkinter import *
import datetime
from JSON import JsonHandler
from functools import partial
from tkinter.messagebox import showinfo



class DeleteAllForm(tk.Frame):
    
    def __init__(self, root, **kwargs):
        self.root = root
        tk.Frame.__init__(self, self.root, **kwargs)
        delete_All_window = tk.Toplevel(self.root)
        delete_All_window.title("Delete date box")
        delete_All_window.geometry("250x110")
        Label(delete_All_window, text="Enter intended date for delete : ").grid(row=0, column=0)
        date_field = Entry(delete_All_window, bg='light gray', width=10, bd=2, selectborderwidth=5)
        date_field.grid(row=0, column=1)
        account_delete_all_action_with_arg = partial(self.delete_all_task_in_date,date_field)
        Button(delete_All_window, text='Delete date',bd=4 ,width=20 ,activebackground='lightgrey' , command=account_delete_all_action_with_arg).place(x=10,y=75)

    def delete_all_task_in_date(self,date_field):
        date_field=str(date_field.get())
        if JsonHandler.search_date(self,date_field):
            intended_data=JsonHandler.search_date(self,date_field)
            JsonHandler.delete_all(self,intended_data)


def create_delete_all_window(args, root=None):
    main_gui = DeleteAllForm(root)
    
class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.json_obj=JsonHandler()
        self.root.geometry('500x320')
        self.root.title('To Do List')
        self.day_date=datetime.date.today()
        scrollbar = Scrollbar(self.root,orient=VERTICAL)
        list_box=Listbox(self.root, height=12 ,yscrollcommand=scrollbar.set , width=45, selectmode=MULTIPLE)
        scrollbar.config(command=list_box.yview)
        scrollbar.pack(side= RIGHT, fill=Y)
        list_box.place(x=200,y=140)
        text_entry=Entry(self.root, bg='white', width=45, bd=2, selectborderwidth=5)
        text_entry.place(x=200,y=110)

        date_entry=Entry(self.root, bg='white', width=15, bd=2, selectborderwidth=5)
        date_entry.place(x=380,y=80)

        lable_for_date_Entry=Label(self.root,text="date")
        lable_for_date_Entry.place(x=350,y=80)

        list_option_field=Label(self.root, text="To Do List",font='Helvetica 18 bold')
        list_option_field.place(x=33,y=10)

        create_delete_all_window_with_args=partial(create_delete_all_window,self.root)
        delete_all_button=Button(self.root,text='Delete Date' ,command=create_delete_all_window_with_args ,bd=4 ,width=20 ,activebackground='lightgrey' ,font='Bnazanin 10 bold')
        delete_all_button.place(x=10,y=140)

        tkvar = StringVar(self.root)
        tkvar.set('choose date')

        create_delete_with_args=partial(self.delete_task,list_box,tkvar)
        delete_button=Button(self.root,text='Delete Task' ,command=create_delete_with_args,width=20 ,bd=4 ,activebackground='lightgrey' ,font='Bnazanin 10 bold')
        delete_button.place(x=10,y=105)

        option=['']
        popupMenu = OptionMenu(self.root, tkvar, *option)
        popupMenu.place(x=200,y=80)
        tkvar.trace('w',partial(self.option_select,tkvar,list_box,popupMenu,delete_all_button,delete_button))
        self.option_select(tkvar,list_box,popupMenu,delete_all_button,delete_button)
    
        create_file_with_arg = partial(self.add_task,text_entry,date_entry,list_box,popupMenu,tkvar,delete_all_button,delete_button)
        add_task_button=Button(self.root,text='Add task' ,command=create_file_with_arg , width=20,bd=4,activebackground='lightgrey' ,font='Bnazanin 10 bold')
        add_task_button.place(x=10,y=70)

        clean_all_item_to_menu=partial(self.clean,list_box,delete_all_button,delete_button)
        clean_list_box=Button(self.root,text='Clean',command=clean_all_item_to_menu ,bd=4 ,width=20 ,activebackground='lightgrey' ,font='Bnazanin 10 bold')
        clean_list_box.place(x=10,y=245)

        create_sort=partial(self.show_sort_day,list_box)
        sort_button_from_A_Z=Button(self.root,text='Sort Button From A-Z' ,command=create_sort,bd=4 ,width=20 ,activebackground='lightgrey' ,font='Bnazanin 10 bold')
        sort_button_from_A_Z.place(x=10,y=175)

        creat_show_all_date_with_task=partial(self.show_all,delete_all_button,delete_button,list_box)
        sort_button_from_Z_A=Button(self.root,text='Show All' ,command=creat_show_all_date_with_task ,bd=4 ,width=20 ,activebackground='lightgrey' ,font='Bnazanin 10 bold')
        sort_button_from_Z_A.place(x=10,y=210)

        exit_button=Button(self.root,text='EXIT',bd=4 ,width=20 ,command=self.root.destroy ,activebackground='lightgrey' ,font='Bnazanin 10 bold')
        exit_button.place(x=10,y=280)

        print_date_word=Label(self.root,text='date')

        show_date=Label(self.root,text=self.day_date)
        show_date.place(x=410,y=5)

    def option_select(self,tkvar,list_box,popupMenu,delete_all_button,delete_button,*args):
        list_box.delete('0', 'end')
        delete_button["state"] = "active"
        delete_all_button["state"] = "active"
        date_assagn=tkvar.get()
        options=self.json_obj.date_menu()
        menu = popupMenu["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string,command=lambda value=string: tkvar.set(value))

        task=self.json_obj.compare_select_list(date_assagn)
        if(isinstance(task, list)):
            for i in task:
                list_box.insert(END,i)

    def delete_task(self,list_box,tkvar):
        selection=list_box.curselection()
        date_assagn=tkvar.get()
        if selection:
            for index in selection:
                task_current=list_box.get(index)
                list_box.delete(ACTIVE)
                list_of_values=self.json_obj.search_values(date_assagn)
                self.json_obj.delete( task_current,list_of_values,date_assagn)

    def add_task(self,text_entry,date_entry,list_box,popupMenu,tkvar,delete_all_button,delete_button):
        if text_entry.get()=="" or date_entry.get()=='':
            showinfo("notification box", "You did not enter a date and a task")
        else:
            text_entry=[text_entry.get()]
            date_entry=str(date_entry.get())
            self.json_obj.add(text_entry,date_entry)
            self.option_select(tkvar,list_box,popupMenu,delete_all_button,delete_button)
            list_box.insert(END, *text_entry)
        
    def clean(self,list_box,delete_all_button,delete_button):
        list_box.delete('0', 'end')
        delete_button["state"] = "active"
        delete_all_button["state"] = "active"
        
    def show_sort_day(self,list_box):
        list_box.delete('0', 'end')
        if self.json_obj.show_sort_day_task():
            date_be_sort=self.json_obj.show_sort_day_task()
            for i in date_be_sort:
                list_box.insert(END, i)
                for elem in date_be_sort[i]:
                    list_box.insert(END, elem)
        else:
            showinfo("notification box", "There are no tasks on the day in select")

    def show_all(self,delete_all_button,delete_button,list_box):
        delete_button["state"] = "disable"
        delete_all_button["state"] = "disable"
        list_box.delete('0', 'end')
        if self.json_obj.show_all_task():
            all_list=self.json_obj.show_all_task()
            for key, value in all_list.items() :
                list_box.insert(END,key)
                for i in value:
                    list_box.insert(END,i)
        else:
            showinfo("notification box", "There are no tasks on the day in select")    


    
main=MainGUI()
main.root.mainloop()
  