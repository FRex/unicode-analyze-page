import collections
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

# some characters have both a name in UnicodeData.txt and a kDefinition in Unihan_Readings.txt
# for example 63787 is both 'CJK COMPATIBILITY IDEOGRAPH-F92B' and 'wolf'
# so find those duplicates here and merge their two strings into one
dedup = collections.defaultdict(list)
for codepoint, text in out:
    dedup[codepoint].append(text)

doubles = [item for item in dedup.items() if len(item[1]) > 1]
if doubles:
    print(f"{len(doubles)} codepoints have duplicate texts.")
    # for codepoint, texts in doubles:
    # print(f"{codepoint} - {hex(codepoint)} - {texts}")
else:
    print("No codepoints with duplicate texts.")

# join the texts if there is more than one plus sort output by codepoint
out = sorted((codepoint, " ".join(texts)) for codepoint, texts in dedup.items())

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
