from bs4 import BeautifulSoup
import requests, pandas as pd

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

class megaStudyInfo:
    def __init__(self):
        self.examSeq = [] # 각 학력평가, 모의평가, 수능 고유코드
        self.tabNo = 2 # 수학
        self.selSubCd = [2004, 2005, 2006, 2007, 2008] # 순서대로 가형, 나형, 확통, 미적 기하
        self.selExamType = 1
    
    def getExamSeq(self):
        url = "https://www.megastudy.net/Entinfo/correctRate/main.asp"
        req = requests.get(url, headers=header)
        soup = BeautifulSoup(req.content, 'html.parser', from_encoding='utf-8')
        tmp = soup.find("ul", {"id": "examNmArea"}).find_all("li")
        for i in tmp:
            self.examSeq.append(str(i.attrs["onclick"][14:17]))
        self.examSeq.reverse()
    
    def getRateInfo(self):
        self.getExamSeq()
        for i in range(1):
            for j in range(1):
                url = f"https://www.megastudy.net/Entinfo/correctRate/main_rate_ax.asp?examSeq={self.examSeq[i]}&tabNo=2&selSubCd={self.selSubCd[j]}&selExamType=1"
                req = requests.get(url, headers=header)
                soup = BeautifulSoup(req.content, 'html.parser', from_encoding='utf-8')
                testName = soup.find("h4", {"class": "areaLogo colorBlue"}).text
                #rate = soup.find("table", {"class": "tb_basic"})
                df = pd.read_html(url, encoding='cp949')
                df[0].to_csv('test.csv', index=False, encoding='cp949')
                #print(df[0])


megaStudy = megaStudyInfo()
megaStudy.getRateInfo()
