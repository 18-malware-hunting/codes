import os
import pandas as pd
import re

# import numpy as np
# import string
# import tld
#
#
# def get_name(url):
#     """
#     用python自带库进行域名提取
#     :param url: url
#     :return: 二级域名，顶级域名
#     """
#     url = url.strip(string.punctuation)
#     try:
#         TLD = tld.get_tld(url, as_object=True, fix_protocol=True)
#         SLD = tld.get_tld(url, as_object=True, fix_protocol=True).domain
#
#     except Exception as e:
#         na_list = url.split(".")
#         TLD = na_list[-1]
#         SLD = na_list[-2]
#     return str(TLD), str(SLD)
#
#
# def SVM_get_feature(url):
#     gram_rank_dict, private_tld = load_gramdict_privatetld()
#     TLD, SLD = get_name(url)
#
#     # 17. 是否包含私人域名#
#     has_private_tld = 0
#     for tld in private_tld:
#         if tld in url:
#             has_private_tld = 1
#             name_list = tld.split('.')
#             TLD = name_list[-1]
#             SLD = name_list[-2]
#
#     url = SLD + "." + TLD
#     # 1. 香农熵#
#     entropy = cal_ent_gni_cer(TLD)[0]
#     # 2. SLD长度#
#     f_len = float(len(SLD))
#     # 3. 香农熵与SLD长度比#
#     ent_flen = entropy / f_len
#     # 4. SLD中元音占比#
#     vowel_ratio = len(re.findall(r"a|e|i|o|u", SLD)) / f_len
#     # 5. SLD中数字占比#
#     digit_ratio = len(re.findall(r"[0-9]", SLD)) / f_len
#     # 6. SLD中重复字母占比#
#     repeat_letter = cal_rep_letter(SLD) / f_len
#     # 7. SLD连续数字占比#
#     dig_list = re.findall(r"[0-9]{2,}", url)
#     dig_len = [len(dig) for dig in dig_list]
#     consec_digit = sum(dig_len) / f_len
#     # 8. SLD连续辅音占比#
#     con_list = re.findall(r"[b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|y|z]{2,}", url)
#     con_len = [len(con) for con in con_list]
#     consec_consonant = sum(con_len) / f_len
#     # 9. gib成文检测#
#     gib_value = cal_gib(SLD)
#     # 10. hmm成文检测#
#     hmm_log_prob = cal_hmm_prob(SLD)
#
#     main_domain = '$' + SLD + '$'
#     gram2 = [main_domain[i:i + 2] for i in range(len(main_domain) - 1)]
#     gram3 = [main_domain[i:i + 3] for i in range(len(main_domain) - 2)]
#     gram1_rank = [gram_rank_dict[i] if i in gram_rank_dict else 0 for i in main_domain[1:-1]]
#     gram2_rank = [gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in gram2]
#     gram3_rank = [gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in gram3]
#
#     # 11. 一元排序均值#
#     avg_gram1_rank = np.mean(gram1_rank)
#     # 12. 二元排序均值#
#     avg_gram2_rank = np.mean(gram2_rank)
#     # 13. 三元排序均值#
#     avg_gram3_rank = np.mean(gram3_rank)
#     # 14. 一元排序标准差#
#     std_gram1_rank = np.std(gram1_rank)
#     # 15. 二元排序标准差#
#     std_gram2_rank = np.std(gram2_rank)
#     # 16. 三元排序标准差#
#     std_gram3_rank = np.std(gram3_rank)
#
#     feature = [entropy, f_len, ent_flen, vowel_ratio, digit_ratio, repeat_letter, consec_digit, consec_consonant,
#                gib_ hmm_log_prob, avg_gram1_rank, avg_gram2_rank, avg_gram3_rank, std_gram1_rank, std_gram2_rank,
#                std_gram3_rank, has_private_tld]
#
#     return feature
#

exclude = set(['__pycache__'])
for root, dirs, filenames in os.walk(os.path.join(os.path.expanduser("~"), "%s" % "mytest".lower()), topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    print(filenames)
    print(root)
for filename in sorted(filenames):
    csv_data = pd.read_csv(root + '/' + filename, names=["addr", "type", "source"])
    csv_df = pd.DataFrame(csv_data)
    csv_df = csv_df["addr"]
    csv_df.drop_duplicates(inplace=True)
    print(csv_df.shape[0])
    csv_df.reset_index(drop=True, inplace=True)
    for i in range(csv_df.shape[0]):
        if re.match(r"\A\d+\.\d+\.\d+\.\d+", csv_df[i]):
            csv_df.drop(index=i, inplace=True)
    print(csv_df.shape[0])
