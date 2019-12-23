from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.datasets import load_wine
import cloudpickle


def run_batch():
    # Load data
    features, target = load_wine(return_X_y=True)

    # Make dataset
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.30,
        random_state=42
    )

    # Set pipeline
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('reduce_dim', PCA()),
        ('svm', SVC()),
    ])

    # Set hyper params
    param_grid = [{
        'scaler': [StandardScaler(), MinMaxScaler()],
        'reduce_dim__n_components': [1, 3, 5],
        'svm__C': [0.5, 1.0, 1.5],
    }]

    # Set GridSearch CrossValidation
    clf = GridSearchCV(
        pipe,
        cv=5,
        verbose=1,
        param_grid=param_grid
    )

    # Train
    clf.fit(X_train, y_train)

    # Predict
    y_train_pred = clf.predict(X_train)
    y_test_pred = clf.predict(X_test)

    # Report
    print('best_estimator', clf.best_estimator_)
    print('train', classification_report(y_train, y_train_pred))
    print('test', classification_report(y_test, y_test_pred))

    # Serialize model and etc ...
    _ = cloudpickle.dumps(clf)
    print('Congratulations!!!')
