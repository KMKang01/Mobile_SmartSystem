file = open("phonebook.txt", "r", encoding="UTF8")
# phonebook.txt를 읽기 모드로 엶.

for line in file.readlines(): 
        ''' 
        readlines 함수를 통해 위에서 열었던 phonebook.txt를
        한 줄씩 읽어서 line 변수에 저장
        for 문은 phonebook.txt의 모든 내용을 읽을 때까지 반복
        '''
        tmp = line.split(",",1)
        aline = "이름은 " + tmp[0] + ", 전화번호는 " + tmp[1]
        '''
        tmp로 line에 저장된 문자열을 콤마를 기준으로 나눠서
        각각 tmp[0], tmp[1]에 저장 후 aline 변수에 문자열로 저장
        '''
        print(aline.strip()) # aline 변수를 strip 함수로 줄 바꿈을 지우고 출력
file.close()