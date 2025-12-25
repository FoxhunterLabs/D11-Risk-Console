from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge

def train_models(df, features, targets, *, pca_components=6, ridge_alpha=1.0):
    X = df[features].astype(float).to_numpy()
    y = df[targets].astype(float).to_numpy()[1:]
    X = X[:-1]

    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)

    pca = PCA(n_components=min(pca_components, Xs.shape[1]))
    pca.fit(Xs)

    ridge = Ridge(alpha=ridge_alpha)
    ridge.fit(Xs, y)

    return {
        "scaler": scaler,
        "pca": pca,
        "ridge": ridge,
        "features": features,
        "targets": targets,
    }
