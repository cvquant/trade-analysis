import time
import pytz
import datetime

## @brief Get EST trading date from unix timestamp based on the custom definition
#  Custom Trading date definition :  6PM EST YDAY to 4PM EST TODAY is TODAY
#
def get_custom_est_date_from_unix_timestamp( UTCTime ):
    UTC_date = UTCTime.date( )
    custom_time = datetime.datetime.combine( UTC_date, datetime.time( 17, 0, tzinfo = pytz.timezone( "EST" ) ) ).astimezone( pytz.timezone( 'UTC' ) )
    if custom_time > UTCTime:
        return UTC_date
    else:
        return ( UTC_date + datetime.timedelta( days = 1 ) )

## @brief Get EST reference unix timestamp based on the custom definition
# Custom Trading date definition :  6PM EST YDAY to 4PM EST TODAY is TODAY
#
def get_custom_est_ref_time_from_unix_timestamp( UTCTime ):
    UTC_date = UTCTime.date( )
    custom_time = datetime.datetime.combine( UTC_date, datetime.time( 17, 30, tzinfo = pytz.timezone( "EST" ) ) ).astimezone( pytz.timezone( 'UTC' ) )
    if custom_time > UTCTime:
        new_UTC_date = UTC_date - datetime.timedelta( days = 1 )
        return datetime.datetime.combine( new_UTC_date, datetime.time( 17, 30, tzinfo = pytz.timezone( "EST" ) ) ).astimezone( pytz.timezone( 'UTC' ) )
    else:
        return custom_time

## @brief Given a date, uses our custom trading date definition to return the 
#  start of day unix timestamp corresponding to this trading date
#
def get_custom_est_midnight_time_from_date( this_date ):
    attempt_1 = datetime.datetime.combine( this_date - datetime.timedelta( days = 1 ), datetime.time( 17, 30, tzinfo = pytz.timezone( "EST" ) ) ).astimezone( pytz.timezone( 'UTC' ) )
    return attempt_1  # added to remove warning

## @brief Given a timezone and a hhmm in that timezone,
#  returns the secs from midnight for this hhmm based
#  on our definition of date 
#
def get_secs_from_midnight( this_date, hhmm, tz ):
    utc_datetime = datetime.datetime.combine( this_date, datetime.time( 17, 0, tzinfo = pytz.timezone( "UTC" ) ) )
    hhmmss_utc = utc_datetime.hour * 10000 + utc_datetime.minute * 100 + utc_datetime.second
    return ( ( hhmmss_utc % 100 ) + 60 * ( ( hhmmss_utc / 100 ) % 100 ) + 3600 * ( ( hhmmss_utc / 10000 ) % 100 ) )

def get_custom_est_secs_from_midnight( this_date, hhmm, tz ):
    this_time = datetime.datetime.combine( this_date , datetime.time( int(hhmm / 100), hhmm % 100, tzinfo = tz ) ).astimezone( pytz.timezone( 'UTC' ) )
    custom_est_ref_time = get_custom_est_ref_time_from_unix_timestamp( this_time )
    return ( this_time - custom_est_ref_time ).total_seconds( )

def get_unix_timestamp_from_hhmm_tz( this_date, hhmm, tz ):
    return datetime.datetime.combine( this_date , datetime.time(int(hhmm / 100), hhmm % 100, tzinfo = tz )).astimezone(pytz.timezone('UTC'))
