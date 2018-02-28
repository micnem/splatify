#!/usr/bin/env python
import tkinter as tk
import urllib.request, json
from pprint import pprint

'''
Splat
'''

trackNames = []
for i in range(5):
    with urllib.request.urlopen(" http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=micnem00&api_key=61232e986c165da82d1903ac0bfcfac9&format=json") as url:
        data = json.loads(url.read().decode())
        trackNames.append(data['recenttracks']['track'][i]['artist']['#text'])
        print(trackNames[i])


def cbc():
    return lambda : callback()

def callback():
    s = trackNames[4]
    tex.insert(tk.END, s)
    tex.see(tk.END)    # Scroll if necessary

top = tk.Tk()
tex = tk.Text(master=top)
tex.pack(side=tk.RIGHT)
bop = tk.Frame()
bop.pack(side=tk.LEFT)

b = tk.Button(bop, text="Output", command=cbc())
b.pack()

tk.Button(bop, text='Exit', command=top.destroy).pack()
top.mainloop()
