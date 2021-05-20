from sklearn.feature_extraction import text
cv=text.CountVectorizer()
data=['hello world','hello hi','no way','hello hello']
train=cv.fit_transform(data).toarray()
#将英文转为数字
i=0
while i<len(train):
	j=0
	while j<len(train[0]):
		if train[i][j]>0:
			train[i][j]=j
		else:
			train[i][j]=-1
		j+=1
	i+=1

print(train)
vocabulary=cv.get_feature_names()
arr=[]
#将数字转为英文
m=0
while m<len(train):
	n=0
	temp=""
	while n<len(train[0]):
		if train[m][n]!=-1:
			temp+=vocabulary[train[m][n]]
			temp+='  '
		n+=1
	arr.append(temp)
	m+=1				

if __name__ == "__main__":
	print(arr)
