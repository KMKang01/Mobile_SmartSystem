# 한글 모스 부호
# 문자열 중간에 n이 있으면 문자 하나의 입력 종료, 맨 마지막에 한 번 더 누르면 문장의 종료
# 즉, Sentence의 마지막에 nn이 있으면 문장이 종료된 것을 의미
from sys import maxsize
from unittest import result
from jamo import h2j, j2hcj # 한글 자모 분리에 대한 패키지가 있어서 사용
from unicode import join_jamos # 나열된 자모음을 합치는 패키지
#    자모음 분리: j2hcj(h2j(변환할 한글문자열))
#    자모음 결합: join_jamos(변환할 분리된 문자열)

def morseCode(sentence):
    letter = sentence.split('n') # 매개변수로 전달된 sentence를 letter에 'n'을 기준으로 잘라서 저장
    tmp = []
    for char in letter[:-2]: # 맨 마지막 n은 공백이므로 제외
        if(switch(char)=='No Char'): # 딕셔너리에 없는 글자가 입력된 경우
            return 'Wrong'
        else:
            tmp.append(switch(char)) # tmp 배열에 
    result = ''.join(tmp)
    return result

def switch(char):
    if(char in dicConsonants):
        return dicConsonants[char]
    elif(char in dicVowels):
        return dicVowels[char]
    elif(char in dicNumAndSymbol):
        return dicNumAndSymbol[char]
    else:
        return 'No Char'

# 모스 부호가 key, 해당하는 자음 or 모음 or 숫자 or 기호가 value
dicConsonants = {
        'o-oo':'ㄱ', 'oo-o':'ㄴ', '-ooo': 'ㄷ', 'ooo-':'ㄹ', '--':'ㅁ','o--':'ㅂ','--o':'ㅅ',
        '-o-':'ㅇ','o--o':'ㅈ','-o-o':'ㅊ','-oo-':'ㅋ','--oo':'ㅌ','---':'ㅍ','o---':'ㅎ', # 기본 자음 14개
        'o-ooo-oo':'ㄲ','-ooo-ooo':'ㄸ','o--o--':'ㅃ','--o--o':'ㅆ','o--oo--o':'ㅉ', # 쌍자음 5개
        'o-oo--o':'ㄳ','oo-oo--o':'ㄵ','oo-oo---':'ㄶ','ooo-o-oo':'ㄺ','ooo---':'ㄻ',
        'ooo-o--':'ㄼ','ooo---o':'ㄽ','ooo---oo':'ㄾ','ooo----':'ㄿ','ooo-o---':'ㅀ','o----o':'ㅄ' # 종성 특수자음 11개
} # 자음 딕셔너리
dicVowels = {
        'o':'ㅏ','oo':'ㅑ','-':'ㅓ','ooo':'ㅕ','o-':'ㅗ','-o':'ㅛ','oooo':'ㅜ','o-o':'ㅠ','-oo':'ㅡ','oo-':'ㅣ', # 기본 모음 10개
        '--o-':'ㅐ','-o--':'ㅔ' # 복합 모음 11개
} # 모음 딕셔너리
dicNumAndSymbol = {
        'o----':'1','oo---':'2','ooo--':'3','oooo-':'4','ooooo':'5','-oooo':'6',
        '--ooo':'7','---oo':'8','----o':'9','-----':'0','o-o-o-':'o','o--o-':' '
} # 숫자, 기호(온점(o)과 공백만 포함) 딕셔너리