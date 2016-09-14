.PHONE: data samples

data: samples

samples: data/ham_sample.json data/spam_sample.json

data/ham_sample.json: sample.sh data/ham_dev.json
	./sample.sh data/ham_dev.json > data/ham_sample.json

data/spam_sample.json: sample.sh data/spam_dev.json
	./sample.sh data/spam_dev.json > data/spam_sample.json
