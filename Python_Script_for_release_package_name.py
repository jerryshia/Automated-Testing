from bs4 import BeautifulSoup  
import pandas as pd  
import requests  
import argparse  
from collections import OrderedDict 
from datetime import datetime 
  
class AzureScraper:  
    def __init__(self, language):  
        # 初始化实例变量  
        self.language = language  
        # 格式化URL地址  
        self.current_year = datetime.now().year
        self.current_month_fullname = datetime.now().strftime('%m')
        # self.url = "https://azure.github.io/azure-sdk/releases/2024-05/{}.html".format(self.language) 
        self.url = "https://azure.github.io/azure-sdk/releases/{}-{}/python.html".format(self.current_year, self.current_month_fullname, self.language) 
        # 发送GET请求  
        self.response = requests.get(self.url)  
        # 使用BeautifulSoup解析HTML内容  
        self.soup = BeautifulSoup(self.response.content, 'html.parser')  
        # 初始化ids和extracted_values列表  
        self.ids = []  
        self.extracted_values = []  
  
    def scrape(self):  
        # 找到所有的h3标签并获取他们的文本  
        h3_tags = self.soup.find_all('h3')  
        self.ids = [tag.text for tag in h3_tags if tag.text is not None]  
        # 删除以"Resource Management"开头的id  
        self.ids = [id for id in self.ids if not id.startswith('Resource Management')]  
        # 提取每个id中的某部分  
        for id in self.ids:  
            last_dash_index = id.rfind(' ')  
            second_last_dash_index = id.rfind(' ', 0, last_dash_index)  
            value = id[:second_last_dash_index]  
            self.extracted_values.append(value)  
        # 去除重复的值  
        self.extracted_values = list(OrderedDict.fromkeys(self.extracted_values))  
  
    def to_excel(self):  
        # 创建一个pandas的DataFrame  
        df = pd.DataFrame(self.extracted_values, columns=['azure-sdk-package'])  
        # 将数据输出到Excel表格中  
        df.to_excel('output.xlsx', index=False)  
  
def main():  
    # 创建命令行参数解析器  
    parser = argparse.ArgumentParser(description="Get a language for url")  
    parser.add_argument('language', type=str, help="Language to be placed in the URL")  
    # 解析命令行参数  
    args = parser.parse_args()  
    # 创建AzureScraper实例  
    scraper = AzureScraper(args.language)  
    # 执行抓取操作  
    scraper.scrape()  
    # 将结果保存到Excel文件中  
    scraper.to_excel()  
  
# 当脚本作为主程序运行时，执行main函数  
if __name__ == "__main__":  
    main()  
