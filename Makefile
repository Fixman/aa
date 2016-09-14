.PHONE: data samples trains

data: samples trains

samples: data/ham_sample.json data/spam_sample.json

trains: data/ham_train.json data/spam_train.json

data/ham_sample.json: sample.sh data/ham_dev.json
	./sample.sh data/ham_dev.json > data/ham_sample.json

data/spam_sample.json: sample.sh data/spam_dev.json
	./sample.sh data/spam_dev.json > data/spam_sample.json

data/ham_train.json: train_test_split.sh data/ham_dev.json
	./train_test_split.sh data/ham_dev.json

data/spam_train.json: train_test_split.sh data/spam_dev.json
	./train_test_split.sh data/spam_dev.json
