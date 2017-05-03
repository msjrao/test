
Measures
---------
transactions
duration
visitors


Dim
-----
Date
browser
major browser
operating system
referrer
user agent



Assumption :
- report grain is days , no time
- data has the PK 
- type 1 dimension
- invalid data is rejected
- in click stream data is trans id is unique

------------
Input files
Browser
Os
Click Stream

---------
Browser
- check it has two columns
- validate first column is a number

OS
- check it has two columns
- validate first column is a number

ClickStream
- check it has 13 columns
- trans_id	visitor_id	user_agent_id	browser_id	operating_system_id	resolution_id,visit_num	page_event,duration_on_page_seconds are numbers
- validate hit_timestamp


---------

How many transactions occurred between September 25, 2013 and September 30, 2013 inclusive? 
Note: Each record in the file is one transaction

select count(*)
from mydb.f_page_events
where hit_date_id between 20130925 and 20130930

1487


----------

What is the average length in seconds of all the transactions that occurred between September 25, 2013 and September 30, 2013 inclusive?


select avg(duration_on_page)
from mydb.f_page_events
where hit_date_id between 20130925 and 20130930

48.8209
---------------
•	How many unique visitors used the Chrome browser (any version)? 
Note: One visitor may have multiple transactions in the file.



select count(distinct visitor_id)
from mydb.f_page_events, mydb.d_browser
where mydb.f_page_events.browser_id=mydb.d_browser.browser_id
and mydb.d_browser.major_browser='Chrome'

1972

----------------
•	What was the most used operating system & browser combination for all dates included in the clickstream data?


select mydb.d_browser.major_browser,mydb.d_os.major_os,count(*)
from mydb.f_page_events, mydb.d_browser,mydb.d_os
where mydb.f_page_events.browser_id=mydb.d_browser.browser_id
and mydb.f_page_events.operating_system_id=mydb.d_os.operating_system_id
group by mydb.d_browser.major_browser,mydb.d_os.major_os
order by 3 desc

'Chrome','Android','1784'

------------------

•	How many transactions were done using the Macintosh operating system? 
Note: Use only the data contained in the clickstream file in the query. The result of the query should be one row.


select count(*)
from mydb.f_page_events,mydb.d_os
where mydb.f_page_events.operating_system_id=mydb.d_os.operating_system_id
and mydb.d_os.major_os='OS X'

870

-----------------
How many unique visitors had transactions per day per major browser? 
For example, for "Chrome 28.7”, the major browser would be "Chrome



select mydb.f_page_events.hit_date_id,mydb.d_browser.major_browser,count(distinct visitor_id)
from mydb.f_page_events,mydb.d_browser
where mydb.f_page_events.browser_id=mydb.d_browser.browser_id
group by mydb.f_page_events.hit_date_id,mydb.d_browser.major_browser


'20130916','Chrome','14'
'20130916','Firefox','10'
'20130916','Opera','22'
'20130917','Chrome','38'
'20130917','Firefox','11'
'20130917','Opera','34'
'20130918','Chrome','20'
'20130918','Edge','3'


