import math
import numpy as np
from core.utils import fclamp

def score_ood_uncertainty(artifact, df):
    if artifact is None or len(df) < 12:
        return 0.0, 0.0

    scaler = artifact["scaler"]
    pca = artifact["pca"]
    ridge = artifact["ridge"]

    x_t = df.iloc[-1][artifact["features"]].astype(float).to_numpy().reshape(1, -1)
    xs = scaler.transform(x_t)

    z = pca.transform(xs)
    recon = pca.inverse_transform(z)
    recon_err = float(np.mean((xs - recon) ** 2))

    x_tm1 = df.iloc[-2][artifact["features"]].astype(float).to_numpy().reshape(1, -1)
    xs_tm1 = scaler.transform(x_tm1)
    yhat = ridge.predict(xs_tm1)
    y = df.iloc[-1][artifact["targets"]].astype(float).to_numpy()

    pred_err = float(np.mean((yhat - y) ** 2))

    ood = 1.0 - math.exp(-recon_err * 4.0)
    unc = 1.0 - math.exp(-pred_err * 0.002)

    return fclamp(ood, 0, 1), fclamp(unc, 0, 1)
