
# Flow xu ly crawller va report theo ngay
'''
1. Crawller du lieu tu cac trang web ve
2. Lam sach du lieu & luu vao folder clearned_data
3. Chay nhan dien tich cuc tieu cuc
4. Sync file qua hive
'''

def main():
    from process.crawller import crawller_process
    from process.clean_data import clean_data_process
    from process.sentiment import sentiment_analysis_process
    from process.sync_hive import sync_data_to_hive_process

    crawller_process()
    clean_data_process()
    sentiment_analysis_process()
    sync_data_to_hive_process()
    
    print("All processes completed successfully.")
    
if __name__ == "__main__":
    main()