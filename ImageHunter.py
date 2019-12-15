import sys
import threading
from PIL import ImageTk,Image 
import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import shutil
if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
    from Tkinter import filedialog
    from Tkinter import *
else:
    # Python 3
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import *


root = tk.Tk()

#Download and save each and every image
def DownloadAndSave(url,picNum):
    try:
        fullname = str(picNum)+".jpg"
        r = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open(root.dest + fullname, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                if saveAsTxt.get():
                    insertIntoFile(url)
    except Exception as e:
        print(str(e))
        
#Write url of the downloaded images into text file
def insertIntoFile(url):
    line = url+"\n"
    with open(root.dest+"urlLinks.txt",'a') as f:
        f.write(line)

        
#Scrap and get image details        
def downloadSetup(url):
        
        picNum = 1
        log.insert(tk.END, "Processing ....\nLoading URL.......", "a")
        log.see(tk.END)
        
        raw_html = url
        
        
        print(root.dest)

        # create a new Firefox session
        driver = webdriver.Firefox(executable_path='/Users/elamparithiezhilarasimurugan/Desktop/geckodriver')
        driver.implicitly_wait(30)
        driver.get(raw_html)

        html = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        linkSet = set()

        for p in html.select('img'):
            try:
                if p['src'].startswith("http"):
                    linkSet.add(p['src'])
            except Exception as e:
                print(str(e))

        for link in linkSet:
            try:
                log.insert(tk.END, "\n"+link, "a")
                log.see(tk.END)
                print(link)
                DownloadAndSave(link,picNum)
                picNum += 1
            except Exception as e:
                print(str(e))

        log.insert(tk.END, "\nFinished!\n Total : "+str(picNum) +" Images", "a")
        log.see(tk.END)
        print("Donwloaded successfully")
        
def browse():
    root.dest =  filedialog.askdirectory()+"/"
    print (root.dest)
    pathText.set(root.dest)
    
def scrap():
    url = urlstr.get()
    if not url or not root.dest:
        log.insert(tk.END, "Please, select destination folder and give correct url.", "a")
        log.see(tk.END)
    else:
        x = threading.Thread(target=downloadSetup, args=(url,),daemon=True)
        x.start()
        
    

#UI PART
root.rowconfigure( 0, weight=1)
root.columnconfigure( 0, weight=1)
root.title("Image Scraper")
root.geometry("800x480")
frame=Frame(root)
frame.grid(row=0, column=0,sticky=N+S+E+W)
frame1=Frame(root)
frame1.grid(row=1, column=0, sticky=N+S+E+W)
tk.Label(frame,text="URL").grid(row=0)
urlstr = tk.StringVar()
Grid.columnconfigure(frame, 1, weight=1)
url = tk.Entry(frame,textvariable = urlstr).grid(row=0,column=1, sticky=N+S+E+W)
tk.Label(frame,text="Destination").grid(row=1)
tk.Button(frame, text="Browse",command=browse).grid(row=1,column=2)
pathText = tk.StringVar()
path = tk.Entry(frame,textvariable=pathText).grid(row=1,column=1, sticky=N+S+E+W) 
saveAsTxt = IntVar()
Checkbutton(frame, text="Save downloaded image links in txt file", variable=saveAsTxt).grid(row=3,column=1 )
tk.Button(frame, text="Download",command=scrap).grid(row=4,column=1,pady=10)
logText = tk.StringVar()
Grid.rowconfigure(frame1, 0, weight=1)
Grid.columnconfigure(frame1, 0, weight=1)
log = tk.Text(frame1, background="black", foreground="green")
log.grid(row=0, column=0, sticky=N+E+W+S)
tk.mainloop()
