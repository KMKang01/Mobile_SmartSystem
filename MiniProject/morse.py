# 한글 모스 부호
# 문자열 중간에 n이 있으면 문자 하나의 입력 종료, 맨 마지막에 한 번 더 누르면 문장의 종료를 의미하도록 함.
# 즉, Sentence의 마지막에 nn이 있으면 문장이 종료된 것을 의미

from sys import maxsize
from unittest import result
from unicode import join_jamos # 나열된 자모음을 합치는 패키지(코드 출처: https://github.com/kaniblu/hangul-utils)
#    자모음 결합: join_jamos(변환할 분리된 문자열)

# 사용자로부터 입력이 완료된 모스 부호 문장을 해석하고, 자모음이 분리된 문자열로 반환하는 함수
def morseCode(sentence): 
    letter = sentence.split('n') # 매개변수로 전달된 sentence를 letter에 'n'을 기준으로 잘라서 저장
    tmp = []
    for char in letter[:-2]: # 맨 마지막 n은 공백이므로 제외하고 마지막에서 두번째 글자까지 반복
        if(switch(char)=='No Char'): # 딕셔너리에 없는 글자가 입력된 경우
            return 'Wrong' # Wrong이라는 문자열을 전달하며 함수 종료
        else: # 딕셔너리에 존재하는 글자인 경우
            tmp.append(switch(char)) # switch 함수를 통해 얻은 글자를 tmp배열의 끝에 덧붙이며 저장
    result = ''.join(tmp) # tmp배열의 원소들을 ''을 붙이며 result 변수에 문자열로 저장
    return result # 문자열 전달 - 이때, 문자열은 아직 분리되어 있음. ex) "ㄱㅏㅇㅇㅏㅈㅣ"

# 전달된 모스 부호 문장의 글자에 대해 판별하고 반환하는 함수
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
# 자음 딕셔너리
dicConsonants = {
        '.-..':'ㄱ', '..-.':'ㄴ', '-...': 'ㄷ', '...-':'ㄹ', '--':'ㅁ','.--':'ㅂ','--.':'ㅅ',
        '-.-':'ㅇ','.--.':'ㅈ','-.-.':'ㅊ','-..-':'ㅋ','--..':'ㅌ','---':'ㅍ','.---':'ㅎ', # 기본 자음 14개
        '.-...-..':'ㄲ','-...-...':'ㄸ','.--.--':'ㅃ','--.--.':'ㅆ','.--..--.':'ㅉ', # 쌍자음 5개
        '.-..--.':'ㄳ','..-..--.':'ㄵ','..-..---':'ㄶ','...-.-..':'ㄺ','...---':'ㄻ',
        '...-.--':'ㄼ','...---.':'ㄽ','...---..':'ㄾ','...----':'ㄿ','...-.---':'ㅀ','.----.':'ㅄ' # 종성 특수자음 11개
}
# 모음 딕셔너리
dicVowels = {
        '.':'ㅏ','..':'ㅑ','-':'ㅓ','...':'ㅕ','.-':'ㅗ','-.':'ㅛ',
        '....':'ㅜ','.-.':'ㅠ','-..':'ㅡ','..-':'ㅣ', '--.-':'ㅐ','-.--':'ㅔ' 
        # 모음 12개 / 복잡한 모음은 분리된 상태로 반환된 후 join_jamos 함수에서 이어붙임.
} 
# 숫자, 기호(온점(.)과 공백만 포함) 딕셔너리
dicNumAndSymbol = {
        '.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6',
        '--...':'7','---..':'8','----.':'9','-----':'0','.-.-.-':'.','.--.-':' '
} 