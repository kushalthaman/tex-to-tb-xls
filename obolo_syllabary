#Make the syllabary

def make_syllabary(df):
    syllables = {}

    column_entries = df["PH + Syl"].astype(str)

    # collects all syllables
    for word, freq in zip (column_entries.tolist(), df["Token Frequency"].tolist()):
        if freq < 0: # excluded words should not be considered
            continue
        word_syls = word.split(".")
        for syl in word_syls:
            if syl == "":
                continue
            if syl in syllables:
                syllables[syl][0] += 1
                syllables[syl][1] += freq
            else:
                syllables[syl] = [1, freq]

    syllabary = pd.DataFrame.from_dict(syllables, orient='index', columns=['Type Frequency', 'Token Frequency'])
    syllabary['Segmental Token'] = syllabary.index
    syllabary.reset_index(drop=True, inplace=True)

    syllabary = syllabary[['Segmental Token', 'Type Frequency', 'Token Frequency']]
    
    return syllabary

def export_templates(syllabary):
    template_entries = syllabary["Template"].astype(str)
    type_entries = syllabary["Type Frequency"].astype(int)
    token_entries = syllabary["Token Frequency"].astype(int)

    templates = {}

    for template, type_count, token_count in zip(template_entries, type_entries, token_entries):
        if template not in templates:
            templates[template] = [type_count, token_count]
        else:
            templates[template][0] += type_count
            templates[template][1] += token_count

    template_table = pd.DataFrame.from_dict(templates, orient='index', columns=['Type Frequency', 'Token Frequency'])
    template_table['Template'] = template_table.index
    template_table.reset_index(drop=True, inplace=True)

    template_table = template_table[['Template', 'Type Frequency', 'Token Frequency']]

    template_table.sort_values(by = 'Token Frequency', ascending = False, inplace = True, kind = 'quicksort')
    template_table.to_excel("OboloTemplateTable.xlsx", index=False)


def nuclize(word):
    result = ''
    for char in word:
        if char in "aeiouɔ.":
            result += char

    if result == "":
        return word

    return result

def onset(word):
    word = word.replace('t͡ʃ', 'C')
    word = word.replace('d͡ʒ', 'J')
    word = word.replace('ŋ͡m', 'N')
    word = word.replace('k͡p', 'K')
    word = word.replace('ɡ͡b', 'G')

    result = ''
    for char in word:
        if char not in "aeiouɔ.":
            result += char
        else:
            break

    if result == word:
        return ''
    
    result = result.replace('C', 't͡ʃ')
    result = result.replace('J', 'd͡ʒ')
    result = result.replace('N', 'ŋ͡m')
    result = result.replace('K', 'k͡p')
    result = result.replace('G', 'ɡ͡b')

    return result

def coda(word):
    word = word.replace('t͡ʃ', 'C')
    word = word.replace('d͡ʒ', 'J')
    word = word.replace('ŋ͡m', 'N')
    word = word.replace('k͡p', 'K')
    word = word.replace('ɡ͡b', 'G')

    result = ''
    for char in word[::-1]:
        if char not in "aeiouɔ.":
            result = char + result
        else:
            break

    if result == word:
        return ''
    
    result = result.replace('C', 't͡ʃ')
    result = result.replace('J', 'd͡ʒ')
    result = result.replace('N', 'ŋ͡m')
    result = result.replace('K', 'k͡p')
    result = result.replace('G', 'ɡ͡b')

    return result



def templatize(word):
    word = word.replace('t͡ʃ', 'C')
    word = word.replace('d͡ʒ', 'J')
    word = word.replace('ŋ͡m', 'N')
    word = word.replace('k͡p', 'K')
    word = word.replace('ɡ͡b', 'G')

    result = ""
    for char in word:
        if char in 'aeiouɔ':
            result += 'V'
        else:
            result += 'C'

    return result

df = pd.read_excel("WordTable.xlsx")
syllabary = make_syllabary(df)
syllabary.sort_values(by = 'Token Frequency', ascending = False, inplace = True, kind = 'quicksort')

syllabary['Segmental Token'] = syllabary['Segmental Token'].astype(str)
syllabary['Onset'] = syllabary['Segmental Token'].apply(onset)
syllabary['Nucleus'] = syllabary['Segmental Token'].apply(nuclize)
syllabary['Coda'] = syllabary['Segmental Token'].apply(coda)
syllabary['Template'] = syllabary['Segmental Token'].apply(templatize)

export_templates(syllabary)

syllabary.to_excel("OboloSyllabary.xlsx", index=False)
