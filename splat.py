import tkinter as tk
import urllib.request, json
from pprint import pprint

'''
Splat
'''
#user1 = input ("Input username 1: ")
user1 = 'micnem00'

TopArtists = []
for i in range(10):
    with urllib.request.urlopen(" http://ws.audioscrobbler.com//2.0/?method=user.gettopartists&user=" + user1 + "&api_key=61232e986c165da82d1903ac0bfcfac9&format=json") as url:
        data = json.loads(url.read().decode())
        TopArtists.append(data['topartists']['artist'][i]['name'])
        print(TopArtists[i])


def cbc():
    return lambda : callback()

def callback():
    s = TopArtists[9]
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