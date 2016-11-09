import sys
import pandas
from sklearn.decomposition import PCA

def main():
    features = pandas.read_csv("dev/features.csv", index_col='num')

    pca = PCA(n_components=30)
    raw_features = features.drop('spam', axis = 1)
    transformed_features = pca.fit_transform(raw_features)
    df = pandas.DataFrame(transformed_features, index = features.index)
    df['spam'] = features['spam']
    df.to_csv("dev/reduced_dim_features.csv", index = True, header = True)


if __name__ == '__main__':
    main()
