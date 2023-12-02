# 한글 모스 부호
# 문자열 중간에 n이 있으면 문자 하나의 입력 종료, 맨 마지막에 한 번 더 누르면 문장의 종료를 의미하도록 함.
# 즉, Sentence의 마지막에 nn이 있으면 문장이 종료된 것을 의미
'''모스 부호에서 단음을 온점으로 표시하지 않은 것은
switchUser.py, cdsUser.py에서 mqttio.js에 모스 부호 문장과 변환된 문장을 JSON문자열로 보낼 때
JSON문자열이 
'''
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
        'o-oo':'ㄱ', 'oo-o':'ㄴ', '-ooo': 'ㄷ', 'ooo-':'ㄹ', '--':'ㅁ','o--':'ㅂ','--o':'ㅅ',
        '-o-':'ㅇ','o--o':'ㅈ','-o-o':'ㅊ','-oo-':'ㅋ','--oo':'ㅌ','---':'ㅍ','o---':'ㅎ', # 기본 자음 14개
        'o-ooo-oo':'ㄲ','-ooo-ooo':'ㄸ','o--o--':'ㅃ','--o--o':'ㅆ','o--oo--o':'ㅉ', # 쌍자음 5개
        'o-oo--o':'ㄳ','oo-oo--o':'ㄵ','oo-oo---':'ㄶ','ooo-o-oo':'ㄺ','ooo---':'ㄻ',
        'ooo-o--':'ㄼ','ooo---o':'ㄽ','ooo---oo':'ㄾ','ooo----':'ㄿ','ooo-o---':'ㅀ','o----o':'ㅄ' # 종성 특수자음 11개
}
# 모음 딕셔너리
dicVowels = {
        'o':'ㅏ','oo':'ㅑ','-':'ㅓ','ooo':'ㅕ','o-':'ㅗ','-o':'ㅛ',
        'oooo':'ㅜ','o-o':'ㅠ','-oo':'ㅡ','oo-':'ㅣ', '--o-':'ㅐ','-o--':'ㅔ' 
        # 모음 12개 / 복잡한 모음은 분리된 상태로 반환된 후 join_jamos 함수에서 이어붙임.
} 
# 숫자, 기호(온점(.)과 공백만 포함) 딕셔너리
dicNumAndSymbol = {
        'o----':'1','oo---':'2','ooo--':'3','oooo-':'4','ooooo':'5','-oooo':'6',
        '--ooo':'7','---oo':'8','----o':'9','-----':'0','o-o-o-':'o','o--o-':' '
} 