
import glob
import pandas as pd
import sqlalchemy as sqla
import MySQLdb
import fileinput
import datetime
import traceback

c_input_dir="/Users/jmangalampalli/Desktop/intuit/"
c_log_file="/Users/jmangalampalli/Desktop/intuit/job.log"
file_lists=['4 Data Team - Browser_Sample.csv','4 Data Team - OperatingSystem_Sample2.csv','4 Data Team - ClickStream_Sample.csv']

c_browser_col=2
c_os_col=2
c_click_col=13



c_browser_query = "INSERT INTO d_browser (browser_id, browser_name, major_browser,created_at,updated_at) VALUES(%s, %s, %s,%s,%s) ON DUPLICATE KEY UPDATE browser_name=%s, major_browser=%s,updated_at=%s;"
c_os_query = "INSERT INTO d_os (operating_system_id, operating_system, major_os,created_at,updated_at) VALUES(%s, %s, %s,%s,%s) ON DUPLICATE KEY UPDATE operating_system=%s, major_os=%s,updated_at=%s;"
c_click_query = "INSERT INTO f_page_events (trans_id,visitor_id,user_agent_id,browser_id,operating_system_id,resolution_id,hit_date_id,visit_num,page_event,referrer_id,duration_on_page,load_date) VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ;"
c_referrer_query = "INSERT INTO d_referrer ( referrer, created_at,updated_at) VALUES(%s, %s, %s)"
c_referrer_select_query = "select referrer_id  from d_referrer where referrer=%s"
c_user_agent_query = "INSERT INTO d_user_agent (user_agent_id,user_agent,created_at,updated_at) VALUES(%s,%s,%s,%s) ;"
c_date_query = "INSERT INTO d_date (date_id,created_at,updated_at) VALUES(%s,%s,%s) ;"

def get_files(i_dir):
	files=glob.glob(i_dir+"*.csv")
	return files

def validate_save_browser_data(engine,df):
    if len(df.columns) ==   c_browser_col:
        df['major_browser']=df['browser_name'].str.split(' ',expand=True).ix[:,0:0]
        for index,row in df[(df.browser_name.notnull()&df.browser_id.notnull())].iterrows() :                              
           engine.execute(c_browser_query,row['browser_id'],row['browser_name'],row['major_browser'],datetime.datetime.now(),datetime.datetime.now(),row['browser_name'],row['major_browser'],datetime.datetime.now())
           log_message('Browser',str(row['browser_id']),' inserted') 

def validate_save_os_data(engine,df):
    if len(df.columns) ==   c_os_col:
        df['major_os']=df['operating_system'].str.split(' ',expand=True).ix[:,0:0]
        for index,row in df[(df.operating_system.notnull()&df.operating_system_id.notnull())].iterrows() :                              
           engine.execute(c_os_query,row['operating_system_id'],row['operating_system'],row['major_os'],datetime.datetime.now(),datetime.datetime.now(),row['operating_system'],row['major_os'],datetime.datetime.now())
           log_message('Os',str(row['operating_system_id']),' inserted')    

def save_get_referrer(engine,i_referrer):
    result=engine.execute(c_referrer_select_query,i_referrer)
    if result.rowcount == 1 : 
        return result.fetchone()[0]
    else :  
        engine.execute(c_referrer_query,i_referrer,datetime.datetime.now(),datetime.datetime.now())
        rres=engine.execute("SELECT LAST_INSERT_ID();")
        return rres.fetchone()[0]

def save_user_agent(engine,i_user_agent_id,i_user_agent):
    try:
        result=engine.execute(c_user_agent_query,i_user_agent_id,i_user_agent,datetime.datetime.now(),datetime.datetime.now())
    except MySQLdb.IntegrityError:
        pass
    except Exception, e:
        print traceback.print_exc()
          
def save_date(engine,i_date):
 
    try:
        result=engine.execute(c_date_query,i_date,datetime.datetime.now(),datetime.datetime.now())
    except Exception, e:
        print traceback.print_exc()

def validate_save_click_data(engine,df):
    if len(df.columns) ==   c_click_col:
        df['hit_date_id']=pd.to_datetime(df['hit_timestamp'],errors='coerce').dt.strftime('%Y%m%d')
        df['referrer'].fillna('Unknown',inplace=True)
        df['duration_on_page_seconds'].fillna(0,inplace=True)
        df['visit_num'].fillna(0,inplace=True)
        df['page_event'].fillna(0,inplace=True)
        
        
        for index,row in df.iterrows() : 
            referrer_id=1
            referrer_id=save_get_referrer(engine,row['referrer'])
            save_user_agent(engine,row['user_agent_id'],row['user_agent'])
            save_date(engine,row['hit_date_id'])
            try :
                engine.execute(c_click_query,row['trans_id'],row['visitor_id'],row['user_agent_id'],row['browser_id'],row['operating_system_id'],row['resolution_id'],
                row['hit_date_id'],row['visit_num'],row['page_event'],referrer_id,row['duration_on_page_seconds'],row['load_date'])
                log_message('Click',str(row['trans_id']),' inserted')  
            except Exception, e:
                #log_message('Click',str(row['trans_id']),' Error inserting row' +traceback.print_exc()) 
                traceback.print_exc()


def log_message(source,key,message):
    global log
    log.write(source+'-'+key+'-'+message+"\n")
	



def main():
    try :
        global log
        log =open(c_log_file,'w')
        log_message('Job Start',str(datetime.datetime.now()),'') 
       
    
        
        engine_str = 'mysql+pymysql://root:''@127.0.0.1:3306/mydb'
        engine = sqla.create_engine(engine_str, echo=False, encoding='utf-8')
        
        for file in file_lists:
            df=pd.read_csv(file)
            if df.empty : continue
            if (file.find("Browser") != -1) :
                log_message(file,str(datetime.datetime.now()),'Processing Browser data '+str(df['browser_id'].count())) 
                validate_save_browser_data(engine,df)
            elif file.find("Operating") != -1:
                log_message(file,str(datetime.datetime.now()),'Processing Os data '+str(df['operating_system_id'].count()) )
                validate_save_os_data(engine,df)
            elif file.find("Click") != -1:
                log_message(file,str(datetime.datetime.now()),'Processing Clickstream data '+str(df['trans_id'].count()) )
                validate_save_click_data(engine,df)
            else:
                log_message(file,str(datetime.datetime.now()),'Unknown file type') 
        log_message('Job End',str(datetime.datetime.now()),'') 
    except Exception,e:
        traceback.print_exc()
    finally:
     
        log.close()
     
if __name__=='__main__' : main()


