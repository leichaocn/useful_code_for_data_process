"""
  get text similarity by computing levenshtein distance

"""

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
  arith = arithmetic()
	txt_distance=arith.levenshteinII(texta, textb)
	# print('txt_distance=',txt_distance)
	# print(max(texta,textb))
	score=1-txt_distance/len(max(texta,textb))
	# print('score=',score)
	return score

def main():
  texta = '523LIasdf'
	textb = '523LIasdfasdf adsf asdf '
  print(get_txt_similiar_score(texta,textb))

if __name__=='__main__':
  main()
