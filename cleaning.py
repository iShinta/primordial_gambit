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

#def set_priority(keywords):
    #Priorities
    # 1.
    # 2.
    # 3.
    # 4.
    # 5.

def main():
    raw_text = "Help my house is on fire! I got out, but my family is still in there"
    keywords = clean_call(raw_text)
    print(keywords)

main()
