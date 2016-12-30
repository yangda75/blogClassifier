import os
import string
files = {'teen_f': [],
         'teen_m': [],
         'adult_f': [],
         'adult_m': [],
         'mature_f': [],
         'mature_m': [], }


def count(file_path, vocab):
    f = open(file_path, encoding="latin-1")
    for line in f.readlines():
        if line == '':
            continue
        if line[0] == '<':
            continue
        # rm punctuation
        new_line = ''.join(c for c in line if c not in string.punctuation)
        for word in new_line.split(' '):
            if word not in vocab.keys():
                vocab[word] = 1
            else:
                vocab[word] += 1


def train(data_folder):
    # load data
    for root, dir_list, file_list in os.walk(data_folder):
        for f in file_list:
            # get tag
            gender = f.split('.')[1]
            age = int(f.split('.')[2])
            if age < 20:
                if gender == 'female':
                    tag = 'teen_f'
                else:
                    tag = 'teen_m'
            elif age < 30:
                if gender == 'female':
                    tag = 'adult_f'
                else:
                    tag = 'adult_m'
            else:
                if gender == 'female':
                    tag = 'mature_f'
                else:
                    tag = 'mature_m'
            files[tag].append(f)
    # count words
    for tag in files.keys():
        vocab = {}
        for f in files[tag]:
            file_path = os.path.join(data_folder, f)
            count(file_path, vocab)
        # write the dict into a csv file
        outfile = open(tag + '.csv', 'w')
        [outfile.write('{0},{1}\n'.format(word, num))
         for word, num in vocab.items()]
