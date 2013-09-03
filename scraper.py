from bs4 import BeautifulSoup
from googlevoice import Voice
import urllib2, os,urllib, traceback, send_email

''' Sample query url for cs70 spring 2014
http://osoc.berkeley.edu/OSOC/osoc?y=0&p_term=SP&p_deptname=Computer+Science&p_course=70 
'''
TEMPLATE_URL = "http://osoc.berkeley.edu/OSOC/osoc?y=0&p_term={0}&p_deptname={1}&p_course={2}"
MAPPINGS = {"DIS":"Discussion Section","LAB":"Lab"} 

def gen_url(department,course,semester="FL"):
   department = ' '.join(department.split()).replace(" ","+") #strips extra spaces, replaces spaces with + 
   return TEMPLATE_URL.format(semester,department,course) 

def return_live_course_size(ccn): 
      try: 
         url = "https://telebears.berkeley.edu/enrollment-osoc/osc"
         values = {'_InField2':str(ccn),'_InField3':'13D2'}
         data = urllib.urlencode(values) 
         req = urllib2.Request(url,data) 
         response = urllib2.urlopen(req)  
         html = response.read()
         soup = BeautifulSoup(html) 
         blockquote = soup.find('blockquote')
         sizes = [0 for i in range(4)] 
         results = blockquote.find('div').text.encode('utf-8').strip().split() 
         index = 0
         for word in results:
             try: 
                 val = int(word) 
                 sizes[index] = val 
                 index += 1
             except Exception as e:
                 pass
         return {'class size':sizes[1], 'curr size': sizes[0], 'avail seats':sizes[1] - sizes[0],'waitlist limit':sizes[2],'waitlist size':sizes[3]} 
      except AttributeError as a:
          print ccn

def nice_print(dictionary):
    for key in dictionary:
        print "{0}:  {1}".format(key,dictionary[key]) 

def scrape_course_info(url):
    html = urllib2.urlopen(url).read() 
    soup = BeautifulSoup(html) 
    output_dict = {} 
    search_results = soup.find_all('table')[1:-1] 
    for each in search_results:
        class_details = each.text.encode('utf-8').strip().replace("\xc2\xa0","").split("\n")
        result_dict = {}
        for field in class_details:
            if field.split(":")[1]:
                result_dict[field.split(":")[0].lower()] = field.split(":")[1].lower().strip()
        result_dict['enrollment info'] = return_live_course_size(int(result_dict['course control number']))
        output_dict[result_dict["course"]] = result_dict 
    return output_dict

