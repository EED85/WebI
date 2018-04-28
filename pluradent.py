##This programm will read out article numbers from the pluradent webshop
#
#
##import libraries
#import requests
#requests.__file__
#import bs4
#bs4.__file__
#from bs4 import BeautifulSoup
#
##main function
#def main(web = 1):
#    #returns 1, if no error
#    if web == 1:
#        print("web1")
#        url = 'https://shop.pluradent.de/praxisbedarf.html'
#    else:
#        print("web0")
#        url = 'n.a.'
#    
#    print(url)
#    print("Importing web site by using requests.get method")
#    r = requests.get(url)
#    return "1"
#
#L = main(1)
#print(L)



#developing area

import requests
requests.__file__
import bs4
bs4.__file__
from bs4 import BeautifulSoup
import pandas
import os
import re

#reading website
#cd "C:/Users/ericb/EED-Solutions by Eric Brahmann/Ideal Dental - Code/webI/"

url = 'https://shop.pluradent.de/praxisbedarf.html'
r = requests.get(url)
c = r.content
soup = BeautifulSoup(c,"html.parser")


#exporting website to txt
with open('url.txt','w') as f:
    f.write(str(c))

with open('url_soup.txt','w') as f:
    f.write(str(soup))







#-----------------------------------------------------------------------------
#Kategorie Level 0 (right now only info - is not used yet)
#---------------------------------------------------------------------
all_main_cat = soup.find_all("a",{"class":"level-top"})
I = 0
for item in all_main_cat:
    I = I +1
    print (I)
    label = item.find_all("span",{"class":"label"})
    try:
        is_cat = 1
        cat = label[0].text
    except:
        is_cat = 0
        cat = ''
    if is_cat == 1:
        print(cat)
        
#-----------------------------------------------------------------------------
#Kategorie Level 1
#---------------------------------------------------------------------
all_subcat = soup.find_all("div",{"class":"category-teasers--wrapper--teaser--content--subcategories mouse-over"})  

l = []
l2 = []
I = 0
for item in all_subcat:
    I = I +1
    print(I,item.text)
    print(item)
    sublinks = item.find_all("a")
    J = 0
    for  link in sublinks:
        if I >= 1:
            d={}
            J = J +1
            print (J)
            has_link = link.has_attr('href')
            print('Hat link',has_link)
            if link.has_attr('href'):
                print (link.text,link['href'])
                d["index"] = I
                d["index2"] = J
                d["url"] = link['href']
                d["Kategorie - Level0"] = "Praxisbedarf"
                d["Kategorie - Level1"] = link.text
                d["Kategorie - Level2"] = ""
                
                l.append(d)
        elif I == 0:
            print('')
#            d2 = {}
#            d2["index"] = I
#            d2["index2"] = J
#            d2["Kategorie"] = link.text 
#            d2["url"] = ""
#            l2.append(d)
#exporting            
df1 = pandas.DataFrame(l)
df1.to_csv('Kategorie - Level1.csv') 

#-----------------------------------------------------------------------------
#Kategorie Level 2
#---------------------------------------------------------------------


I = 0
l = []

for index,row in df1.iterrows():
     I = I+1
     
     if I != 0:
         print ("I=",I," / ", row["Kategorie - Level1"])
         print (row["url"])
         url = row["url"]
         r2 = requests.get(url)
         c2 = r2.content
         soup2 = BeautifulSoup(c2,"html.parser")
#url = 'https://shop.pluradent.de/praxisbedarf/praxisinstrumente/instrumente-konservierend.html'         
#r2 = requests.get(url)
#c2 = r2.content
#soup2 = BeautifulSoup(c2,"html.parser")
         url_nohtml = os.path.splitext(url)[0]
         all_subcat2_name = soup2.find_all("a",{"class":"category-subnav--content--list--entry--link"})
         K = 0
         J = 0
         for item in all_subcat2_name:
            K = K+1
            if item["href"].find(url_nohtml) == 0:
                d = {}
                J = J +1
                d["index"] = row["index"]
                d["index2"] = row["index2"]
                d["index3"] = J
                d["Kategorie - Level0"] = row["Kategorie - Level0"]
                d["Kategorie - Level1"] = row["Kategorie - Level1"]
                d["Kategorie - Level2"] = item.text.strip()
                d["url"] = item["href"]
                l.append(d)
#print(l)
df2 = pandas.DataFrame(l)
df2.to_csv('Kategorie - Level2.csv') 


#-----------------------------------------------------------------------------
#Product Level 0 - infos auf der Übersichtsseite
#---------------------------------------------------------------------
I = 0
J = 0
K = 0
l = []
for index,row in df2.iterrows():
     I = I+1
     if row["Kategorie - Level1"] != row["Kategorie - Level2"] and I == 2:
         print ("I=",I,"/", row["Kategorie - Level1"],"/",row["Kategorie - Level2"])
         print (row["url"])
         url = row["url"]

#url = 'https://shop.pluradent.de/praxisbedarf/pluline-qualitaetsprodukte/praxismaterial/abformung.html'
         r3 = requests.get(url)
         c3 = r3.content
         soup3 = BeautifulSoup(c3,"html.parser")

         #count pages
         pages = soup3.find_all("div",{"class":"pages"})
         pages2 = pages[0].find_all("a")
         K = 0
         pagecount = 0
         for page in pages2:
             K= K+1
#             print (page["href"])
#             print (page.text)
             if page.text.isdigit():
                 pagecount = max(int(page.text),pagecount)
         print ("pagecount=", pagecount)



#         for I in range(1,pagecount+1):
         for J in range(1,2):
             
             url_page = url+"?p="+str(J)
             print(url_page)

#read artikelnummer / url image / name / preis
#url_page = 'https://shop.pluradent.de/praxisbedarf/pluline-qualitaetsprodukte/praxismaterial/abformung.html?p=1'
             r4 = requests.get(url_page)
             c4 = r4.content
             soup4 = BeautifulSoup(c4,"html.parser")
             #lists all products
             products = soup4.find_all("div",{"class":"list-product-item"})
             L=0
             for product in products:
                 L=L+1
                 #url to image
                 image = product.find("div",{"class":"list-product-item--image"})
                 url_image=image.find("img")["src"]
                 #artikelnummer
                 sku = product.find("div",{"class":"product-info--sku"})
                 m=re.search('\d+',sku.text)
                 sku = m.group(0)
                 #name+url
                 pr_info = product.find("div",{"class":"product-info"})
                 pr_info_a = pr_info.find("a")
                 product_name=pr_info_a["title"]
                 product_url=pr_info_a["href"]
                 d = {}
                 d["index"] = row["index"]
                 d["index2"] = row["index2"]
                 d["index3"] = row["index3"]
                 d["index4"] = L
                 d["Kategorie - Level0"] = row["Kategorie - Level0"]
                 d["Kategorie - Level1"] = row["Kategorie - Level1"]
                 d["Kategorie - Level2"] = row["Kategorie - Level2"]
                 d["Artikelnummer"] = sku
                 d["url image"] = url_image
                 d["url"] = product_url
                 d["Artielbezeichnung"] = product_name
                 l.append(d)
        #price
print(l) 
df3 = pandas.DataFrame(l)
df3.to_csv('Produkt - Level0.csv') 
#        print(name,url)
#preis
#  <div class="product-info--original-price">
#      pr_info.find()
#<div class="product-info--price special-price">
#            Aktionspreis        24,95&nbsp;€</div>
  
#        mame.find("a")
#        name = name["title"]
        #url
        
        
#        "product-info--price "
    
#-----------------------------------------------------------------------------
#Product Level 1 - info von der spezifischen Produktseite
#---------------------------------------------------------------------


#exporting website to txt
with open('url4.txt','w') as f:
    f.write(str(c4))

with open('url_soup4.txt','w') as f:
    f.write(str(soup4))



m = re.search('(?<=abc)def', 'abcdef')
m.group(0)











    
    





    






