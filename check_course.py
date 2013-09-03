import scraper 
import time
import threading
from httplib import BadStatusLine
import send_email
class_info = {}
def nice_print(dictionary):
    for key in dictionary:
        print "{0}:  {1}".format(key,dictionary[key]) 

def check_for_changes(FieldName="enrollment info"):
    global class_info
    print("Ran")
    try: 
        new_class_info = scraper.scrape_course_info(scraper.gen_url("computer science", "61a")) 
        intersection =  set(new_class_info.keys()) - set(class_info.keys());
        if (intersection):
            print("\a")
            print("new classes ha been added to course!") 
            for each in intersection:
                nice_print(new_class_info[each])   
                result_dict = new_class_info[each]
                if result_dict['enrollment info'] and int(result_dict['enrollment info']['avail seats']) > 0:
                    send_email.send_email(str(result_dict), "vaishaal@g    mail.com", "FOUND ROOM IN COURSE: " + each)

        for key in new_class_info:
            if new_class_info[key][FieldName] != class_info[key][FieldName]:
                print "{0} has changed its {1}".format(key,FieldName) 
                print "Old class:" 
                nice_print(class_info[key])
                print "New class:" 
                nice_print(new_class_info[key])

    except KeyError:
        print("Thats not a valid key silly!") 
    class_info = new_class_info
    timer = threading.Timer(1.0,check_for_changes)
    timer.start()

timer = threading.Timer(1.0,check_for_changes) 
timer.start()
