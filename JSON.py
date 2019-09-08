import json
import os.path
import datetime
from collections import OrderedDict
from sortedcontainers import SortedDict
import os

class JsonHandler:
        
    def add(self,text_entry,date_entry):
        if not os.path.isfile('customer_list.json'): 
            with open('customer_list.json', 'w')as f:
                key=str(date_entry)
                list=text_entry
                dictionary={}
                dictionary.setdefault(key,list)
                f.write(json.dumps(dictionary))
        else:
            key=str(date_entry)
            list=text_entry
            dictionary={}
            with open('customer_list.json')as f:
                feeds = json.load(f)
                for k, v in feeds.items():
                    if date_entry == k:
                        v=v+text_entry
                        dictionary.setdefault(k,v)
                        feeds.update(dictionary)
                        with open('customer_list.json', 'w') as f:
                            f.write(json.dumps(feeds))            
                dictionary.setdefault(key,list)
                feeds.update(dictionary)
                with open('customer_list.json', 'w') as f:
                    f.write(json.dumps(feeds))


    def search_values(self,date_entry):
        with open('customer_list.json')as f:
                data = json.load(f)
                for key, values in data.items():
                    if key==date_entry:
                        return values        
                return False

    def search_date(self,date_entry):
        with open('customer_list.json')as f:
                data = json.load(f)
                if date_entry in data:
                    return date_entry
                else:
                    return False

    def delete(self, task_current , list_of_values,date_assagn):
        list_of_values.remove(task_current)
        new_dict={date_assagn:list_of_values}
        with open('customer_list.json') as f:
            data = json.load(f)
        data.update(new_dict)
        with open('customer_list.json','w') as f:
            f.write(json.dumps(data))

    def delete_all(self,intended_data):
        with open('customer_list.json') as f:
            data = json.load(f)
        if len(data)!=1:
            del data[intended_data]
            with open('customer_list.json','w') as f:
                f.write(json.dumps(data))
        else:
            with open ("customer_list.json" , "r+") as f:
                f.seek(0)
                f.close()
                os.unlink('customer_list.json')

    def show_all_task(self):
        if not os.path.isfile('customer_list.json'): 
            return False
        else:
            with open('customer_list.json') as f:
                data = json.load(f)
                return data

    def show_sort_day_task(self):
        if not os.path.isfile('customer_list.json'): 
            return False
        else:
            with open('customer_list.json') as f:
                data = json.load(f)
                sort_date=SortedDict(data)
                for line in f:
                    sort_date += line.split(']')
                return sort_date

    def date_menu(self):
        list_date=[]
        if not os.path.isfile('customer_list.json'):
            # with open('customer_list.json', 'w') as f:
            #     data = json.load(f)
            return list_date
        else:
            with open('customer_list.json') as f:
                data = json.load(f)
                for key, values in data.items():
                    list_date.append(key)
                return list_date

    def compare_select_list(self,date_assagn):
        date=[]
        if not os.path.isfile('customer_list.json'):
            return date
        else:
            with open('customer_list.json')as f:
                data = json.load(f)
                for key, values in data.items():
                    if date_assagn==key:
                        date=values
                        return date






