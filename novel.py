from urllib import request
from bs4 import BeautifulSoup

novel_url = 'http://www.00ksw.com/html/'
novel_code = input('input the novel number\n')
novel_url += novel_code[0:2] + '/' + novel_code

htmldoc = request.urlopen(novel_url)

soup = BeautifulSoup(htmldoc.read().decode('gbk'),"html.parser")
print('《' + soup.h1.string +'》')
novel_file = open(soup.h1.string+'.txt','a')
dd_list = soup.find_all('dd')
name_link_list = list(map(lambda var:(var.a.get_text(),var.a['href']),dd_list))
print('本书共有',len(name_link_list),'章')
cnt = 0
for var in name_link_list:
    if cnt < 658:
        cnt+=1
        continue
    print('\r当前已下载' + str(cnt) + '章',end='')
    novel_text_url = novel_url +'/'+ var[1]
    try:
        htmldoc = request.urlopen(novel_text_url)
    except:
        print('第',cnt,'章出现异常，已跳过')
        continue
    soup = BeautifulSoup(htmldoc.read().decode('gbk'),"html.parser")
    #novel_file.write('\n' + var[0] + '\n' + str(soup.find('div',id = 'content')).replace('<br/><br/>',u'\n')[18:-6].replace(u'\xa0', u' ')+'\n')
    cnt += 1
print('\r-----Done-----')
novel_file.close()