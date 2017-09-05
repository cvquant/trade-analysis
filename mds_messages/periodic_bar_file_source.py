from common_data_structures.periodic_bar import Quote, PeriodicBar
from ctypes import *
from datetime import datetime
from event_processing.external_data_listener import ExternalDataListener
from event_processing.market_book import MarketBook
from utils.datetime_convertor import get_unix_timestamp_from_hhmm_tz

import os
import pytz
import platform

class C_TimeInternal(Structure):
    _fields_ = [("tv_usec", c_int), ("tv_sec", c_int)]


class C_Time(Union):
    _fields_ = [("val", c_ulong), ("time", C_TimeInternal)]


class C_Quote(Structure):
    _fields_ = [('bid_price', c_double), ('bid_size', c_int), ('ask_price', c_double), ('ask_size', c_int)]


class C_PERIODIC_BAR(Structure):
    _fields_ = [('open', C_Quote), ('close', C_Quote), ('low', c_double), ('high', c_double), ('volume', c_ulonglong),
                ('ts', C_Time)]


class PeriodicBarFileSource(ExternalDataListener):
    def __init__(self, shortcode, watch, start_date, end_date, periodic_bar_period=1):
        self.watch = watch
        self.shortcode = shortcode
        self.start_date = start_date  # The date from which this file source should load data
        self.end_date = end_date  # The last date till which this file source should consider data
        self.current_date = start_date  # The date for which csi file source has read the latest struct
        self.current_index = 0
        self.file_reader = None  # The file from which this filesource will read structs
        self.current_quote = None  # The latest read daily_quote (is needed by dispatcher to see the next timestamp of a source)
        self.market_books = MarketBook.GetUniqueInstances(
            watch)  # A pointer to the market book to which the data packets are to be sent

        self.periodic_bars = []
        self.periodic_bar_period = periodic_bar_period

        self.load_data()

        # Set next_event_timestamp_
        if self.current_index < len(self.periodic_bars):
            self.next_event_timestamp = self.periodic_bars[self.current_index].ts
        else:
            self.next_event_timestamp = 0  # Go to passive mode

    def _filesource(self, ticker):
        if platform.system() == 'Windows':
            return os.path.expanduser(r'.\datafiles\{}'.format(ticker))
        else:
            return os.path.expanduser('./datafiles/{}'.format(ticker))

    def load_data(self):
        self.process_etf_data([self._filesource(self.shortcode)])
        self.periodic_bars.sort(key=lambda x: x.ts)

    @staticmethod
    def get_minutebar(filesource):
        output = []
        with open(filesource, 'rb') as file_:
            a = C_PERIODIC_BAR()
            while (file_.readinto(a) == sizeof(C_PERIODIC_BAR)):
                open_ = Quote(a.open.bid_price, a.open.bid_size, a.open.ask_price, a.open.ask_size)
                close_ = Quote(a.close.bid_price, a.close.bid_size, a.close.ask_price, a.close.ask_size)
                ts = datetime.utcfromtimestamp(a.ts.time.tv_sec + a.ts.time.tv_usec / 1000000)
                ts_with_tz = datetime(year=ts.year,
                                      month=ts.month,
                                      day=ts.day,
                                      hour=ts.hour,
                                      minute=ts.minute,
                                      second=ts.second,
                                      tzinfo=pytz.UTC)
                elem = PeriodicBar(open_, close_, a.high, a.low, a.volume, ts_with_tz)
                output.append(elem)

        return output

    ## @brief Make quote objects from futures data
    #  date,product,specific_ticker,open,high,low,close,contract_volume,contract_oi,total_volume,total_oi
    #
    def process_etf_data(self, filesources):
        for filesource in filesources:
            min_bar_list = self.get_minutebar(filesource)
            for minutebar in min_bar_list:
                self.periodic_bars.append(minutebar)

    def seek_to_first_event_after(self, end_time):
        # Go through all the quotes which are timestamped <= end_time
        while ((self.current_index < len(self.periodic_bars)) and
               (self.periodic_bars[self.current_index].ts <= end_time)):
            self.current_index += 1
        if self.current_index < len(self.periodic_bars):  # If there are more events
            source_has_events = True
            self.next_event_timestamp = self.periodic_bars[self.current_index].ts
        else:  # there are no more events
            source_has_events = False
            self.next_event_timestamp = 0  # Go to passive mode
        return source_has_events

    def process_all_events(self):
        # If there are no events, then simply return
        if self.current_index == len(self.periodic_bars):
            self.next_event_timestamp = 0  # Go to passive mode
            return
        # Else process the events
        while self.current_index < len(self.periodic_bars):
            self.next_event_timestamp = self.periodic_bars[self.current_index].ts
            self.watch.on_new_market_event(self.next_event_timestamp)  # Notify the watch first
            # Notify the market book
            self.market_books[0].on_new_minute_bar(self.periodic_bars[self.current_index], self.periodic_bar_period)
            self.current_index += 1
        self.next_event_timestamp = 0  # Since we have processed all events, go to passive mode

    def process_events_till(self, end_time):
        # If there are no events, return
        if self.current_index == len(self.periodic_bars):
            self.next_event_timestamp = 0  # Go to passive mode
            return
        # Go through all the quotes which are timestamped <= end_time
        while (self.current_index < len(self.periodic_bars)) and (self.next_event_timestamp <= end_time):
            self.watch.on_new_market_event(self.next_event_timestamp)  # Notify the watch first
            # Notify the market book
            self.market_books[0].on_new_minute_bar(self, self.periodic_bars[self.current_index],
                                                   self.periodic_bar_period)
            self.current_index += 1
            if self.current_index < len(self.periodic_bars):
                self.next_event_timestamp = self.periodic_bars[self.current_index].ts
        # If there are events
        if self.current_index < len(self.periodic_bars):
            self.next_event_timestamp = self.periodic_bars[self.current_index].ts
        else:  # There are no more events
            self.next_event_timestamp = 0  # Go to passive mode
