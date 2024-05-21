import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import *


def two_layer_model(X, Y, layers_dims, learning_rate=0.0001, num_iterations=3000, print_cost=False):
    """
    Implementacja dwuwarstwej siecu neuronoweh:
    
    Argumenty:
    X -- dane wejściowe, kształt 
    Y -- wektor prawdziwych etykiet ( 1 - 'kot', 0 - 'nie-kot'),
    layers_dims -- wymiary warstw
    num_iterations -- liczba iteracji 
    learning_rate -- współczynnik uczenia się 
    
    Zwraca:
    parameters -- słownik zawierający W1, W2, b1, b2
    """
    
    np.random.seed(1)
    grads = {}
    costs = []  # to keep track of the cost
    m = X.shape[1]  # number of examples
    (n_x, n_h, n_y) = layers_dims
    
    # Initialize parameters dictionary
    parameters = initialize_parameters(n_x, n_h, n_y)
    
    # Loop (gradient descent)
    for i in range(num_iterations):

        if i % 100 == 0:
            print(f"Iteration {i}")

        # Forward propagation: LINEAR -> RELU -> LINEAR -> SIGMOID
        A1, cache1 = linear_activation_forward(X, parameters["W1"], parameters["b1"], activation="relu")
        A2, cache2 = linear_activation_forward(A1, parameters["W2"], parameters["b2"], activation="sigmoid")
        
        # Compute cost
        cost = compute_cost(A2, Y)
        
        # Initialize backward propagation
        A2 = np.clip(A2, 1e-10, 1 - 1e-10)
        dA2 = - (np.divide(Y, A2) - np.divide(1 - Y, 1 - A2))
        
        # Backward propagation
        dA1, dW2, db2 = linear_activation_backward(dA2, cache2, activation="sigmoid")
        dA0, dW1, db1 = linear_activation_backward(dA1, cache1, activation="relu")
        
        # Set grads
        grads["dW1"] = dW1
        grads["db1"] = db1
        grads["dW2"] = dW2
        grads["db2"] = db2
        
        # Update parameters
        parameters = update_parameters(parameters, grads, learning_rate)
        
        # Print the cost every 100 training examples
        if print_cost and i % 100 == 0:
            print(f"Cost after iteration {i}: {np.squeeze(cost)}")
            costs.append(cost)
    
    return parameters


def predict(X, parameters):
    """
    Using the learned parameters, predicts a class for each example in X
    
    Arguments:
    X -- input data of size (n_x, m)
    parameters -- python dictionary containing your parameters 
    
    Returns
    predictions -- vector of predictions of our model (red: 0 / blue: 1)
    """
    
    # Computes probabilities using forward propagation, and classifies to 0/1 using 0.5 as the threshold.
    A2, cache = linear_activation_forward(X, parameters["W1"], parameters["b1"], activation="relu")
    A2, cache = linear_activation_forward(A2, parameters["W2"], parameters["b2"], activation="sigmoid")
    predictions = (A2 > 0.5).flatten()
    
    return predictions

def score(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)


def main():
    np.random.seed(1)
    train_x_orig, train_y, test_x_orig, test_y, classes = load_data()

    print(train_x_orig.shape)

    n_x = train_x_orig.shape[0]
    n_h = 10
    n_y = 1
    layers_dims = (n_x, n_h, n_y)

    parameters = two_layer_model(
        train_x_orig,
        train_y,
        layers_dims,
        learning_rate=0.0001,
        num_iterations=2200,
        print_cost=True
    )

    predictions_train = predict(train_x_orig, parameters)
    predictions_test = predict(test_x_orig, parameters)

    predictions_train_df = pd.DataFrame({
        "train_y": train_y.flatten(),
        "predictions_train": predictions_train
    })

    predictions_test_df = pd.DataFrame({
        "test_y": test_y.flatten(),
        "predictions_test": predictions_test
    })

    print(predictions_train_df)
    print(predictions_test_df)

    print(f"Train accuracy: {score(train_y.flatten(), predictions_train) * 100:.2f}%")
    print(f"Test accuracy: {score(test_y.flatten(), predictions_test) * 100:.2f}%")


if __name__ == "__main__":
    main()
