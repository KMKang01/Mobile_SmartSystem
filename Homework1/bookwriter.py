import sys
try:
        file = open('phonebook.txt','w')
        '''
        phonebook.txt 파일이 디렉토리 내부에 있으면 쓰기 모드로 열고,
        phonebook.txt 파일이 디렉토리 내부에 없으면 phonebook.txt를 생성한 후
        쓰기 모드로 엶.
        '''
except IOError:
        sys.exit("파일을 열 수 없습니다.")

while(True): # 사용자의 입력으로 끝날 수 있도록 무한 루프를 생성
        name = input("name >> ")
        if(name == "exit"): # 사용자의 입력이 exit인 경우 종료
                break
        tel = int(input("tel >> "))
        data = "%s,%d\n" %(name,tel) # data 변수에 사용자의 입력을 저장
        file.write(data) # data 변수를 phoenbook.txt에 입력

file.close()
