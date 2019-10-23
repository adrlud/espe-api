import csv
import json
import datetime
import models


#with open('espe_data4.csv', 'r') as f:
 #reader = csv.reader(f)
 #your_list = list(reader)


class Spike:
    your_list = []
    date: datetime
    start_index = 0
    end_index = 0
    readings = []
    
    def __init__(self, hej):
        self.your_list = hej
        
    def median_reading(self):
        median = 0
        i = 0
        self.readings = []
        if self.end_index != 0:
            for item in self.your_list[self.start_index : self.end_index]:
                self.readings.append(float(item['reading']))
                i += 1
            self.readings.sort
            
            median = self.readings[int(i/2)]
        
        else:
            #last spike is runnig median
            for item in self.your_list[self.start_index:]:
                self.readings.append(float(item['reading']))
                i += 1
            
            self.readings.sort
            median = self.readings[int(i/2)]
        
        return median
    
def get_events(x):
    i = 0
    last_reading = 0
    your_list = []
    for item in x:
        if item['reading'] < 100:
            your_list.append({'created_at': item['created_at'], 'reading':0 })
        else:
            your_list.append({'created_at': item['created_at'], 'reading':item['reading']})
    
   
    spikes = [Spike]
    print(your_list)
    for item in your_list:
        reading = float(item['reading'])
        if last_reading == 0 and reading > 0:
            spike = Spike(your_list)
            spike.start_index = i
            spike.date = item['created_at'].__str__()
            spikes.append(spike)
            

        if last_reading > 0 and reading == 0:
            spikes[-1].end_index = i
            

        last_reading = reading
        i += 1

    #remove first item in list
    spikes.remove(spikes[0])

    data = []

    i = 0
    for spike in spikes:
        #print(spike.start_index, spike.end_index)
        if len(spikes) > i + 1:
            diff = spikes[i].median_reading() - spikes[i+1].median_reading()
            #print(diff)
            if 10 < diff < 17:
                data.append({
                    'id': 1,
                    'datetime': spike.date,
                    'count': 1
                })
                #print("Du tog 1 piller: ", spike.date)
            if 22 < diff < 35:
                #print("Du tog 2 piller: ", spike.date)
                data.append({
                    'id': 1,
                    'datetime': spike.date,
                    'count': 2
                })
        
        i += 1
    #print(data)
    
    return data
    
        




