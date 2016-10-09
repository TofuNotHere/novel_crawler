from urllib import request
from bs4 import BeautifulSoup
import threading
import time
import sys,math

ress = []
all = 0
lock = threading.Lock()
lenn = 0
class NovelDownLoader(threading.Thread):
    def __init__(self,nu,pice,code,name_link_list):
        threading.Thread.__init__(self)
        self.novel_url = 'http://www.00ksw.com/html/' + str(int(int(code)/1000))+ '/' + code
        self.nu = nu
        self.name_link_list = name_link_list
        self.pice = pice

    def input(self,novel_code):
        self.novel_code = novel_code

    def run(self):
        global all
        res = []
        cnt = 0
        for var in self.name_link_list:
            cnt += 1
            novel_text_url = self.novel_url +'/'+ var[1]
            try:
                htmldoc = request.urlopen(novel_text_url)
            except:
                print(self.pice*self.nu + cnt ,'章出现异常，已跳过')
                continue
            soup = BeautifulSoup(htmldoc.read().decode('gbk'),"html.parser")
            res += ['\n' + var[0] + '\n' + str(soup.find('div',id = 'content')).replace('<br/><br/>',u'\n')[18:-6].replace(u'\xa0', u' ')+'\n']
            if lock.acquire():
                all += 1
                lock.release()
        ress[self.nu] = res



class Draw(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def progressbar(self,cur, total):
        percent = '{:.2%}'.format(cur / total)
        sys.stdout.write('\r')
        sys.stdout.write("[%-50s] %s" % (
                                '=' * int(math.floor(cur * 50 / total)),
                                percent))
        sys.stdout.flush()

    def run(self):
        global  all
        li = 0
        while li != lenn:
            if lock.acquire():
                li = all
                lock.release()
            self.progressbar(li,lenn)
            time.sleep(0.2)


def startDown():
    global lenn
    novel_url = 'http://www.00ksw.com/html/'
    code = input("input the num of novel\n")
    novel_url += str(int(int(code)/1000))+ '/' + code
    try:
        htmldoc = request.urlopen(novel_url)
        soup = BeautifulSoup(htmldoc.read().decode('gbk'),"html.parser")
        print('《' + soup.h1.string +'》')
        print(soup.find('div',id='info').p.string.replace(u'\xa0', u''))
        dd_list = soup.find_all('dd')
        name_link_list = list(map(lambda var:(var.a.get_text(),var.a['href']),dd_list))
        print('本书共有',len(name_link_list),'章')
        pice = int(len(name_link_list)/8)
        lenn = len(name_link_list)
        threadList = []
        for i in range(0,len(name_link_list),pice):
            #print(i,i+pice)
            ress.append([])
            nd = NovelDownLoader(int(i/pice),pice,code,name_link_list[i:i+pice])
            threadList.append(nd)
        start = time.time()
        print("下载中...")
        threadList.append(Draw())
        for var in threadList:
            var.start()
        for var in threadList:
            var.join()

        novel_file = open(soup.h1.string+'.txt','w')
        for var in ress:
            for tex in var:
                novel_file.write(tex)
        novel_file.close()
        print('\n耗时{:.2}s'.format(time.time() - start))
    except:
        print("\n404?")

if __name__ == '__main__':
    startDown()
