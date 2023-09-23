file = open("phonebook.txt","r",encoding="UTF8") # phonebook.txt를 읽기 전용으로 엶.
dict = {} # 빈 딕셔너리 생성

for line in file.readlines():
    tmp=line.split(',',1)
    """ split 함수로 file에서 읽어와 저장한 line 변수를
    콤마(,)를 기준으로 분할하여 문자열 배열로 저장 """
    key=tmp[0]
    val=tmp[1]
    dict[key]=val # key와 val을 딕셔너리에 저장

while(True):
        name = input("검색할 이름 >> ") # 사용자 입력
        if(name == "exit"): # exit를 입력 받으면 프로그램 종료
            print("검색을 끝냅니다.")
            break
        
        if(name in dict): # 딕셔너리에서 사용자의 입력과 일치하는 key가 있는지 확인
            msg = name + "의 전화번호는 " + dict.get(name)
            print(msg.strip()) # msg에서 줄바꿈 문자를 제거하기 위해 strip 함수 사용
        else:
            print(name, "은/는 없는 이름입니다.")

file.close()