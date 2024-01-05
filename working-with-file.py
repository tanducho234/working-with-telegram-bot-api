



# with open("testing.txt", 'r') as file:
#         content=file.read()
#         print(content)

# file=f.readlines()
# def search_by_name(text:str,file) ->str:
#     keyword: str= text.lower()
#     words=keyword.split()
#     for line in file:
#         if all(word in line.lower() for word in words):
#             return line

# print(search_by_name("Mia Lewis",file))
f=open("testing.txt",'w')
f.write("ABC")
f.close()
import os
os.remove("testing.txt")
if os.path.exists("testing.txt"):
    print("file exists")
else:
    print("file not exists")
