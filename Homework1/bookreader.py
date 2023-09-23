file = open("phonebook.txt", "r", encoding="UTF8")
# phonebook.txt를 읽기 모드로 엶.

for line in file.readlines(): 
        ''' 
        readlines 함수를 통해 위에서 열었던 phonebook.txt를
        한 줄씩 읽어서 line 변수에 저장
        for 문은 phonebook.txt의 모든 내용을 읽을 때까지 반복
        '''
        aline = line.strip() 
        '''
        line 변수에 포함되는 줄바꿈 문자를
        strip 함수로 삭제한 후 aline 변수에 저장
        '''
        print(aline) # aline 변수를 출력
file.close()