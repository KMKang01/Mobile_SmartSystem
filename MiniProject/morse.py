# 한글 모스 부호
# buttonFin이 한 번 눌리면 띄어쓰기, 두 번 눌리면 문장의 종료
# 즉, Sentence의 마지막에 nn 이 연속으로 있으면 문장이 종료된 것을 의미
from jamo import h2j, j2hcj # 한글 자모 분리에 대한 패키지가 있어서 사용
from unicode import join_jamos # 나열된 자모음을 합치는 패키지
#    자모음 분리: j2hcj(h2j(변환할 한글문자열))
#    자모음 결합: join_jamos(변환할 분리된 문자열)

def morseCode(sentence):
    letter = sentence.split('n') # 매개변수로 전달된 sentence를 letter에 'n'을 기준으로 잘라서 저장
    string = ''
    for char in letter:
        if(switch(char)=='No Char'):
            return 'Wrong'
        string = ''.join(switch(char))
    


def switch(char):
    # 모스 부호가 key, 해당하는 자음 or 모음 or 숫자 or 기호가 value
    dicConsonants = {
        '.-..':'ㄱ', '..-.':'ㄴ', '-...': 'ㄷ', '...-':'ㄹ', '--':'ㅁ','.--':'ㅂ','--.':'ㅅ',
        '-.-':'ㅇ','.--.':'ㅈ','-.-.':'ㅊ','-..-':'ㅋ','--..':'ㅌ','---':'ㅍ','.---':'ㅎ', # 기본 자음 14개
        '.-...-..':'ㄲ','-...-...':'ㄸ','.--.--':'ㅃ','--.--.':'ㅆ','.--..--.':'ㅉ', # 쌍자음 5개
        '.-..--.':'ㄳ','..-..--.':'ㄵ','..-..---':'ㄶ','...-.-..':'ㄺ','...---':'ㄻ',
        '...-.--':'ㄼ','...---.':'ㄽ','...---..':'ㄾ','...----':'ㄿ','...-.---':'ㅀ','.----.':'ㅄ' # 종성 특수자음 11개
    } # 자음 딕셔너리
    dicVowels = {
        '.':'ㅏ','..':'ㅑ','-':'ㅓ','...':'ㅕ','.-':'ㅗ',
        '-.':'ㅛ','....':'ㅜ','.-.':'ㅠ','-..':'ㅡ','..-':'ㅣ','--.-':'ㅐ','-.--':'ㅔ',
    } # 모음 딕셔너리
    dicNumAndSymbol = {
        '.----':'1','..---':'2','...--':'3','....-':'4','.....':'5','-....':'6',
        '--...':'7','---..':'8','----.':'9','-----':'0','.-.-.-':'.','.--.-':' '
    } # 숫자, 기호(온점(.)과 공백만 포함) 딕셔너리

    if(char in dicConsonants):
        return dicConsonants.get(char)
    elif(char in dicVowels):
        return dicVowels.get(char)
    elif(char in dicNumAndSymbol):
        return dicNumAndSymbol.get(char)
    else:
        return 'No Char'