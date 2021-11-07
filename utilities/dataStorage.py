from sqlalchemy import create_engine
import pandas as pd

def saveDb(data,table_name):
    engine=create_engine('postgresql://bqocmdsxiegqxh:7a8730d127abacc1abd7087a2b925919df34d388c9cb733a1b240d9309fd7314@ec2-184-73-198-174.compute-1.amazonaws.com:5432/devp0g7010lckj')
    data.to_sql(table_name,engine,if_exists='replace',index=False)
    engine.dispose()
def readData(table_name):
    engine=create_engine('postgresql://bqocmdsxiegqxh:7a8730d127abacc1abd7087a2b925919df34d388c9cb733a1b240d9309fd7314@ec2-184-73-198-174.compute-1.amazonaws.com:5432/devp0g7010lckj')
    con=engine.connect()
    data=pd.read_sql("select * from "+table_name,con)
    con.close()
    engine.dispose()
    return data

