import requests
import re
import lxml
from bs4 import BeautifulSoup
class BiliBarrage(object):

    def __init__(self,av_num,path):
        self.av_num = av_num
        self.av_url = "https://www.bilibili.com/video/av"+ av_num
        self.path = path + av_num + ".txt" 
        self.headers = {    
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"}

    
    def get_cid_url(self):
        api_url = "https://api.bilibili.com/x/web-interface/view?aid=" + av_num
        try:
            a = requests.get(api_url)
            a.raise_for_status()  #状态码如果不是200，则引发异常
            a.encoding = "utf-8"
        except:
            print("获取url失败")  
        #print(a.text)
        cid = re.findall(r"\"pages\"\:\[\{\"cid\":(.*?)\,",a.text)[0] #正则表达式提取cid
        #print("cid:"+cid +"\n cid获取完成")
        cid_url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(cid)#格式化cid并合并成url
        #print(cid_url)
        return cid_url
      

    def get_barrage(self,cid_url):
        try:
            bar = requests.get(cid_url)
            bar.encoding  = "utf-8"
        except:
            print("获取弹幕失败")
        print(bar.text)
        barrage = BeautifulSoup(bar.text)
        #print(barrage.d.string)
        text = [] #创建一个列表来储存弹幕
        for d in barrage.find_all(name = 'd'):
            #print(d.text)
            text.append(d.text) #把弹幕逐行加入列表
        print("获取弹幕成功")
        return text            
    
    
    def get_video_url(self):
        #av_url = "https://www.bilibili.com/video/av"+ av_num
        try:
            au = requests.get(self.av_url)
            au.raise_for_status()
            au.encoding = "utf-8"
            print(au.text)
        except:
            print("获取url失败")
        vu = re.findall(r"\"baseUrl\"\:\"(.*?)\"",au.text)[0]
        print(vu)
        return vu



       
    def save(self,path,av_num,barrage):
        f = open(path,'w',encoding = "utf-8")
        try:
            f.write(" \n ".join(barrage)) #这里要把列表转换为字符串（str），并换行写出
            f.close()
            print("写入弹幕文件成功")
        except Exception:
            print("写入错误")
     
        
    def run(self):
        cu = b.get_cid_url()
        ba = b.get_barrage(cu)
        print (ba)
        self.save(self.path,self.av_num,ba)
        gv = b.get_video_url()


if __name__ == '__main__':
    path = input("输入路径,例：  D:\\abc\ ")
    av_num = input("输入av号:")
    b = BiliBarrage(av_num,path)
    b.run()
            
        
    