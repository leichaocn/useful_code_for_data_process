from sklearn.isotonic import IsotonicRegression
import pandas as pd


def get_isotonic_revise(x,y,increasing=True):
    ir = IsotonicRegression(increasing=increasing)
    y_ = ir.fit_transform(x, y)
    return y_

def make_isotonic_cleaning(df,target,mono_col,increasing=True):
    if len(df[target])>=2:
        # 如果长度大于等于2，才有必要修正
        # 以df[target]为x，df[mono_col]为y，输出修正后的y_
        y_ = get_isotonic_revise(df[target], df[mono_col], increasing=increasing)
        # df[mono_col + '_revised']=pd.Series(y_,index=df[mono_col].index)
        df[mono_col]=pd.Series(y_,index=df[mono_col].index)
    else:
        # 长度等于1，直接复制。
        # df[mono_col+'_revised']=df[mono_col]
        df[mono_col]=df[mono_col]
    return df
    
# 对于囊括单调性字段的数组mono_cols_list，修正其中每一个字段
def make_cols_monotonical(df,mono_cols_list,increasing=True):
    all_cols_list=[col_1, col_2, col_3, col_4]
    target = 'car_price'
    for mono_col in mono_cols_list:
        print ('-'*100)
        print ('本轮要修正的字段为',mono_col,'单调性increasing=',increasing)
        this_cols=all_cols_list.copy()
        this_cols.remove(mono_col)
        # df[mono_col+'_amended'] = df.groupby(this_cols).apply(lambda x:make_isotonic_cleaning(x=x[target], y=x[mono_col], increasing=increasing))
        df = df.groupby(this_cols).apply(make_isotonic_cleaning,target=target,mono_col=mono_col,increasing=increasing)
    return df
    
def main():
    
    increasing_cols=[col_2]
    decreasing_cols=[col_3, col_4]
    total_data = make_cols_monotonical(total_data,decreasing_cols,increasing=False)
    total_data = make_cols_monotonical(total_data,increasing_cols,increasing=True)
    
if __name__ == '__main__':
    main()
 
