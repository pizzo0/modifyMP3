from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3

import tkinter as tk
from tkinter import filedialog

import os

# you can add more keys if you want
KEYS=['TITLE','ARTIST','ALBUM','DATE','GENRE']

SPACE='####################################################################################'

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def modifyMP3(SONGPATH:str)->None:
    Q=input(f'{SPACE}\nDo you want to change its metadata? (y/n):\n')
    NEWTITLE=''
    if Q.lower()=="y":
        NEWTITLE=modifyMetadata(SONGPATH)
    Q=input(f'{SPACE}\nDo you want to change its album art? (y/n):\n')
    if Q.lower()=="y":
        modifyAlbumCover(SONGPATH)
    if NEWTITLE:
        NEWSONGPATH='/'.join(SONGPATH.split('/')[:-1])+f'/{NEWTITLE}.mp3'
        try:
            os.rename(SONGPATH,NEWSONGPATH)
            print(f'{SPACE}\nRenamed file')
        except:
            print(f'{SPACE}\nCouldn\'t rename file. Maybe there is a file with the same name.')
    print(f'{SPACE}\nDone!\n{SPACE}')
    os.system('pause')
    clearTerminal()

def modifyMetadata(SONGPATH:str)->str:
    audio=openAudio('EasyID3',SONGPATH)
    print(f"{SPACE}\nNo modify: Just press enter.\n{SPACE}")
    NEWTITLE=''
    for key in KEYS:
        CURRVALUE= audio.get(key.lower(), [''])[0]
        NEWVALUE=input(f'{key[0].upper()}{key[1:].lower()} (Current: {CURRVALUE}):\n')
        if NEWVALUE: audio[key.lower()]=NEWVALUE
        if key == 'TITLE': NEWTITLE=audio[key.lower()][0]
    saveAudio(audio)
    return NEWTITLE

def modifyAlbumCover(SONGPATH:str)->None:
    print('New album art path:')
    ACPATH=filedialog.askopenfilename(filetypes=[("Image file",".jpg .png")])
    if ACPATH:
        print(f'{ACPATH}\n')
        audio=openAudio('ID3',SONGPATH)
        try:
            with open(ACPATH,'rb') as ALBUMCOVER:
                audio.delall('APIC')
                ACFORMAT = ACPATH.split('.')[-1]
                if ACFORMAT == 'jpg':
                    NEWAPIC=APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3, desc='Cover',
                        data=ALBUMCOVER.read()
                    )
                elif ACFORMAT == 'png':
                    NEWAPIC=APIC(
                        encoding=3,
                        mime='image/png',
                        type=3, desc='Cover',
                        data=ALBUMCOVER.read()
                    )
                else:
                    print('Path is not an image or image format is not supported')
                    audio.save()
                    return
        except:
            print(f'Wrong path\n{SPACE}')
            audio.save()
            return
        audio.add(NEWAPIC)
        saveAudio(audio)
    else:
        print('No path given')
    
def openAudio(type:str,SONGPATH:str)->ID3|EasyID3|None:
    audio={'EASYID3':EasyID3(SONGPATH),'ID3':ID3(SONGPATH)}.get(type.upper(), None)
    try:
        return audio
    except:
        print(f'Wrong path or path is not a MP3\n{SPACE}')
        return

def saveAudio(audio:ID3|EasyID3)->None:
    audio.save()
    print(f'{SPACE}\nChanges saved!\n{SPACE}')
    os.system('pause')
    clearTerminal()
    
if __name__=="__main__":
    root = tk.Tk()
    root.withdraw()
    
    icon = tk.PhotoImage(file='icon.png')
    root.iconphoto(True, icon)
    
    clearTerminal()
    
    print(f"{SPACE}\nSong(s) path:")
    SONGPATHS=filedialog.askopenfilenames(filetypes=[("Audio file(s)",".mp3")])
    if SONGPATHS:
        for SONGPATH in SONGPATHS:
            clearTerminal()
            print(f"Song path:\n{SONGPATH}")
            modifyMP3(SONGPATH=SONGPATH)
    else:
        print(f'{SPACE}\nNo song(s) selected.\n{SPACE}')
        os.system('pause')
        clearTerminal()