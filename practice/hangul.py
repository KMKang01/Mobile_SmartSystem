#한글 자모음 분리, 결합 연습 코드
#     분리: j2hcj(h2j(변환할 한글문자열))
#     결합: join_jamos(변환할 분리된 문자열)


from jamo import h2j, j2hcj
from unicode import join_jamos

sentence = '-.-n.n..-.n..-.n...n-.-nn'
letter = sentence.split('n') # 매개변수로 전달된 sentence를 letter에 'n'을 기준으로 잘라서 저장
string = ''.join(letter)

print(string)