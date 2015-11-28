#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import codecs
import operator
from functools import partial


# adds d2 to d1
def join_dicts(d1, d2, conflict_solver):
    for k,v in d2.items():
        if k in d1:
            d1[k] = conflict_solver(d1[k], v)
        else:
            d1[k] = v
    return d1


def ngram_counts_to_freqs(count_ht, textlen):
    normcoef = 1.0 / textlen
    return { ng: (cnt * normcoef) for ng,cnt in count_ht.items() }


# возвращает пару (словарь, в котором ключём является строчка-n-грамма, значением -- количество n-грамм в text ; аналогичный частотный словарь
def calc_ngram_counts_freqs(text, ngram_len):
    count_ht = dict()
    for i in xrange(len(text) - ngram_len + 1):
        ngram = text[i:i+ngram_len]
        if ngram in count_ht:
            count_ht[ngram] += 1
        else:
            count_ht[ngram] = 1
    return (count_ht, ngram_counts_to_freqs(count_ht, len(text)))


# разбиение текстов автора, тексты которого спрятаны в author_dir, на фрагменты размером frag_size символов
# (или меньше, в случае достижения конца файла)
def fragmentize_author(author_dir, frag_size):
    tdir = os.path.join(author_dir, '')
    fragments = []
    for txtfile in os.listdir(tdir):
        fl = codecs.open(tdir + txtfile, 'r', 'utf-8')
        while True:
            fragment = fl.read(frag_size)
            if fragment == '': # eof
                break
            fragments.append(fragment)
        fl.close()
    return fragments


# возвращает словарь (строка -- имя автора; список фрагментов этого автора)
def fragmentize_all_authors(teach_dir, frag_size):
    fragmentation = dict()
    tdir = os.path.join(teach_dir, '')
    for author_dir in os.listdir(teach_dir):
        author_dir = author_dir.strip('/')
        fragmentation[author_dir] = fragmentize_author(tdir + author_dir, frag_size)
    return fragmentation


# возвращает кортеж (строка -- имя автора; (словарь с количествами слов; словарь с частотами слов))
def author_ngrams_count(author_frag_list, n):
    return map(partial(calc_ngram_counts_freqs, ngram_len=n), author_frag_list) # (author_str, (count_ht, freq_ht))


def count_all_authors(fragmentation, ngram_len):
    return { author_dir : author_ngrams_count(author_frag_list, ngram_len) for author_dir, author_frag_list in fragmentation.items() }


def get_top_k_ngrams(author_ht_tuples, top_k):
    total_count_dict = {}
    for author_name, author_list_of_dicts in author_ht_tuples.items():
        for frag_dicts in author_list_of_dicts:
            join_dicts(total_count_dict, frag_dicts[0], operator.add)
    sorted_dict = sorted(total_count_dict.items(), key = operator.itemgetter(1), reverse = True)
    return map(operator.itemgetter(0), sorted_dict)[0:top_k]


fragments = fragmentize_all_authors('filtertxt', 1500)
counts = count_all_authors(fragments, 2)
top_k_ngrams = get_top_k_ngrams(counts, 100)

print type(top_k_ngrams)
