import numpy as np
import h5py


def sigmoid(Z):
    """
    Argumenty:
    Z -- tablica numpy o dowolnym kształcie

    Zwraca:
    A -- wynik funkcji sigmoid(z), taki sam kształt jak Z
    cache -- zwraca również Z, przydatne podczas propagacji wstecznej
    """
    A = 1 / (1 + np.exp(-Z))
    cache = Z
    return A, cache


def relu(Z):
    """
    Argumenty:
    Z -- Wynik warstwy liniowej, dowolny kształt

    Zwraca:
    A -- Parametr po aktywacji, ten sam kształt co Z
    cache -- słownik pythona zawierający "A"; przechowywany do efektywnego obliczania propagacji wstecznej
    """
    A = np.maximum(0, Z)
    cache = {"A": A}

    return A, cache


def relu_backward(dA, cache):
    """
    Argumenty:
    dA -- gradient po aktywacji, dowolny kształt
    cache -- 'Z', przechowywane dla efektywnego obliczania propagacji wstecznej

    Zwraca:
    dZ -- Gradient kosztu względem Z
    """

    Z = cache  # In activation_cache, we have stored Z
    dZ = np.array(dA, copy=True)  # just converting dA to a correct object.

    return dZ


def sigmoid_backward(dA, cache):
    """
    Argumenty:
    dA -- gradient po aktywacji, dowolny kształt
    cache -- 'Z', przechowywane dla efektywnego obliczania propagacji wstecznej

    Zwraca:
    dZ -- Gradient kosztu względem Z
    """

    Z = cache  # In activation_cache, we have stored Z
    s = 1 / (1 + np.exp(-Z))
    dZ = dA * s * (1 - s)

    return dZ


def load_data():
    """
    Zwraca:
    train_set_x_orig -- tablica numpy z cechami zestawu treningowego
    train_set_y_orig -- tablica numpy z etykietami zestawu treningowego
    test_set_x_orig -- tablica numpy z cechami zestawu testowego
    test_set_y_orig -- tablica numpy z etykietami zestawu testowego
    classes -- tablica numpy z listą klas
    """

    with h5py.File('data/train_catvnoncat.h5', 'r') as train_dataset:
        train_set_x_orig = np.array(train_dataset['train_set_x'][:])
        train_set_y_orig = np.array(train_dataset['train_set_y'][:])
        classes = np.array(train_dataset['list_classes'][:])
    
    with h5py.File('data/test_catvnoncat.h5', 'r') as test_dataset:
        test_set_x_orig = np.array(test_dataset['test_set_x'][:])
        test_set_y_orig = np.array(test_dataset['test_set_y'][:])

    train_set_x_orig = train_set_x_orig.reshape((train_set_x_orig.shape[0], -1)).T
    test_set_x_orig = test_set_x_orig.reshape((test_set_x_orig.shape[0], -1)).T
    
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


def initialize_parameters(n_x, n_h, n_y):
    """
    Argumenty:
    n_x -- rozmiar warstwy wejściowej
    n_h -- rozmiar warstwy ukrytej
    n_y -- rozmiar warstwy wyjściowej

    Zwraca:
    parameters -- słownik Pythona zawierający parametry:
                  W1 -- macierz wag o kształcie (n_h, n_x)
                  b1 -- wektor bias o kształcie (n_h, 1)
                  W2 -- macierz wag o kształcie (n_y, n_h)
                  b2 -- wektor bias o kształcie (n_y, 1)
    """

    np.random.seed(1)
    
    W1 = np.random.randn(n_h, n_x) * 0.01
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))
    
    parameters = {
        "W1": W1,
        "b1": b1,
        "W2": W2,
        "b2": b2
    }

    return parameters


def linear_forward(A, W, b):
    """
    Argumenty:
    A -- aktywacje z poprzedniej warstwy (lub dane wejściowe): (rozmiar poprzedniej warstwy, liczba przykładów)
    W -- macierz wag: tablica numpy o kształcie (rozmiar bieżącej warstwy, rozmiar poprzedniej warstwy)
    b -- wektor bias, tablica numpy o kształcie (rozmiar bieżącej warstwy, 1)

    Zwraca:
    Z -- wejście funkcji aktywacji, nazywane również parametrem przed aktywacją
    cache -- słownik python zawierający "A", "W" i "b"; przechowywany do efektywnego obliczania propagacji wstecznej
    """
    Z = np.dot(W, A) + b
    cache = {"A": A, "W": W, "b": b}

    return Z, cache


def linear_activation_forward(A_prev, W, b, activation):
    """
    Argumenty:
    A_prev -- aktywacje z poprzedniej warstwy (lub dane wejściowe): (rozmiar poprzedniej warstwy, liczba przykładów)
    W -- macierz wag: tablica numpy o kształcie (rozmiar bieżącej warstwy, rozmiar poprzedniej warstwy)
    b -- wektor bias, tablica numpy o kształcie (rozmiar bieżącej warstwy, 1)
    activation -- funkcja aktywacji używana w tej warstwie, przechowywana jako tekst: "sigmoid" lub "relu"

    Zwraca:
    A -- wynik funkcji aktywacji, nazywany również wartością po aktywacji
    cache -- słownik python zawierający "linear_cache" i "activation_cache";
             przechowywany do efektywnego obliczania propagacji wstecznej
    """

    if activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)
    elif activation == "relu":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)
    
    cache = (linear_cache, activation_cache)

    return A, cache


def compute_cost(AL, Y):
    """
    Argumenty:
    AL -- wektor prawdopodobieństwa odpowiadający twoim przewidywaniom etykiet, kształt (1, liczba przykładów)
    Y -- prawdziwy wektor etykiet (na przykład zawierający 0, jeśli nie-kot, 1, jeśli kot), kształt (1, liczba przykładów)

    Zwraca:
    cost -- koszt entropii krzyżowej
    """

    m = Y.shape[1]  # number of examples

    AL = np.clip(AL, 1e-10, 1 - 1e-10)

    # Compute the cross-entropy cost
    cost = -1/m * np.sum(Y * np.log(AL) + (1 - Y) * np.log(1 - AL))

    cost = np.squeeze(cost)  # Ensures cost is a scalar (not an array with one element)
    assert(cost.shape == ()), "The cost should be a scalar"

    return cost


def linear_backward(dZ, cache):
    """
    Argumenty:
    dZ -- Gradient kosztu względem liniowego wyjścia (bieżącej warstwy l)
    cache -- krotka wartości (A_prev, W, b) pochodząca z propagacji wprzód w bieżącej warstwie

    Zwraca:
    dA_prev -- Gradient kosztu względem aktywacji (poprzedniej warstwy l-1), taki sam kształt jak A_prev
    dW -- Gradient kosztu względem W (bieżącej warstwy l), taki sam kształt jak W
    db -- Gradient kosztu względem b (bieżącej warstwy l), taki sam kształt jak b
    """

    A_prev = cache["A"]
    W = cache["W"]
    b = cache["b"]
    m = A_prev.shape[1]

    dW = 1/m * np.dot(dZ, A_prev.T)
    db = 1/m * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)

    return dA_prev, dW, db


def linear_activation_backward(dA, cache, activation):
    """
    Argumenty:
    dA -- gradient po aktywacji dla bieżącej warstwy l
    cache -- krotka wartości (linear_cache, activation_cache) przechowywana dla efektywnego obliczania propagacji wstecznej
    activation -- funkcja aktywacji używana w tej warstwie, "sigmoid" lub "relu"

    Zwraca:
    dA_prev -- Gradient kosztu względem aktywacji (poprzedniej warstwy l-1), taki sam kształt jak A_prev
    dW -- Gradient kosztu względem W (bieżącej warstwy l), taki sam kształt jak W
    db -- Gradient kosztu względem b (bieżącej warstwy l), taki sam kształt jak b
    """

    linear_cache, activation_cache = cache
    
    if activation == "sigmoid":
        dZ = sigmoid_backward(dA, activation_cache)
    elif activation == "relu":
        dZ = relu_backward(dA, activation_cache)
    
    dA_prev, dW, db = linear_backward(dZ, linear_cache)

    return dA_prev, dW, db


def update_parameters(parameters, grads, learning_rate):
    """
    Argumenty:
    parameters -- słownik Pythona zawierający twoje parametry
    grads -- słownik Pythona zawierający twoje gradienty, wynik L_model_backward
    learning_rate -- współczynnik uczenia się

    Zwraca:
    parameters -- słownik Pythona zawierający zaktualizowane parametry
                  parameters["W" + str(l)] = ...
                  parameters["b" + str(l)] = ...
    """

    L = len(parameters) // 2  # number of layers in the neural network

    for l in range(1, L + 1):
        parameters["W" + str(l)] -= learning_rate * grads["dW" + str(l)]
        parameters["b" + str(l)] -= learning_rate * grads["db" + str(l)]
    
    return parameters
