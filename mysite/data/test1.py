from sklearn.feature_extraction import text
import jieba
from sklearn import neural_network
from sklearn import model_selection
from sklearn import ensemble

with open('data.txt','r+',encoding='utf-8') as f:
	data=f.read()
data=data.split('\n')
question=[]
answer=[]
for i in data:
	question.append(" ".join(jieba.cut(i.split(',')[0])))
	answer.append(" ".join(jieba.cut(i.split(',')[1])))
cv=text.CountVectorizer()
X_train=cv.fit_transform(question).toarray()
i=0
while i<len(X_train):
	j=0
	while j<len(X_train[0]):
		if  X_train[i][j]>0:
			X_train[i][j]=j
		else:
			X_train[i][j]=-1
		j+=1
	i+=1
#print(cv.vocabulary_)
y_train=cv.fit_transform(answer).toarray()
i=0
while i<len(y_train):
	j=0
	while j<len(y_train[0]):
		if y_train[i][j]>0:
			y_train[i][j]=j
		else:
			y_train[i][j]=-1
		j+=1
	i+=1
#print(y_train)
#mlp=neural_network.MLPClassifier(hidden_layer_sizes=(100,20),max_iter=5000)
X,X_test,y,y_test=model_selection.train_test_split(X_train,y_train,test_size=.1,random_state=0)
from sklearn import preprocessing
from sklearn import pipeline
sc=preprocessing.StandardScaler()
rfc=ensemble.RandomForestClassifier()
trainer=pipeline.make_pipeline(sc,rfc).fit(X,y)
#y_predict=rfc.predict(X_test)
#print(y_predict)

if __name__ == "__main__":
	print(X_train)
	print(y_train)
	y_predict=trainer.predict(X_test)
	print(y_predict)
	print(cv.vocabulary_)