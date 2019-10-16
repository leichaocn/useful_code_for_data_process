"""
Categorical Variables 分两种：
1.ordinal variables. 即顺序变量，各取值之间存在单调关系，适合进行单纯数字化即可，Label Encoding
2.nominal variables.即名称变量，各取值之间无单调关系，适合用独热，One-Hot Encoding。但是值太多效果较差，不宜超过15个值。

code source:
Intermediate Machine Learning Home Page
https://www.kaggle.com/alexisbcook/categorical-variables
"""

# 获取训练年数据中的对象型字段
# Get list of categorical variables
s = (X_train.dtypes == 'object')
object_cols = list(s[s].index)
print("Categorical variables:")
print(object_cols)


# 扔掉对象型字段，看看结果如何
drop_X_train = X_train.select_dtypes(exclude=['object'])
drop_X_valid = X_valid.select_dtypes(exclude=['object'])
print("MAE from Approach 1 (Drop categorical variables):")
print(score_dataset(drop_X_train, drop_X_valid, y_train, y_valid))






# 使用LabelEncoder
from sklearn.preprocessing import LabelEncoder
# Make copy to avoid changing original data 
label_X_train = X_train.copy()
label_X_valid = X_valid.copy()
# Apply label encoder to each column with categorical data
label_encoder = LabelEncoder()
for col in object_cols:
    label_X_train[col] = label_encoder.fit_transform(X_train[col])
    label_X_valid[col] = label_encoder.transform(X_valid[col])
print("MAE from Approach 2 (Label Encoding):") 
print(score_dataset(label_X_train, label_X_valid, y_train, y_valid))





# 使用OneHotEncoder
from sklearn.preprocessing import OneHotEncoder
# handle_unknown='ignore'，即对验证集中出现未在训练中出现的值时的缺省操作。
# sparse=False 即获取完整矩阵，而非稀疏编码的矩阵。
# Apply one-hot encoder to each column with categorical data
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[object_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[object_cols]))

# One-hot encoding removed index; put it back
OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

# Remove categorical columns (will replace with one-hot encoding)
num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

# Add one-hot encoded columns to numerical features
OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)

print("MAE from Approach 3 (One-Hot Encoding):") 
print(score_dataset(OH_X_train, OH_X_valid, y_train, y_valid))
