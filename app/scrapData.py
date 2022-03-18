from google.cloud import storage
import uuid
from bs4 import *
import requests
import re
from app.taskGenerator import create_task

def sentUrl(uid,url):
    #url ="https://hackernoon.com/the-fastest-way-to-invoke-a-httprest-url-from-an-aws-lambda"
    if "https://hackernoon.com" in url:
        if len(url.split('.com/'))==2:
            r = requests.get(url)
            
            soup = BeautifulSoup(r.text,'html.parser').select('body')[0]
            print(soup.find('div',{'class':'youtube-container'}))
            try:
                title = soup.find('footer').clear()
            except:
                pass
            try:
                title = soup.find('div',{'class':'info'}).clear()
            except:
                pass
            try:
                title = soup.find('div',{'class':'Profile__Layout-sc-1j6ysg0-0 eVxkPD profile'}).clear()
            except:
                pass
            try:
                element = soup.find('div',{'class':'Container-sc-11afu3a-0 Story__Layout-sc-1k5ahq9-0 tZwSj iVmyGl'})
                paragraphs = []
                # Iterate through all tags
                for tag in element.find_all():
                    if tag.name == "p":
                        pattern = r'([\d*])([:])'
                        if re.search(pattern,tag.text):
                            tag.clear()
                            tag.find_next_sibling('p').clear()
                            element.clear()
                            return "Video Content..."
                        else:
                            if re.search(r'((https://)|(www.)|(/)|(.html))',tag.text):
                                tag.clear()
                            paragraphs.append(tag.text)
                listTostr = ' '.join([str(ele) for ele in paragraphs])
                text = ' '.join([line for line in listTostr.split('\n') if line.strip() != ''])
                text_filter = re.sub(r'\[\w*\]|\(((/).*?)\)',' ',text)
                text_summerized = re.sub(r'\.','. ',text_filter)
                #print(text_summerized)
                ###### GC File create with a Bucket ###########
                fName = str(uuid.uuid4())    
                client = storage.Client()
                bucket = client.get_bucket('mydemo-bucket-ts')
                new_blob = bucket.blob(f'remote/hackernoon/{fName}.txt')
                new_blob.upload_from_string(text_summerized)
                print('Upload successfully')
                #### create task here ######
                create_task(uid=uid,url=url,payload=text_summerized)
                #################################################
                return text_summerized
            except:
                pass
