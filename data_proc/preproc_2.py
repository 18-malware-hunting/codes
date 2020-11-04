import os
import pandas as pd
import re

import sys
import csv

from datetime import datetime
import tld
import math
import numpy as np
import pickle
import string
from collections import defaultdict, Counter

# dgaTLD_list = ["cf", "recipes", "email", "ml", "gq", "fit", "cn", "ga", "rest", "tk"]
hmm_add = r"./static/hmm_matrix.csv"
gib_add = r"./static/gib_model.pki"
gramfile_add = r"./static/n_gram_rank_freq.txt"
private_tld_file = r"./static/private_tld.txt"
hmm_prob_threshold = -120


accepted_chars = 'abcdefghijklmnopqrstuvwxyz '
pos = dict([(char, idx) for idx, char in enumerate(accepted_chars)])
def get_name(url):

    url = url.strip(string.punctuation)
    try:
        TLD = tld.get_tld(url, as_object=True, fix_protocol=True)
        SLD = tld.get_tld(url, as_object=True, fix_protocol=True).domain

    except Exception as e:
        na_list = url.split(".")
        TLD = na_list[-1]
        SLD = na_list[-2]
    return str(TLD), str(SLD)

def load_gramdict_privatetld():

    rank_dict = dict()
    with open(gramfile_add, 'r') as f:
        for line in f:
            cat, gram, freq, rank = line.strip().split(',')
            rank_dict[gram] = int(rank)
    pritld_list = list()
    with open(private_tld_file, 'r') as f:
        pritld_list = set(line.strip() for line in f)
    return rank_dict, pritld_list

def cal_ent_gni_cer(SLD):

    f_len = float(len(SLD))
    count = Counter(i for i in SLD).most_common()  # unigram frequency
    ent = -sum(float(j / f_len) * (math.log(float(j / f_len), 2)) for i, j in count)  # shannon entropy
    gni = 1 - sum(float(j / f_len) * float(j / f_len) for i, j in count)
    cer = 1 - max(float(j/ f_len) for i, j in count)
    return ent, gni, cer


def cal_rep_letter(SLD):

    count = Counter(i for i in SLD if i.isalpha()).most_common()
    sum_n = 0
    for letter, cnt in count:
        if cnt > 1:
            sum_n += 1
    return sum_n
def cal_gib(SLD):

    gib_model = pickle.load(open(gib_add, 'rb'))
    mat = gib_model['mat']
    threshold = gib_model['thresh']

    log_prob = 0.0
    transition_ct = 0
    SLD = re.sub("[^a-z]", "", SLD)
    gram2 = [SLD[i:i + 2] for i in range(len(SLD) - 1)]
    for a, b in gram2:
        log_prob += mat[pos[a]][pos[b]]
        transition_ct += 1
    # The exponentiation translates from log probs to probs.
    prob = math.exp(log_prob / (transition_ct or 1))
    return int(prob > threshold)

def cal_hmm_prob(url):

    hmm_dic = defaultdict(lambda: defaultdict(float))
    with open(hmm_add, 'r') as f:
        for line in f.readlines():
            key1, key2, value = line.rstrip().split('\t')  # key1 can be '' so rstrip() only
            value = float(value)
            hmm_dic[key1][key2] = value
    url = '^' + url.strip('.') + '$'
    gram2 = [url[i:i+2] for i in range(len(url)-1)]
    prob = hmm_dic[''][gram2[0]]

    for i in range(len(gram2)-1):
        prob *= hmm_dic[gram2[i]][gram2[i+1]]
    if prob < math.e ** hmm_prob_threshold:
        prob = -999
    return prob

def SVM_get_feature(url):
    gram_rank_dict, private_tld = load_gramdict_privatetld()
    TLD, SLD = get_name(url)


    has_private_tld = 0
    for tld in private_tld:
        if tld in url:
            has_private_tld = 1
            name_list = tld.split('.')
            TLD = name_list[-1]
            SLD = name_list[-2]

    url = SLD + "." + TLD

    entropy = cal_ent_gni_cer(TLD)[0]

    f_len = float(len(SLD))

    ent_flen = entropy / f_len

    vowel_ratio = len(re.findall(r"a|e|i|o|u", SLD)) / f_len

    digit_ratio = len(re.findall(r"[0-9]", SLD)) / f_len

    repeat_letter = cal_rep_letter(SLD) / f_len

    dig_list = re.findall(r"[0-9]{2,}", url)
    dig_len = [len(dig) for dig in dig_list]
    consec_digit = sum(dig_len) / f_len

    con_list = re.findall(r"[b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z]{2,}", url)
    con_len = [len(con) for con in con_list]
    consec_consonant = sum(con_len) / f_len

    gib_value = cal_gib(SLD)

    hmm_log_prob = cal_hmm_prob(SLD)

    main_domain = '$' + SLD + '$'
    gram2 = [main_domain[i:i + 2] for i in range(len(main_domain) - 1)]
    gram3 = [main_domain[i:i + 3] for i in range(len(main_domain) - 2)]
    gram1_rank = [gram_rank_dict[i] if i in gram_rank_dict else 0 for i in main_domain[1:-1]]
    gram2_rank = [gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in gram2]
    gram3_rank = [gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in gram3]

    avg_gram1_rank = np.mean(gram1_rank)

    avg_gram2_rank = np.mean(gram2_rank)

    avg_gram3_rank = np.mean(gram3_rank)

    std_gram1_rank = np.std(gram1_rank)
 
    std_gram2_rank = np.std(gram2_rank)

    std_gram3_rank = np.std(gram3_rank)

    feature = [entropy, f_len, ent_flen, vowel_ratio, digit_ratio, repeat_letter, consec_digit, consec_consonant,
               gib_value,hmm_log_prob, avg_gram1_rank, avg_gram2_rank, avg_gram3_rank, std_gram1_rank, std_gram2_rank,
               std_gram3_rank, has_private_tld]

    return feature


exclude = set(['__pycache__'])
f=[]
for root, dirs, filenames in os.walk(os.path.join(os.path.expanduser("~"), "%s" % "mytest".lower()), topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    print(filenames)
    print(root)
for filename in (filenames):
    csv_data = pd.read_csv(root + '/' + filename, names=["addr", "type", "source"])
    csv_df = pd.DataFrame(csv_data)
    csv_df = csv_df["addr"]
    csv_df.drop_duplicates(inplace=True)
    print(csv_df.shape[0])
    csv_df.reset_index(drop=True, inplace=True)


    #store as file
    
    fea = open('feature.csv','a+')
    csv_writer=csv.writer(fea)
    csv_writer.writerow(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'])
        
    for i in range(csv_df.shape[0]):
        if re.match(r"\A\d+\.\d+\.\d+\.\d+", csv_df[i]):
            csv_df.drop(index=i, inplace=True)
            continue
        
        f=SVM_get_feature(csv_df[i])
        print(f)
        f.append(0)
        csv_writer.writerow(f)

    fea.close()

    
    print(csv_df.shape[0])
