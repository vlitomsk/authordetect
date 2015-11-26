#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import codecs

# возвращает словарь, в котором ключём является строчка-n-грамма, значением -- количество n-грамм в text 
def calc_ngram_counts(text, n):
    count_ht = dict() 
    for i in xrange(len(text) - n + 1):
        ngram = text[i:i+n]
        if ngram in count_ht:
            count_ht[ngram] += 1
        else:
            count_ht[ngram] = 1
    return count_ht

# count_len_pair -- результат calc_ngram_counts
def ngram_counts_to_freqs(count_ht, textlen):
    normcoef = 1.0 / textlen
    return { ng: (cnt * normcoef) for ng,cnt in count_ht.items() }

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
    for author_dir in os.listdir(teach_dir):
        author_dir = author_dir.strip('/')
        fragmentation[author_dir] = fragmentize_author(author_dir, frag_size)
    return fragmentation

# good name; used only in author_ngrams_count
def map_helper(fragment, ngram_len):
    count_ht = calc_ngram_counts(fragment, ngram_len)
    return (count_ht, ngram_counts_to_freqs(count_ht, len(fragment)))

# возвращает кортеж (строка -- имя автора; (словарь с количествами слов; словарь с частотами слов))
def author_ngrams_count(author_frag, n):
    fragments = author_frag[1]
    return (author_frag[0], map(calc_ngram_counts(lambda x : calc_ngram_counts(x, n))

def count_all_authors(fragmentation):


def get_top_k_ngrams(train_set, top_k):
    



fragmentize_all_authors('filtertxt', 1500)
