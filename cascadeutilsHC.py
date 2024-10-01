import os

def generate_negative_description_file():
    #open out put file to write in. overwrite ALL EXISTING DATA
    with open('neg.txt', 'w') as f:
        #loop for all filenames in negative folder. for each file write the path to that file in the neg.txt
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')