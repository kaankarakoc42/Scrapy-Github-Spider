import scrapy
from json import dump
from ast import literal_eval
from ..items import UserItem

class GithubSpider(scrapy.Spider):
    
    name = "github"
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.username = kwargs.get("username")
        self.usernames = kwargs.get("usernames")
        self.output = kwargs.get("output")
        self.extraItems = False
        self.url="https://github.com/{}?tab=repositories"
        if self.username:
           self.urls=[self.url.format(self.username)]
        
        elif self.usernames:
             self.urls=[]
             self.extraItems=True
             self.usernames=literal_eval(self.usernames.replace("'",'"'))
             for user in self.usernames:
                 self.urls.append(self.url.format(user)) 
                 
        else:
            raise ValueError("No usernames given")
        
        if not self.output:
           self.output = "github.json"

    def start_requests(self):
        for url in range(len(self.urls)):
            self.index=url
            yield scrapy.Request(url=self.urls[url], callback=self.parse)
    
    def getTopics(self):
        return self.state.css("div[class*=topics] a::text").getall()

    def getLangs(self):
        lang = self.state.xpath(".//div[4]/span[1]/span[2]/text()").getall()
        if lang:
            return lang
        else:
            return self.state.xpath(".//div[3]/span/span[2]/text()").getall()
        
    def getDesc(self):
        return self.state.xpath(".//div[2]/p/text()").getall()
    
    def xp(self,xp):
        return  self.response.xpath(xp)
    
    def parse(self, response):
        self.response=response
        repos = self.xp("//div[@id='user-repositories-list']/ul/li/div")
        username = self.xp('//*[@id="js-pjax-container"]/div[2]/div/div[1]/div/div[2]/div[2]/h1/span[2]/text()').get()
        name = self.xp('//*[@id="js-pjax-container"]/div[2]/div/div[1]/div/div[2]/div[2]/h1/span[1]/text()').get()
        pp = self.xp('//*[@id="js-pjax-container"]/div[2]/div/div[1]/div/div[2]/div[1]/a/img/@src').get()
        userinfos = self.xp("//div[@class='js-profile-editable-area d-flex flex-column d-md-block']/div[2]/div/a/span/text()").getall()
        userbio = self.xp("//div[@class='p-note user-profile-bio mb-3 js-user-profile-bio f4']/div/text()").get()
        reponames = repos.xpath(".//div[1]/h3/a/text()").getall()
        repoList = []
        for i in range(len(reponames)):
            self.state=self.response.xpath("//div[@id='user-repositories-list']/ul/li[$i]/div",i=i+1)
            repoList.append({
                 "repo":reponames[i],
                 "desc":self.getDesc(),
                 "topics":self.getTopics(),
                 "langs":self.getLangs()
            })
        yield UserItem(
            username=username,
            name=name,
            followers=userinfos[0],
            follows=userinfos[1],
            stars=userinfos[2],
            userbio=userbio,
            repo_count=len(reponames),
            pp=pp,
            repos=repoList
        )
        
        #with open(self.output,"w",encoding="utf8") as file:
             #file.write(dump(item,file,indent=4,ensure_ascii=False))
        
       