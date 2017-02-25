import re

def clean_call(transcript):
    list_transcript = transcript
    #str.replace(res, "[^A-Za-z0-9]", "")
    #re.sub('[^A-Za-z0-9-_*.]', '', res)
    re.sub('[^A-Za-z]', '', list_transcript)
    list_transcript = list_transcript.lower()
    list_transcript = list_transcript.split()

    exclude = ['i', 'you', 'he', 'she', 'we', 'they', 'them',
                'my', 'your', 'his', 'her', 'our', 'their',
                'is', 'in', 'at', 'on',
                'but', 'and',
                'still'
                ]

    list_exclude = []
    for x in list_transcript:
        if x not in exclude:
            list_exclude.append(x)

    res = list_exclude

    return res

def match1(clean_list):
    category_list = ['fire']

    word_count = len(clean_list)

    clean_set = list(set(clean_list))

    pba = 0
    for x in clean_list:
        if x in category_list:
            pba += 1
    pba /= word_count

    return pba

def match2(clean_list):
    category_list = ['flood']

    word_count = len(clean_list)

    clean_set = list(set(clean_list))

    pba = 0
    for x in clean_list:
        if x in category_list:
            pba += 1
    pba /= word_count

    return pba

def match3(clean_list):
    category_list = ['hurricane']

    word_count = len(clean_list)

    clean_set = list(set(clean_list))

    pba = 0
    for x in clean_list:
        if x in category_list:
            pba += 1
    pba /= word_count

    return pba

def match(clean_list):
    category1 = "Fire"
    pba1 = match1(clean_list)
    category = "Flood"
    pba2 = match2(clean_list)
    category = "Hurricane"
    pba3 = match3(clean_list)
    pba = (pba1, pba2, pba3)

    max_pba = max(pba)

    if(max_pba == pba1):
        return category1
    if(max_pba == (pba2)):
        return category2
    if(max_pba == (pba3)):
        return category3

#def set_priority(keywords):
    #Priorities
    # 1.
    # 2.
    # 3.
    # 4.
    # 5.

def main():
    raw_text = "Help my house is on fire ! I got out, but my family is still in there"
    keywords = clean_call(raw_text)
    print(keywords)
    print(match(keywords))

main()
