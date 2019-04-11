
class arithmetic():

    def __init__(self):
        pass

    ''''' 【编辑距离算法】 【levenshtein distance】 【字符串相似度算法】 '''

    def levenshtein(self, first, second):
        if len(first) > len(second):
            first, second = second, first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [list(range(second_length)) for x in list(range(first_length))]
        # print distance_matrix
        for i in list(range(1, first_length)):
            for j in list(range(1, second_length)):
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1]
                if first[i - 1] != second[j - 1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion, deletion, substitution)
        #print (distance_matrix)
        return distance_matrix[first_length - 1][second_length - 1]

    def levenshteinII(self, first, second):
        # 确保first字符短，second字符长
        if len(first) > len(second):
            first, second = second, first
        if len(first) == 0:
            return len(second),second
        if len(second) == 0:
            return len(first),first
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [list(range(second_length)) for x in list(range(first_length))]
        #print (distance_matrix)
        for i in list(range(1, first_length)):
            for j in list(range(1, second_length)):
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1]
                if first[i - 1] != second[j - 1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion, deletion, substitution)
        #print (distance_matrix)
        # print ('distance_matrix[first_length - 1][second_length - 1]=',distance_matrix[first_length - 1][second_length - 1])
        return distance_matrix[first_length - 1][second_length - 1]

def get_txt_similiar_score(texta,textb):
    # texta = '523LIasdf'
    # textb = '523LIasdf'
    arith = arithmetic()
    txt_distance=arith.levenshteinII(texta, textb)
    # print('txt_distance=',txt_distance)
    # print(max(texta,textb))
    score=txt_distance/len(max(texta,textb))
    # print('score=',score)
    return score


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
    df = df.rename({"old_name":"new_name"}, axis='columns')    # 计算距离，包括 年款 排量 model_str
    df['C_delta'] = df.apply(lambda x: get_txt_similiar_score(x['C'], test_demo['C']), axis=1)
    df['A_delta'] = abs(df['A'] - test_demo['A'])
    df['B_delta'] = abs(df['B'] - test_demo['B'])
    # 按年款 排量 model_str_similiar_score排序
    df = df.sort_values(by=['A_delta','B_delta','C_delta'])
    
    
   
