import numpy as np


# Decision stump used as weak classifier
class DecisionStump:
    def __init__(self):
        self.polarity = 1
        self.feature_idx = None
        self.threshold = None
        self.alpha = None

    def predict(self, X):
        n_samples = X.shape[0]
        x_column = X[:, self.feature_idx]
        predictions = np.ones(n_samples)
        if self.polarity == 1:
            predictions[x_column < self.threshold] = -1
        else:
            predictions[x_column > self.threshold] = -1

        return predictions


def update_weights(weights, alpha, incorrect):
    return weights * np.exp(alpha * incorrect * ((weights > 0) | (alpha < 0)))


class Adaboost:
    def __init__(self, n_clf=5, learning_rate=0.5):
        self.n_clf = n_clf
        self.clfs = []
        self.alphas = []
        self.estimator_weights = []
        self.training_errors = []
        self.learning_rate = learning_rate

    def fit(self, X, y):
        n_samples, n_features = X.shape
        weights = np.ones(n_samples) / n_samples

        for m in range(0, self.n_clf):
            clf = DecisionStump()

            min_error = float("inf")
            for feature_i in range(n_features):
                x_column = X[:, feature_i]
                thresholds = np.unique(x_column)

                for threshold in thresholds:
                    p = 1
                    predictions = np.ones(n_samples)
                    predictions[x_column < threshold] = -1

                    misclassified = weights[y != predictions]
                    error = sum(misclassified)

                    if error > 0.5:
                        error = 1 - error
                        p = -1

                    # store the best configuration
                    if error < min_error:
                        clf.polarity = p
                        clf.threshold = threshold
                        clf.feature_idx = feature_i
                        min_error = error

            y_pred = clf.predict(X)
            incorrect = np.asarray([int(y_pred[i] != y[i]) for i in range(len(y))], dtype=np.int32)
            print("inc", incorrect)

            # error
            if min_error == 0.:
                # Found a strong classifier
                self.estimator_weights = [1.]
                self.clfs = [clf]
                break

            # estimator error
            estimator_error = np.mean(np.average(incorrect, weights=weights, axis=0))

            # alpha
            alpha = self.learning_rate * np.log((1. - estimator_error) / estimator_error)

            # boost weights
            weights = update_weights(weights, alpha, incorrect)

            self.estimator_weights.append(alpha)
            self.clfs.append(clf)

    def predict(self, X):
        y_predict_list = np.asarray([clf.predict(X) for clf in self.clfs])
        self.estimator_weights = np.asarray(self.estimator_weights)
        return np.array([np.sign((y_predict_list[:, point] * self.estimator_weights).sum()) for point in range(X.shape[0])]), self.clfs


# Testing
if __name__ == "__main__":
    # Imports
    from sklearn import datasets
    from sklearn.model_selection import train_test_split


    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy


    # data = datasets.load_breast_cancer()
    # X, y = data.data, data.target

    # y[y == 0] = -1

    X = np.array([[123, 213], [312, 111], [23, 98], [122, 11], [999, 666], [420, 69]])
    y = [-1, 1, 1, 1, -
    1, -1]

    # X_train, X_test, y_train, y_test = train_test_split(
    #     X, y, test_size=0.2, random_state=5
    # )

    # Adaboost classification with 5 weak classifiers
    clf = Adaboost(n_clf=5)
    clf.fit(X, y)
    print(X, y)
    y_pred = clf.predict(X)

    acc = accuracy(y, y_pred)
    print("Accuracy:", acc)