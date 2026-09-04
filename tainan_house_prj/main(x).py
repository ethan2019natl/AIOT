# 載入所需套件工具

# 處理路徑 載入.env檔案的變數到os.environ
from sqlalchemy.util import preloaded  #(注意!!!此行AI建議先移除,有發生 error再行加入)
import os

# 紀錄程式執行過程 log
import logging

# 向server提出請求
import requests as rq

# 處理資料
import pandas as pd
from sqlalchemy import create_engine, text  # DB engine

# 連線mysql
import pymysql

# excel驅動
import openpyxl

# 處理url
import urllib3
from dotenv import load_dotenv # 抓取.env資料

# 1. 載入.env檔案內容 into 環境變數
load_dotenv()  # 載入.env檔案內容 into 環境變數, 之後os.environ[]就可以讀取到變數內容

# 2. 設定log機制(看要 純寫到file 或是 輸出到終端機上)
logging.basicConfig(
    # log等級 設定記錄層級
    level=logging.INFO,                 
    # log格式
    format='%(asctime)s  [%(levelname)s]  %(filename)s(行:%(lineno)d: %(message)s)',
    # log時間格式
    datefmt='%Y/%m/%d %H:%M:%S',
    # log輸出位置
    handlers=[
        logging.FileHandler( "scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]  
)



# 3. 環境變數管理
# 使用os.environ[]來讀取.env檔案內容
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "peter")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "[AAaabbbb@012]")
DB_PORT = os.environ.get("DB_PORT", 3306)
DB_NAME = os.environ.get("DB_NAME", "tainan")
DB_CHARSET = os.environ.get("DB_CHARSET", "utf8mb4")

API_URL = os.environ.get("API_URL")
EXCEL_FILENAME = os.environ.get("EXCEL_FILENAME", "tainan_house.xlsx")

# 4.要透過API去抓資料需要API
# opendata 需key/token/auth
# 不需 http://google.com ? q=python
def fetch_data(api_url, params=None):
        # 檢查api_url
        if not api_url:
            logging.error("API_URL 尚未設定。請檢查 .env 檔案。")
            return None

        try:
            logging.info(f"正在從API獲取資料: {api_url} ")
            # get opendata by API 
            response = rq.get(api_url, params=params, verify=False)
            
            # 檢查回傳狀態
            if response.ok: # 200
                # 轉換資料型態json 轉 python
                data = response.json()
                # 顯示資料筆數 data這個名字是API KEY 裡面定的
                logging.info(f"成功獲取 共計 {len(data.get('data', []))} 筆資料")
                return data
            else:
                logging.warning(f"API回傳狀態碼非200: {response.status_code}")
                return None
        except rq.exceptions.SSLError as ssl_err:
            logging.error(f"SSL憑證驗證失敗，忽略SSL檢查後重試: {ssl_err}")
            return None

        except Exception as error:
            logging.error(f"執行截取時,發生未知錯誤: {error}")
            return None

def save_to_excel(data, filename):
    try:
        # 將資料轉換成pandas的資料型態，excel(2D):dataframe
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine="openpyxl")
        logging.info(f"資料寫入成功:excel {filename}")
    except Exception as e:
        # exc_info=True 會把完整的錯誤訊息trace在log中顯示
        logging.error(f"寫入excel時發生錯誤: {e}", exc_info=True)

def save_to_mysql(data):
    # 建立通道
    conn = None
    # SQL指令物件
    cursor = None
    
    try:
        # 將資料轉換成pandas的資料型態，excel(2D):dataframe
        df = pd.DataFrame(data)
        # 建立資料庫
        logging.info(f"連線至MYSQL ({DB_HOST}:{DB_PORT}) {DB_NAME})檢查資烙庫狀態......")
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            charset=DB_CHARSET,
        )
        cursor = conn.cursor()     
        # 建立資料庫
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET {DB_CHARSET} COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        cursor.close()
        conn.close()
        conn = None
        cursor = None

        db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
        engine = create_engine(db_url)

        # 建立資料表 table
        # 產生通道
        with engine.begin() as sql_conn:
            # 傳遞sql指令
            sql_conn.execute(text('''
            CREATE TABLE IF NOT EXISTS houses(
                Seq BIGINT,
                鄉鎮市區別 TEXT.
                區段數合計 TEXT,
                一般區段數 TEXT,
                繁榮街道路線價區段數 TEXT,
                一般路線價區段數 TEXT,
                一般區段價最高 TEXT,
                一般區段價最低 TEXT,
                最高繁榮街道路線價 TEXT,
                最低繁榮街道路線價 TEXT,
                最高一般路線價 TEXT,
                最低一般路線價 TEXT,
                最高宗地地價數 TEXT,
                最低宗地地價數 TEXT,                
            )   ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci

            '''))
            # 清空table舊資料
            sql_conn.execute(text("TRUNCATE TABLE houses;"))
        logging.info("MySQL 資料表已建立並清空舊資料")    
        
        # 寫入資料
        logging.info("正將資料寫入 MySQL table中")    
        df.to_sql(
            name='houses',
            con=engine,
            if_exists='append',
            index=False,
            chunksize=1000,
            method="multi",
        )
        logging.info(f"資料成功寫入MySQL!")
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        logging.error(f"MYSQL 操作錯誤{e}", exc_info=True) 
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def read_from_excel(filename):
    try:
        df = pd.read_excel(filename, engine="openpyxl")
        logging.info(f"成功讀取excel,共{len(df)}筆資料")
        return df
    except Exception as e:
        logging.error(f"讀取excel失敗: {e}")
        return None

def read_from_mysql(filename):
    try:
        db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
        engine = create_engine(db_url)
        df = pd.read_sql("SELECT * FROM houses", engine)
        logging.info(f"成功讀取Mysql,共{len(df)}筆資料")
        return df
    except Exception as e:
        logging.error(f"讀取Mysql失敗: {e}")
        return None

if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    data = fetch_data(API_URL)

    if data and isinstance(data, dict) and 'data' in data:
        records = data['data']
        
        if records:
            logging.info(f"準備處理{len(records)}筆記錄")
            save_to_excel(records, EXCEL_FILENAME)
            save_to_mysql(records)
       

        

            
        
        


        

            
        
        

 
    

        
            


        

            
        
        


        

            
        
        


 
    

        
            
    
