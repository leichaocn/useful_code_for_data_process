"""
  pleas make sure install pypinyin before using it
  command just like below:
  pip install pypinyin
"""
import pypinyin

# 不带声调的(style=pypinyin.NORMAL)
def get_pinyin(word):
  s = ''
	for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
		s += ''.join(i)
	return s
 
def main():
  print(get_pinyin('罗密欧_呵呵'))
	print(get_pinyin('罗密欧_hehe'))
	print(get_pinyin('LOCALR'))
  
  # if you have a dataframe of pandas,you can make a new cols named pinyin like this when you have a columns containing chinese characters.
  # df['pinyin']=df.apply(lambda x:get_pinyin(x['chinese']),axis=1)
  
if __name__=='__main__':
  main()
 
