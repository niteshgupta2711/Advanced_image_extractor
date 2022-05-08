from datetime import datetime
import os

from selenium import webdriver
import time
import logging
import urllib
import urllib.request
from io import BytesIO
import io
from PIL import Image
def image_to_byte_array(image: Image) -> bytes:
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format="PNG")
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr
def resize(readable,size=(224,224)):
    #response.read()

    img = Image.open(BytesIO(readable))
    
    img=img.resize(size,resample=Image.LANCZOS)
    #kl=image_to_byte_array(img)
    # with open('pn.png','wb') as f:
    #     f.write(kl)
    return img
 
def fetch_image_urls(query: str,max_links_to_fetch :int,wd: webdriver,sleep_between_interactions=0.5):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)
    search_url="https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(search_url.format(q=query))
    image_urls=set()
    image_count=0
    results_start=0
    while image_count<max_links_to_fetch:
        scroll_to_end(wd)
        thumbnail_results=wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results=len(thumbnail_results)
        logging.info(f'{number_results} Extracting links from {results_start}:{number_results}')
        for img in thumbnail_results[results_start:number_results]:
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue
            actual_images=wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:

                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
            image_count=len(image_urls)
            if len(image_urls)>=max_links_to_fetch:
                logging.info(f'found {len(image_urls)} Images Done')
                print(f'found {len(image_urls)} Images Done')
                break
            else:
                logging.info(f'found {len(image_urls)} finding more ............')
                print(f'found {len(image_urls)} finding more ............')
                time.sleep(0.5)
                load_more_button=wd.find_elements_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click()")
            results_start=len(thumbnail_results)
    return list(image_urls)



def persist_image(path:str,url:str,counter,size):
    try:
        image_content=urllib.request.urlopen(url,timeout=60).read()
    
        img=resize(image_content,size=size)
        imag=image_to_byte_array(img)
    except Exception as E:
        print(E, 'not resized/forbidden')
        return 'forbidden'
    
    try:
        f=open(os.path.join(path,'jpg'+'_'+str(counter)+".jpg"),"wb")
        f.write(imag)
        f.close()
        print(f'saved url to path{path}')
    except Exception as e:
        print(e)


                







def download(searchterm : str,path :str,resize,no_images=10):
    size=resize
    target_folder=os.path.join(path,'_'.join(searchterm.lower().split(' ')))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    with webdriver.Chrome(executable_path='./chromedriver.exe') as wd:
        res=fetch_image_urls(searchterm,no_images,wd=wd,sleep_between_interactions=0.5)
    counter=0
    for element in res:
        
        if not persist_image(target_folder,element,counter,size)=='forbidden':
            counter+=1

if __name__=="__main__":
    download('dogs','datset/cat',(224,224),3)




    # try:
    #     image_content=urllib.request.urlopen(url, timeout=60).read()
    #     print('go the image')
    #     img=resize(image_content,resize)
    #     image_content=image_to_byte_array(img)
    #     print
    # except Exception as E:
    #     print(E)
    #     print('not resized')