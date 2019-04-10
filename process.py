def get_process(df):
    # 去除重复值
    df = df.drop_duplicates()
    # df[['longitude', 'latitude']].drop_duplicates())
    
    # 扔掉某个字段
    df = df.drop(['col'], axis=1)
    
    # 扔掉某个字段
    df = df.drop(['col'], axis=1)
    
    ### 填充一定要放在数字化后，避免数字化时有些被置为空时，填充为最新月份。
    df['col'] = df['col'].fillna(1)
    
    # 数字化
    NUM_COLS_FOR_TRAIN = ['col_1', 'col_2']
    for c in NUM_COLS_FOR_TRAIN:
        df[c] = pd.to_numeric(df[c], errors='coerce')
      
    # 重命名
    df = df.rename({"old_name":"new_name"}, axis='columns')
