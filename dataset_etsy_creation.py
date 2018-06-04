# -*- coding: utf-8 -*-
"""
Created on Thu May 10 11:00:49 2018

@author: raghudr
"""

import json
import urllib
from googletrans import Translator
import codecs
import os
os.chdir('C:/Users/HP800/Desktop/proj/esty_dataset')


from glob import glob

'''
with open('0000.json', 'r') as f:
    listings = json.load(f)
    f.close()

count=0
'''
  
translator = Translator()

for json_file in glob('C:/Users/HP800/Desktop/proj/listings/*.json'):
#for json_file in os.listdir('C:/Users/HP800/Desktop/proj/listings'):
    #create json object
    data =[]
    filename=[]
    print(json_file)
    with open(json_file, 'r') as f:
        listings = json.load(f)
        
        for items in listings:
            try:
                product={}
                image=items['Images'][0]['url_170x135']
                product['image']=image
                title=items['title']
                product['title']=title
                materials=items['materials']
                product['materials']=materials
                tags=items['tags']
                product['tags']=tags
                #@count=count+1
                #print(image)
                ImageUrl = image.split("//")
                ImageName = ImageUrl[1].split("/")
                print(ImageName[-1])
                urllib.request.urlretrieve(image, ImageName[-1])
                # The target language
                target = 'fr'
                #Translates some text into french
                Translated_text_french=translator.translate(title, dest=target).text
                # The target language
                target = 'hi'
                #Translates some text into hindi
                Translated_text_hindi=translator.translate(title, dest=target).text
                t = codecs.open('C:/Users/HP800/Desktop/proj/esty_dataset/text/'+ImageName[-1]+'.txt',encoding='utf-8', mode='a+')
                t.writelines("english"+" "+title)
                t.writelines("\n")
                t.writelines("french"+" "+Translated_text_french)
                t.writelines("\n")
                t.writelines("hindi"+" "+Translated_text_hindi)
                t.close()


            except:
                pass
            
    f.close()            
            
            
            #data.append(product)
            
        #json_data = json.dumps(data)    
            
    #with open('esty_dataset/etsy_'+str(json_file.split('\\')[1]), 'w') as f:
        #json.dump(json_data, f)
     
