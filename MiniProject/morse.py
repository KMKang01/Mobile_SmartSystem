# 한글 모스 부호
# buttonFin을 문자 중간에 누르면 띄어쓰기로, 맨 마지막에 누르면 문장의 종료
# 즉, Sentence의 마지막에 n이 있으면 문장이 종료된 것을 의미
from sys import maxsize
from unittest import result
from jamo import h2j, j2hcj # 한글 자모 분리에 대한 패키지가 있어서 사용
from unicode import join_jamos # 나열된 자모음을 합치는 패키지
#    자모음 분리: j2hcj(h2j(변환할 한글문자열))
#    자모음 결합: join_jamos(변환할 분리된 문자열)

def morseCode(sentence):
    letter = sentence.split('n') # 매개변수로 전달된 sentence를 letter에 'n'을 기준으로 잘라서 저장
    tmp = []
    for char in letter[:-1]: # 맨 마지막 n은 공백이므로 제외
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
        '.-..':'ㄱ', '..-.':'ㄴ', '-...': 'ㄷ', '...-':'ㄹ', '--':'ㅁ','.--':'ㅂ','--.':'ㅅ',
        '-.-':'ㅇ','.--.':'ㅈ','-.-.':'ㅊ','-..-':'ㅋ','--..':'ㅌ','---':'ㅍ','.---':'ㅎ', # 기본 자음 14개
        '.-...-..':'ㄲ','-...-...':'ㄸ','.--.--':'ㅃ','--.--.':'ㅆ','.--..--.':'ㅉ', # 쌍자음 5개
        '.-..--.':'ㄳ','..-..--.':'ㄵ','..-..---':'ㄶ','...-.-..':'ㄺ','...---':'ㄻ',
        '...-.--':'ㄼ','...---.':'ㄽ','...---..':'ㄾ','...----':'ㄿ','...-.---':'ㅀ','.----.':'ㅄ' # 종성 특수자음 11개
} # 자음 딕셔너리
dicVowels = {
        '.':'ㅏ','..':'ㅑ','-':'ㅓ','...':'ㅕ','.-':'ㅗ','-.':'ㅛ','....':'ㅜ','.-.':'ㅠ','-..':'ㅡ','..-':'ㅣ', # 기본 모음 10개
        '--.-':'ㅐ','-.--':'ㅔ' # 복합 모음 11개
} # 모음 딕셔너리
dicNumAndSymbol = {
        '.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6',
        '--...':'7','---..':'8','----.':'9','-----':'0','.-.-.-':'.','.--.-':' '
} # 숫자, 기호(온점(.)과 공백만 포함) 딕셔너리