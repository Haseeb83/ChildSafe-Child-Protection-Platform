from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression

def calibrate(base_clf, X_val, y_val):
    calib = CalibratedClassifierCV(base_estimator=base_clf, method="sigmoid", cv="prefit")
    calib.fit(X_val, y_val)
    return calib