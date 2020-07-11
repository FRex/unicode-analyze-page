import zipfile
import json

def loadlines(zipname, fname):
    with zipfile.ZipFile(zipname) as f:
        with f.open(fname) as g:
            return g.read().decode('UTF-8').splitlines()

code = loadlines('UCD.zip', 'UnicodeData.txt')
uhan = loadlines('Unihan.zip', 'Unihan_Readings.txt')

out = []
for line in code:
    parts = line.split(';')
    idx = 10 if parts[1] == '<control>' else 1
    out.append((int(parts[0], 16), parts[idx]))

chars = len(out)
for line in uhan:
    parts = line.split(maxsplit=2)
    if len(parts) == 3 and parts[1] == 'kDefinition':
        out.append((int(parts[0][2:], 16), parts[2]))

unihan = len(out) - chars
print("chars: ", chars)
print("unihan chars: ", unihan)
print("total: ", chars + unihan)
open('data.js', 'w').write("data=JSON.parse('" + json.dumps(out).replace("'", "\\'") + "')\n")
