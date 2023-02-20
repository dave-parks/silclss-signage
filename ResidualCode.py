
    # def convert_to_datetime_format(self, time: str):
    #     now = datetime.datetime.now()
    #     temp = time.split(':')
    #     return now.replace(hour=int(temp[0]), minute=int(temp[1]), second=int(temp[2]))

    # def filter_events(self, timeframe_mins = 15):
    #     now = datetime.datetime.now()
    #     plus_timeframe = now + datetime.timedelta(minutes = timeframe_mins)
    #     idx_to_drop = []
    #     for i in range(self.events.shape[0]):
    #         start_time = self.convert_to_datetime_format(self.events['start'][i])
    #         end_time = self.convert_to_datetime_format(self.events['end'][i])
    #         if (start_time >= now and start_time <= plus_timeframe) or (end_time >= now and end_time <= plus_timeframe):
    #             pass
    #         else:
    #             idx_to_drop.append(i)
        
    #     for i in idx_to_drop:
    #         self.events = self.events.drop(i, axis = 0)  

    
    # def return_events_as_dataframe(self):
    #     return self.events

    # def list_all_categories(self):
    #     print(self.all_categories)

    # def print_events(self, list):
    #     print(self.events)