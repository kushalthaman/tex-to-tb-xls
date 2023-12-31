#Finnish Syllabary Building

#we only want those with isgold=1 and freq > 99
def make_syllabary_one(df): #We take from gold1, gold2, gold3 looking at is-gold and freq
    syllables = {}
    gold1_entries = df['gold1']
    gold2_entries = df['gold2']
    gold3_entries = df['gold3']
    frequency = df['freq']
    is_gold_list = df['is-gold']
    
    # print(str(len(column_entries)) + ' ' + str(len(frequency)) + ' ' + str(len(is_gold_list)))

    # count = 0
    # for entry in df['gold2'].tolist():
    #     if not pd.isna(entry):
    #         count += 1

    #604 words with more than 1 syllabification (without checking if is-gold)

    # print(count)

    for word1, word2, word3, freq, is_gold in zip(gold1_entries, gold2_entries, gold3_entries, frequency, is_gold_list):
        # if pd.isna(word):
        #     continue
        if freq < 100 or not is_gold:
            continue

        increment = 1.0/3
        if pd.isna(word3):
            increment = 0.5
            word3 = ''
        if pd.isna(word2):
            increment = 1.0
            word2 = ''

        word1, word2, word3 = str(word1), str(word2), str(word3)

        if word1 == 'aal.lon':
            print(word2 + ', ' + word3)
            print(str(increment))

        def strip(word):
            word = word.replace(' ', '.')
            word = word.replace('-', '.')
            word = word.replace('_', '.')
            word = word.replace('`', '')
            word = word.replace('\'', '')

            return word

        for word in [word1, word2, word3]:
            word = strip(word)
            word_syls = word.split('.')
            if '' in word_syls:
                word_syls.remove('')

            first = True
            for syl in word_syls:
                if first:
                    first = False
                    entry = (syl, True)
                else:
                    entry = (syl, False)
                if entry in syllables:
                    syllables[entry][0] += increment
                    syllables[entry][1] += freq*increment
                else:
                    syllables[entry] = [increment, freq*increment]

    keys = list(syllables.keys())
    values = list(syllables.values())

    index_cols = pd.DataFrame(keys, columns=['Syllable', 'Stressed'])
    syllabary = pd.DataFrame(values, columns=['Type Frequency', 'Token Frequency'])
    syllabary = pd.concat([index_cols, syllabary], axis=1)

    syllabary.reset_index(drop=True, inplace=True)

    syllabary = syllabary[['Syllable', 'Stressed', 'Type Frequency', 'Token Frequency']]
    
    return syllabary

def make_syllabary_two(df): #take from 'lem-P1', ignoring stress
    syllables = {}
    column_entries = df['lem-P1'].astype(str)
    frequency = df['freq']
    is_gold_list = df['is-gold']
    
    for word, freq, is_gold in zip(column_entries, frequency, is_gold_list):
        if pd.isna(word):
            continue
        if freq < 100 or not is_gold:
            continue

        word = str(word)
        word = word.replace(' ', '.')
        word = word.replace('-', '.')
        word = word.replace('_', '.')
        word = word.replace('`', '')
        word = word.replace('\'', '')

        word_syls = word.split('.')

        first = True
        for syl in word_syls:
            if first:
                first = False
                entry = (syl, True)
            else:
                entry = (syl, False)
            if entry in syllables:
                syllables[entry][0] += 1
                syllables[entry][1] += freq
            else:
                syllables[entry] = [1, freq]

    # syllabary = pd.DataFrame.from_dict(syllables, orient='index', columns=['Unweighted Frequency', 'Weighted Frequency'])
    # syllabary['Syllable'] = syllabary.index
    # syllabary.reset_index(drop=True, inplace=True)

    # syllabary = syllabary[['Syllable', 'Unweighted Frequency', 'Weighted Frequency']]
    
    # return syllabary

    keys = list(syllables.keys())
    values = list(syllables.values())

    index_cols = pd.DataFrame(keys, columns=['Syllable', 'Stressed'])
    syllabary = pd.DataFrame(values, columns=['Unweighted Frequency', 'Weighted Frequency'])
    syllabary = pd.concat([index_cols, syllabary], axis=1)

    syllabary.reset_index(drop=True, inplace=True)

    syllabary = syllabary[['Syllable', 'Stressed', 'Unweighted Frequency', 'Weighted Frequency']]
    
    return syllabary


vowels = 'aeiouy{|'
def vowelize(syl):
    result = ''
    for char in syl:
        if char in vowels:
            result += char.upper()
    return result

def templatize(syl):
    result = ''
    for char in syl:
        if char in vowels:
            result += 'V'
        else:
            result += 'C'
    return result

def weight(template):
    return 'VC' in template or 'VV' in template

def onset(syl):
    result = ''
    for char in syl:
        if char in vowels:
            break
        result += char

    if result == syl:
        return ''

    return result

def nuclize(syl):
    result = ''
    for char in syl:
        if char in vowels:
            result += char

    if result == '':
        return syl

    return result

def coda(syl):
    result = ''
    for char in syl[::-1]:
        if char in vowels:
            break
        result += char

    if result == syl:
        return ''

    return result[::-1]

def eval_onset(template):
    count = 0
    for char in template:
        if char == 'C':
            count += 1
        else:
            break

    return count > 1

def eval_coda(template):
    count = 0
    for char in template[::-1]:
        if char == 'C':
            count += 1
        else:
            break

    return count > 1

def export_templates(syllabary):
    template_entries = syllabary["Template"].astype(str)

    typestring = 'Type Frequency' if 'Type Frequency' in syllabary.columns else 'Unweighted Frequency'
    tokenstring = 'Token Frequency' if 'Token Frequency' in syllabary.columns else 'Weighted Frequency'

    type_entries = syllabary[typestring]
    token_entries = syllabary[tokenstring]

    templates = {}
    for template, type_count, token_count in zip(template_entries, type_entries, token_entries):
        if template not in templates:
            templates[template] = [type_count, token_count]
        else:
            templates[template][0] += type_count
            templates[template][1] += token_count

    template_table = pd.DataFrame.from_dict(templates, orient='index', columns=[typestring, tokenstring])
    template_table['Template'] = template_table.index
    template_table.reset_index(drop=True, inplace=True)

    template_table = template_table[['Template', typestring, tokenstring]]

    template_table.sort_values(by = tokenstring, ascending = False, inplace = True, kind = 'quicksort')

    suffix = 1 if typestring == 'Type Frequency' else 2
    template_table.to_excel("FinnishTemplateTable" + str(suffix) + ".xlsx", index=False)

    
df = pd.read_csv('aamulehti-1999.csv', sep=',')

syllabary1 = make_syllabary_one(df)
syllabary1.sort_values(by = 'Token Frequency', ascending = False, inplace = True, kind = 'quicksort')

syllabary2 = make_syllabary_two(df)
syllabary2.sort_values(by = 'Weighted Frequency', ascending = False, inplace = True, kind = 'quicksort')

syllabary1['Vowel'] = syllabary1['Syllable'].apply(vowelize)
syllabary1['Template'] = syllabary1['Syllable'].apply(templatize)
syllabary1['Weight'] = syllabary1['Template'].apply(weight)
syllabary1['Complex Onset'] = syllabary1['Template'].apply(eval_onset)
syllabary1['Complex Coda'] = syllabary1['Template'].apply(eval_coda)
syllabary1['Onset'] = syllabary1['Syllable'].apply(onset)
syllabary1['Nucleus'] = syllabary1['Syllable'].apply(nuclize)
syllabary1['Coda'] = syllabary1['Syllable'].apply(coda)

syllabary2['Vowel'] = syllabary2['Syllable'].apply(vowelize)
syllabary2['Template'] = syllabary2['Syllable'].apply(templatize)
syllabary2['Weight'] = syllabary2['Template'].apply(weight)
syllabary2['Complex Onset'] = syllabary2['Template'].apply(eval_onset)
syllabary2['Complex Coda'] = syllabary2['Template'].apply(eval_coda)
syllabary2['Onset'] = syllabary2['Syllable'].apply(onset)
syllabary2['Nucleus'] = syllabary2['Syllable'].apply(nuclize)
syllabary2['Coda'] = syllabary2['Syllable'].apply(coda)

syllabary1.to_excel("FinnishSyllabary1.xlsx", index=False)

syllabary2.to_excel("FinnishSyllabary2.xlsx", index=False)

export_templates(syllabary1)

export_templates(syllabary2)
