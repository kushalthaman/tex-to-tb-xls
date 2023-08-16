##Adds PH column

def to_ipa(ann):
    ann = "." + ann

    ann = ann.replace('ọ', 'ɔ')
    ann = ann.replace('ny', 'ɲ')
    ann = ann.replace('ch', 't͡ʃ')
    ann = ann.replace('j', 'd͡ʒ')
    ann = ann.replace('.ng', '.ŋg') #NOTE!***
    ann = ann.replace('.nk', '.ŋk')
    ann = ann.replace('.nnw', '.ŋŋw')
    ann = ann.replace('nw', 'ŋw') # this is not incongruent with what is done before, nw is supposed to represent ŋw, nk is only supposed to represent ŋk word-initially, deviation from that is on the bible not on me
    ann = ann.replace('n̄', 'ŋ')

    ann = ann.replace('ŋm', 'ŋ͡m')
    ann = ann.replace('.mkp', '.ŋ͡mkp')
    ann = ann.replace('.mgb', '.ŋ͡mgb')

    ann = ann.replace('kp', 'k͡p')
    ann = ann.replace('gb', 'ɡ͡b') #note that this g is U+0261
    ann = ann.replace('g', 'ɡ') # converted to wack g

    ann = ann.replace('y', 'j')

    ann = ann[1:]

    prev_let = None
    result = ""
    for char in ann:
        if prev_let and prev_let == 'i' and (char in vowels or char == 'ɔ') and char != 'i': # there are no "iii" > "jii" sequences in this data
            result = result[:-1] + 'j' + char
        else:
            result += char
        prev_let = char

    return result

    #ambiguous words:
    #atanga, okpungwu, ojọngwu, ikanwọnge
    #also isnt ikanwọnge ambiguous about nw?
    #ebingwan̄

    #onaan̄ge is written clearly

    #system
    #any nw at all is ŋw
    #any WORD-INITIAL ng is ŋg
    #any WORD-INITIAL nk is NG


    #Obolo syllabification rules:
    #Run CC --> C.C, 
    #AND VCV -> V.CV
    #No final C syllables (group with prior syllable if this occurs)


def syllabify(word):  # not sensible for excluded words
    result = ""
    # prev_seg = None

    # dividers = " 1\n,.2:3“!”4567890-?();‘’–[]"
    # capitals = "IBEMAUÒOCSÌNÀÎPGKTYǸLJRDFỌWÈÙÔH"
    # = "fknrmbwjsyltgpdchǹ" + "BMCSNPGKTYǸLJRDFWH"
    # c_list = ['f', 'k', 'n', 'r', 'm', 'b', 'w', 'j', 's', 'l', 't', 'g', 'ɡ', 'p', 'd', 'ɲ', 't͡ʃ', 'd͡ʒ', 'ŋ', 'ŋ͡m', 'ŋ͡mkp', 'k͡p', 'ɡ͡b'
    #           'fj', 'kj', 'nj', 'rj', 'mj', 'bj', 'wj', 'jj', 'sj', 'lj', 'tj', 'gj', 'ɡj', 'pj', 'dj', 'ɲj', 't͡ʃj', 'd͡ʒj', 'ŋj', 'ŋ͡mj', 'ŋ͡mkpj', 'k͡pj', 'ɡ͡bj',
    #             'fw', 'kw', 'nw', 'rw', 'mw', 'bw', 'ww', 'jw', 'sw', 'lw', 'tw', 'gw', 'ɡw', 'pw', 'dw', 'ɲw', 't͡ʃw', 'd͡ʒw', 'ŋw', 'ŋ͡mw', 'ŋ͡mkpw', 'k͡pw', 'ɡ͡bw']

    v_list = ['u', 'o', 'e', 'i', 'a', 'ɔ']
    # v_nasal = '̄'

    word = word.replace('t͡ʃ', 'C')
    word = word.replace('d͡ʒ', 'J')
    word = word.replace('ŋ͡m', 'N')
    word = word.replace('k͡p', 'K')
    word = word.replace('ɡ͡b', 'G')

    glides = ['w', 'j']

    #this deserves some re-writing
    k = 0
    result = ""
    while(k < len(word)):
        if k-1 >= 0 and k+1 < len(word) and word[k-1] in v_list and word[k] not in v_list and word[k+1] in v_list + glides:
            result += '.' + word[k]
        elif k+1 < len(word)-1 and word[k] not in v_list and word[k+1] not in v_list + glides: # attempt to fix nt
            result += word[k] + '.'
        else:
            result += word[k]
        k += 1

    

    # VCV > V.CV this is good
    # CC > C.C this is good
    # VCgV > V.CgV NOTE THIS IS NOT A GIVEN, REMEMBER
        # *Cg > C.g (we do not want this)

    result = result.replace('C', 't͡ʃ')
    result = result.replace('J', 'd͡ʒ')
    result = result.replace('N', 'ŋ͡m')
    result = result.replace('K', 'k͡p')
    result = result.replace('G', 'ɡ͡b')

    return '.' + result + '.'


df = pd.read_excel('WordTable.xlsx')
df['PH'] = df['Segmental Token'].apply(to_ipa)
df["PH"] = df["PH"].astype(str)
df['PH + Syl'] = df['PH'].apply(syllabify)

df.to_excel('WordTable.xlsx', index=False)
