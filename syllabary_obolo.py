#Make the syllabary



def make_syllabary(df):
    syllables = {}

    column_entries = df["PH + Syl"].astype(str)

    # collects all syllables
    for word, freq, is_lower in zip (column_entries.tolist(), df["Token Frequency"].tolist(), df["Appears Lowercase"].tolist()):
        if freq < 0: # excluded words should not be considered
            continue
        word_syls = word.split(".")
        for syl in word_syls:
            if syl == "":
                continue
            if syl in syllables:
                syllables[syl][0] += 1
                syllables[syl][1] += freq
                if is_lower:
                    syllables[syl][2] = True
            else:
                syllables[syl] = [1, freq, is_lower]

    syllabary = pd.DataFrame.from_dict(syllables, orient='index', columns=['Type Frequency', 'Token Frequency', 'In Lowercased Word'])
    syllabary['Segmental Token'] = syllabary.index
    syllabary.reset_index(drop=True, inplace=True)

    syllabary = syllabary[['Segmental Token', 'Type Frequency', 'Token Frequency', 'In Lowercased Word']]
    
    return syllabary

def make_positional_syllabary(df):
    syllables = {}

    column_entries = df["PH + Syl"].astype(str)

    # collects all syllables
    for word, freq, is_lower in zip (column_entries.tolist(), df["Token Frequency"].tolist(), df["Appears Lowercase"].tolist()):
        if freq < 0: # excluded words should not be considered
            continue
        word_syls = word.split('.')
        word_syls.remove('')

        if not word_syls:
            continue

        syl_count = word.count('.') - 1
        for ind, syl in enumerate(word_syls):
            if syl == '':
                continue

            position = 'Medial'
            if ind == 0:
                if syl_count == 1:
                    position = 'Monosyllable'
                else:
                    position = 'Initial'
            elif ind == syl_count - 1:
                position = 'Final'

            syl_pair = (syl, position)
            if syl_pair in syllables:
                syllables[syl_pair][0] += 1
                syllables[syl_pair][1] += freq
                if is_lower:
                    syllables[syl_pair][2] = True
            else:
                syllables[syl_pair] = [1, freq, is_lower]
    
    keys = list(syllables.keys())

    values = list(syllables.values())

    index_cols = pd.DataFrame(keys, columns=['Segmental Token', 'Position'])
    syllabary = pd.DataFrame(values, columns=['Type Frequency', 'Token Frequency', 'In Lowercased Word'])
    syllabary = pd.concat([index_cols, syllabary], axis=1)

    # syllabary = pd.DataFrame.from_dict(syllables, orient='index', columns=['Type Frequency', 'Token Frequency', 'In Lowercased Word'])
    # syllabary['Segmental Token'] = syllabary.index
    
    syllabary.reset_index(drop=True, inplace=True)

    syllabary = syllabary[['Segmental Token', 'Position', 'Type Frequency', 'Token Frequency', 'In Lowercased Word']]
    
    return syllabary


#input is  a list [syllabary, pos_match], but pos_match is optional (can be None)
def export_templates(syllabary_list):
    syllabary = syllabary_list[0]
    pos_match = syllabary_list[1]

    template_entries = syllabary["Template"].astype(str)
    type_entries = syllabary["Type Frequency"].astype(int)
    token_entries = syllabary["Token Frequency"].astype(int)
    position_entries = ['']*len(token_entries)

    if pos_match:
        position_entries = syllabary["Position"].astype(str)


    templates = {}

    for template, type_count, token_count, position in zip(template_entries, type_entries, token_entries, position_entries):
        if pos_match and position != pos_match:
            continue
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

    if not pos_match:
        pos_match = ''

    template_table.to_excel(pos_match+"OboloTemplateTable.xlsx", index=False)


def nuclize(syl):
    result = ''
    for char in syl:
        if char in "aeiouɔ":
            result += char

    if result == "":
        return syl

    return result

def onset(syl):
    result = ''
    for char in syl:
        if char not in "aeiouɔ":
            result += char
        else:
            break

    if result == syl:
        return ''
    
    return result

def coda(syl):
    result = ''
    for char in syl[::-1]:
        if char not in "aeiouɔ":
            result = char + result
        else:
            break

    if result == syl:
        return ''
    
    return result

def templatize(syl):
    syl = syl.replace('t͡ʃ', 'C')
    syl = syl.replace('d͡ʒ', 'J')
    syl = syl.replace('ŋ͡m', 'N')
    syl = syl.replace('k͡p', 'K')
    syl = syl.replace('ɡ͡b', 'G')
    syl = syl.replace('ɡʷ', 'W')
    syl = syl.replace('kʷ', 'Q')
    syl = syl.replace('ŋʷ', 'V')
    
    result = ""
    for char in syl:
        if char in 'aeiouɔ':
            result += 'V'
        else:
            result += 'C'

    return result



dorsals = {'k', 'ɡ', 'ŋ', 'kʷ', 'ɡʷ', 'ŋʷ'}
def print_dors_counts(syllabary):
    kvvt = 0
    tvvk = 0
    tvk = 0
    kvt = 0
    templates = syllabary['Template'].astype(str)
    onsets = syllabary['Onset'].astype(str)
    codas = syllabary['Coda'].astype(str)
    type_freqs = syllabary['Type Frequency'].astype(int)

    for onset, coda, template, type_freq in zip(onsets, codas, templates, type_freqs):
        if onset in dorsals:
            if 'CVVC' in template:
                kvvt += type_freq
            elif 'CVC' in template:
                kvt += type_freq
        if coda in dorsals:
            if 'CVVC' in template:
                tvvk += type_freq
            elif 'CVC' in template:
                tvk += type_freq
    
    print('kvvt: ' + str(kvvt) + ', tvvk: ' + str(tvvk) + ', kvt: ' + str(kvt) + ', tvk: ' + str(tvk))


def print_codas(syllabary):
    codas = syllabary['Coda'].astype(str)
    token_freqs = syllabary['Token Frequency'].astype(int)

    coda_dict = {}

    for coda, token_freq in zip(codas, token_freqs):
        if coda == '':
            continue
        if coda in coda_dict:
            coda_dict[coda] += token_freq
        else:
            coda_dict[coda] = token_freq
    
    print(coda_dict)


df = pd.read_excel("WordTable.xlsx")
syllabary = make_syllabary(df)
syllabary.sort_values(by = 'Token Frequency', ascending = False, inplace = True, kind = 'quicksort')

syllabary['Segmental Token'] = syllabary['Segmental Token'].astype(str)
syllabary['Onset'] = syllabary['Segmental Token'].apply(onset)
syllabary['Nucleus'] = syllabary['Segmental Token'].apply(nuclize)
syllabary['Coda'] = syllabary['Segmental Token'].apply(coda)
syllabary['Template'] = syllabary['Segmental Token'].apply(templatize)

export_templates([syllabary, None])

positional_syllabary = make_positional_syllabary(df)
positional_syllabary.sort_values(by = 'Token Frequency', ascending = False, inplace = True, kind = 'quicksort')
positional_syllabary['Segmental Token'] = positional_syllabary['Segmental Token'].astype(str)
positional_syllabary['Onset'] = positional_syllabary['Segmental Token'].apply(onset)
positional_syllabary['Nucleus'] = positional_syllabary['Segmental Token'].apply(nuclize)
positional_syllabary['Coda'] = positional_syllabary['Segmental Token'].apply(coda)
positional_syllabary['Template'] = positional_syllabary['Segmental Token'].apply(templatize)

export_templates([positional_syllabary, 'Initial'])
export_templates([positional_syllabary, 'Medial'])
export_templates([positional_syllabary, 'Final'])
export_templates([positional_syllabary, 'Monosyllable'])

print_codas(syllabary)
print_dors_counts(syllabary)
syllabary.to_excel("OboloSyllabary.xlsx", index=False)
positional_syllabary.to_excel("PositionalOboloSyllabary.xlsx", index=False)
