from tkinter import filedialog, ttk
from tkinter import *
import os  # extract file path
import shutil  # copy data file
from PIL import Image, ImageTk

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Good luck")
        master.configure(background='white')

        self.load = Image.open('CBGRs.jpg')
        self.render = ImageTk.PhotoImage(self.load)

        # image = PhotoImage(file="CBGR.jpg")
        self.CBG_logo = Label(image=self.render, background='white')
        self.CBG_logo.image = self.render
        # self.CBG_logo.place(x=0,y=0)
        self.CBG_logo.grid(row=1, column=1, rowspan=4, sticky=N+S+E+W)

        # labels setting
        self.label = Label(master, text="Lazy copy app for BGI files")
        self.label.config(font=("Helvetica", 24), background='white')
        self.label.grid(row=0, column=1,columnspan=4)

        self.labelauthor = Label(master, text="This program will automatically copy files without FASTQ files. Please contact Ray if you have any questions", background='white')
        self.labelauthor.grid(row=7, column=1,columnspan=4,sticky=W)

        self.folder_path_source = StringVar()
        self.folder_path_destination = StringVar()

        self.lbl1 = Label(master=master, text="", background='white')
        self.lbl1.grid(row=1, column=3)

        self.lbl2 = Label(master=master, text="", background='white')
        self.lbl2.grid(row=2, column=3)

        self.lbl3 = Label(master=master, text="", background='white')
        self.lbl3.grid(row=4, column=3)
        # button setting

        self.source_button = Button(master, text="Select Resource", command=self.browse_path_source,width=20)
        self.source_button.grid(row=1, column=2)

        self.dest_button = Button(master, text="Select Destination", command=self.browse_path_destination,width=20)
        self.dest_button.grid(row=2, column=2)

        self.copyfile_button = Button(text="Copy files", command=self.copy_files, width=20)
        self.copyfile_button.grid(row=3, column=2)

        self.close_button = Button(master, text="Exit", command=master.quit,width=20)
        self.close_button.grid(row=4, column=2)

        # progressbar
        self.pb = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
        self.pb.grid(row=3, column=3)


    def browse_path_source(self):
        print("Initializing Dialogue...\nPlease select a directory.")
        dirname = filedialog.askdirectory(initialdir=os.getcwd(), title='Please select a directory')
        if len(dirname) > 0:
            print("You chose %s" % dirname)
            self.folder_path_source.set(dirname)
            self.lbl1.configure(text=dirname)
            return dirname
        else:
            dirname = os.getcwd()
            print("\nNo directory selected - initializing with %s \n" % os.getcwd())
            return dirname

    def browse_path_destination(self):
        print("Initializing Dialogue...\nPlease select a directory.")
        dirname = filedialog.askdirectory(initialdir=os.getcwd(), title='Please select a directory')
        if len(dirname) > 0:
            print("You chose %s" % dirname)
            self.folder_path_destination.set(dirname)
            self.lbl2.configure(text=dirname)
            return dirname
        else:
            dirname = os.getcwd()
            print("\nNo directory selected - initializing with %s \n" % os.getcwd())
            return dirname

    # def get_size(self):
    #     total_size = 0
    #     folder_path_source1 = self.folder_path_source.get()
    #     for dirpath, dirnames, filenames in os.walk(folder_path_source1):
    #         for f in filenames:
    #             fp = os.path.join(dirpath, f)
    #             total_size += os.path.getsize(fp)
    #     return total_size

    def copy_files(self):
        # root_src_dir = filename1
        # root_target_dir = filename2
        # print('Your source dir is %s'%root_src_dir)
        # print('Your des dir is %s'%root_target_dir)
        print('Here we go!!')
        print('Do not close this window plz!')
        folder_path_source1 = self.folder_path_source.get()
        folder_path_destination1 = self.folder_path_destination.get()
        # Count total number of files
        cpt = sum([len(files) for r, d, files in os.walk(folder_path_source1)])
        print(" total number of file:%s" % cpt)
        step = (100000 / cpt)
        # step = 120
        operation = 'copy'  # 'copy' or 'move'
        # transfer files
        for src_dir, dirs, files in os.walk(folder_path_source1):
            dst_dir = src_dir.replace(folder_path_source1, folder_path_destination1)
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            dst_free = shutil.disk_usage(dst_dir).free
            size = sum(os.path.getsize(os.path.join(src_dir, n)) for n in files)
            if size > dst_free:
                # print("Yes Ray")
                print("Do not have enough space, please find a new hard drive and copy from the folder:", src_dir)
                self.lbl3.configure(text="Do not have enough space!!",fg='red')
                exit
            else:
                for file_ in files:
                    # print("this is step: %s" % step)
                    # print(cpt)
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    if operation is 'copy':
                        if not dst_file.endswith('.fq.gz'):
                            shutil.copy(src_file, dst_dir)
                            # Show the file name
                            print(file_)
                    elif operation is 'move':
                        shutil.move(src_file, dst_dir)
                    # Update progress bar
                    self.pb.step(step)
                    self.pb.update()

        if size < dst_free:
            self.lbl3.configure(text="Mission completed!!")
            print("Congratulation!! Mission completed!")
        # root.destroy()

root = Tk()
# Tk().withdraw()
my_gui = MyFirstGUI(root)
root.mainloop()
