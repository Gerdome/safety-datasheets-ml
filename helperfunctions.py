#Eingelesene Dokumente
docs = data.doc.unique().tolist()
success = []

success.append(data.loc[row.Index, 'doc'])

for i in success:
    if i in docs:
        docs.remove(i)

print ('---------------Undetected PDFs-----------------------')

for i in docs:
    print (i)

print ('-----------------Open undected PDFS-------------------')

cmd = 'open $(find ' + ospath + '/data/3_pdf -name '
for i in docs:
    cmd = cmd + i + ' -o -name '
cmd = cmd[:-10] + ')'
print(cmd)