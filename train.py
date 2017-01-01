import os
import string
files = {'teen_f': [],
         'teen_m': [],
         'adult_f': [],
         'adult_m': [],
         'mature_f': [],
         'mature_m': [], }


def count(file_path, vocab):
    tot = 0
    f = open(file_path, encoding="latin-1")
    for line in f.readlines():
        if line == '':
            continue
        if line[0] == '<':
            continue
        # rm punctuation
        new_line = line.replace('-', ' ')
        new_line = new_line.replace('&nbsp', ' ')
        new_line = new_line.replace('\t', ' ')
        new_line = ''.join(c.lower() for c in new_line
                           if c not in string.punctuation)
        for word in new_line.split(' '):
            tot += 1
            if len(word) <= 20:
                if word not in vocab.keys():
                    vocab[word] = 1
                else:
                    vocab[word] += 1
    return tot


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
    for tag in files:
        vocab = {}
        tot = 0
        for f in files[tag]:
            file_path = os.path.join(data_folder, f)
            tot += count(file_path, vocab)
        print('{0} has {1} words in total'.format(tag, tot))
        # write the dict into a csv file
        outfile = open(tag + '.csv', 'w', encoding="utf-8")
        for word, num in vocab.items():
            if num != 1:
                outfile.write('{0},{1}\n'.format(word, num * 1.0 / tot))
