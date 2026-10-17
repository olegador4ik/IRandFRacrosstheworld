import requests
import json
from bs4 import BeautifulSoup

fl = [1.1, 1.6, 2.1, 3.0, 4.0]
il = [-10, -5, 0, 5, 15]
rp = {"Turkey": "Türkiye", "C\u00c3\u00b4te_d'Ivoire": "Cote_d_Ivoire", "Guinea-Bissau": "Guinea_Bissau", 
      "Czech_Republic_(Czechia)": "Czechia", "Timor-Leste": "Timor_Leste",
      "State_of_Palestine": "Palestinian_Territories"}

def h0(e, l):
    r = [0, 0]
    for i in range(len(l)):
        if e > l[i]:
            r[0] = (i+1) * (256//len(l))
            r[1] = i
        else:
            continue
    return r

def h1(r):
    r = format(r, "X")
    if len(r) == 1:
        r = "0"+r
    return r

def h(f, e):
    q = 1
    x = h0(f, fl)
    y = h0(e, il)
    z = 16*x[1]*y[1]
    if z == 0:
        q = 0
    return f"#{h1(x[0])}{h1(z-(q*1))}{h1(y[0])}"

r = {"groups" : {}}

for i in range(6):
    a = 0
    s = ["", ""]
    if i == 5:
        a = 1
        i = 4
        s[0] = ">"
    for j in range(6):
        b = 0
        s[1] = ""
        if j == 5:
            b = 1
            j = 4
            s[1] = ">"
        k = h(float(fl[i]+a), int(il[j]+b))
        r["groups"][k] = {}
        r["groups"][k]["label"] = f"{s[0]}{fl[i]}, {s[1]}{il[j]*0.01}%"
        r["groups"][k]["paths"] = []

url = "https://www.worldometers.info/world-population/population-by-country/"
text = requests.get(url).text
soup = BeautifulSoup(text, "html.parser").find("tbody")
for row in soup.find_all("tr"):
    d = [row.find_all("td")[i].get_text().replace(",", "") for i in [1, 2, 7, 8]]
    d[0] = d[0][2:-2].replace(" ", "_")
    if d[0] in rp.keys():
        d[0] = rp[d[0]]
    d[2] = d[2].replace("â\x88\x92", "-")
    d[1] = int(d[2]) * 10000 // int(d[1])
    k = h(float(d[3]), int(d[1]))
    r["groups"][k]["paths"].append(d[0])

with open("extension.txt", "r") as f:
    j = json.loads(f.read())
    j.update(r)
    r = open("result.txt", "w")
    r.write(json.dumps(j))


