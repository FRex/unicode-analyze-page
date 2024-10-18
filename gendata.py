import zipfile
import json


def loadlines(zipname, fname):
    with zipfile.ZipFile(zipname) as f:
        with f.open(fname) as g:
            return g.read().decode("UTF-8").splitlines()


code = loadlines("UCD.zip", "UnicodeData.txt")
uhan = loadlines("Unihan.zip", "Unihan_Readings.txt")
bloc = loadlines("UCD.zip", "Blocks.txt")

unicodeversion = "???"

for x in uhan[:10]:
    if x.startswith("# Unicode Version"):
        unicodeversion = x.replace("# ", "")

out = []
for line in code:
    parts = line.split(";")
    idx = 10 if parts[1] == "<control>" else 1
    out.append((int(parts[0], 16), parts[idx]))

chars = len(out)
for line in uhan:
    parts = line.split(maxsplit=2)
    if len(parts) == 3 and parts[1] == "kDefinition":
        out.append((int(parts[0][2:], 16), parts[2]))

blocks = []
for line in bloc:
    if line.startswith("#") or not line.strip():
        continue
    nums, item = line.split("; ")
    a, b = nums.split("..")
    # NOTE: this range is inclusiv [a, b] not [a, b)
    blocks.append((int(a, 16), int(b, 16), item))


unihan = len(out) - chars

print("blocks: ", len(blocks))
print("chars: ", chars)
print("unihan chars: ", unihan)
print("total: ", chars + unihan)
print("version: ", unicodeversion)

with open("data.js", "w", encoding="ASCII") as fout:
    fout.write("data=JSON.parse('" + json.dumps(out).replace("'", "\\'") + "')\n")

with open("blocks.js", "w", encoding="ASCII") as fout:
    fout.write(f"unicode_version = '{unicodeversion}';\n")
    fout.write("blocks=JSON.parse('" + json.dumps(blocks).replace("'", "\\'") + "')\n")
