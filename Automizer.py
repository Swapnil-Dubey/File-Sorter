import os.path
from plyer import notification
import tkinter as tk
import shutil
import re
from tkinter.filedialog import askdirectory

errorlabel = ''
usage = ''
window = tk.Tk()
window.title("Automizer")
paths = []
count = 0
files = []
conf = ''
exts = []
movecount= 0
def confirm():
    global errorlabel, usage, count, paths, files
    paths = []
    exts = []
    count+=1
    src = entry.get()
    if src[-1] == "/":
        src = src.rstrip("/")
        if os.path.exists(src):
            if os.path.isdir(src):
                if re.search(r"^/+", src):
                    if usage != '':
                        usage.after(1, usage.destroy)
                    paths.append(src.strip())
                    if len(paths) != 0:
                        codename = paths[0]
                        notification.notify(title="Automizer",message="For confirmation please select the folder from the dialogue box too.", timeout=3)
                        conf = askdirectory(title='Select Folder')
                        if codename == conf:
                            for dir in os.listdir(conf):
                                if dir != ".DS_Store":
                                    files.append(dir)
                            for file in files:
                                exten = re.search(r"(\.\w+$|\.\w+$)", file, re.IGNORECASE)
                                if exten:
                                    ext = exten.group().lower()
                                    exts.append(ext.strip().lower())
                            sorting(os.listdir(conf), exts, src)
                        else:
                            notequalerror = tk.Label(window,text="Due to safety purposes, select the folder which has the same path as entered before.")
                            notequalerror.pack()
                            notequalerror.after(4000, notequalerror.destroy)
                    else:
                        if errorlabel == '':
                            errorlabel = tk.Label(window, text="Please enter the mac os folder path correctly.",
                                                  fg="red", bg="black")
                            errorlabel.pack()
                            if usage == '':
                                usage = tk.Label(window, text="Example Usage: /Users/user-name/Documents/", fg="green",
                                                 bg="black")
                                usage.pack()
                            errorlabel.after(3000, errorlabel.destroy)
                            errorlabel = ''

                else:
                    if errorlabel == '':
                        errorlabel = tk.Label(window, text="Please enter the mac os folder path correctly.", fg="red",bg="black")
                        errorlabel.pack()
                        if usage == '':
                            usage = tk.Label(window, text="Example Usage: /Users/user-name/Documents/", fg="green",bg="black")
                            usage.pack()
                        errorlabel.after(3000, errorlabel.destroy)
                        errorlabel = ''
            else:
                notDirError = tk.Label(window, text = "The Given pathname does not lead to a folder. Please enter the pathname of a folder correctly.")
                notDirError.pack()
                notDirError.after(3000, notDirError.destroy)
        else:
            notexisterror = tk.Label(window, text="File doesnt exist")
            notexisterror.pack()
            notexisterror.after(3000, notexisterror.destroy)

def sorting(folder, extensions, path):
    global conf, files, movecount
    pictureex = [".jpeg", ".jpg", ".gif", ".png", ".tiff", ".raw"]
    pdfex = ".pdf"
    wordocex = ".docx", ".doc", ".odt", ".rtf", ".tex", ".txt", ".wpd"
    otherdocex = [".psd", ".eps", ".ai", ".indd", ".fnt"]
    programmingfiles= [".py", ".c", ".class", ".js", ".cgi", ".pl", ".cpp", ".cs", ".h" , ".php", ".sh", ".swift", ".vb", ".asp", ".aspx", ".cer", ".css", ".html", ".part", ".php", ".rss", ".xhtml"]
    videoex = [".avi", ".flv", ".h264", ".m4v", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", ".rm", ".swf", ".vob", ".wmv"]
    spreadsheetex = [".ods", ".xls", ".xlsm", ".xlsx"]
    presentationex = [".key", ".odp", ".pps", ".ppt", ".pptx"]
    executableexe = [".apk", ".bin", ".com", ".exe", ".gadget", ".jar", ".msi", ".wsf"]
    dataex = [".csv", ".dat", ".db", ".dbf", ".sql", ".xml"]
    compressedex = [".7z", ".pkg", ".rar", ".tar.gz", ".zip", ".z"]
    audioex = [".aif", ".cda", ".mid", ".midi", ".mp3", ".mpa", ".wav", ".wma", ".wpl"]
    NOsystemex= [".bak", ".cab", ".cfg", ".cpi", ".cur", ".dll", ".dmp", ".drv", ".icns", ".ico", ".ini", ".lnk", ".msi", ".sys", ".tmp"]
    dir_list = os.listdir(paths[0])
    for y in extensions:
        if y in NOsystemex:
            systemstatement = tk.Label(text=f"System File {y} wasn't moved for security reasons", fg = "white", bg = "black")
            systemstatement.pack()
            systemstatement.after(5000, systemstatement.destroy)
        elif y in pictureex:
            moving(pictureex, "Images", dir_list)
        elif y in pdfex:
            moving(pdfex, "PDF Documents", dir_list)
        elif y in wordocex:
            moving(wordocex, "Word Documents", dir_list)
        elif y in otherdocex:
            moving(otherdocex, "Other Documents", dir_list)
        elif y in programmingfiles:
            moving(programmingfiles, "Programming Files", dir_list)
        elif y in videoex:
            moving(videoex, "Videos", dir_list)
        elif y in spreadsheetex:
            moving(spreadsheetex, "Spreadsheets", dir_list)
        elif y in presentationex:
            moving(presentationex, "Presentation Documents", dir_list)
        elif y in executableexe:
            moving(executableexe, "Executables", dir_list)
        elif y in dataex:
            moving(dataex, "Data Files", dir_list)
        elif y in compressedex:
            moving(compressedex, "Compressed Files", dir_list)
        elif y in audioex:
            moving(audioex, "Audio Files", dir_list)
        else:
            filenotsupported = tk.Label(text=f"Either a file in the folder is not supported or there are no files in this folder", fg = "white", bg = "black")
            filenotsupported.pack()
            filenotsupported.after(3000, filenotsupported.destroy)
    if movecount!=0:
        successlabel = tk.Label(text=f"The folder has been sorted successfully", fg = "white", bg = "black")
        successlabel.pack()
        successlabel.after(5000, successlabel.destroy)
        notification.notify(title="Automizer", message="Automated File sorting successfully completed", timeout=3)


def moving(typeext, foldername, dir_list):
    global movecount
    if foldername not in dir_list:
        os.makedirs(f"{paths[0]}/{foldername}")
    for fi in files:
        for extiterator in typeext:
            if fi.lower().endswith(f"{extiterator}"):
                shutil.move(f"{paths[0]}/{fi.lower()}", f"{paths[0]}/{foldername}")
                movecount += 1

window.geometry("800x400")
window.config(bg = "black")
pathstatement = tk.Label(text = "Enter the path of the folder you want sorted, below.", fg = "white", bg = "black")
pathstatement.pack()
entry = tk.Entry(window, fg = "black", bg ="white", width = 50)
entry.pack()
button = tk.Button(window, text="Confirm by selecting the folder", width= 30, command= confirm)
button.place(relx= .5, rely= .5, anchor="center")



# fix the bug of spamming sort button and spammming wrong paths and If statements ke lie else blocks daalo and complete the code.













window.mainloop()

