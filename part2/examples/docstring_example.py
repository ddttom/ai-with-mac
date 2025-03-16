#!/usr/bin/env python3
"""
Example script demonstrating proper Python docstring usage for ML projects.

This module illustrates how to write clear and comprehensive docstrings
for machine learning code, following Google-style conventions.
"""

def train_model(X, y, learning_rate=0.01, epochs=100, batch_size=32, verbose=True):
    """
    Train a neural network model on the provided data.
    
    This function implements mini-batch gradient descent to train a 
    simple neural network classifier. It uses early stopping based on
    validation loss to prevent overfitting.
    
    Args:
        X (np.ndarray): Training data of shape (n_samples, n_features)
        y (np.ndarray): Target values of shape (n_samples,)
        learning_rate (float, optional): Step size for gradient updates. Default: 0.01
        epochs (int, optional): Maximum number of training epochs. Default: 100
        batch_size (int, optional): Number of samples per gradient update. Default: 32
        verbose (bool, optional): Whether to print progress during training. Default: True
        
    Returns:
        dict: A dictionary containing the trained model weights, training history,
              and evaluation metrics
        
    Raises:
        ValueError: If X and y have incompatible shapes
    """
    # This is a placeholder implementation
    if X.shape[0] != y.shape[0]:
        raise ValueError(f"X and y have incompatible shapes: {X.shape} vs {y.shape}")
    
    # Placeholder for actual implementation
    print("Training model..." if verbose else "")
    
    # Simulate training loop
    history = {"loss": [], "val_loss": []}
    for epoch in range(epochs):
        # Placeholder for training logic
        train_loss = 1.0 / (epoch + 1)  # Simulated decreasing loss
        val_loss = 1.2 / (epoch + 1)    # Simulated validation loss
        
        history["loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        
        if verbose and epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs}, Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
    
    # Return simulated results
    return {
        "weights": {"layer1": "dummy_weights"},
        "history": history,
        "metrics": {"accuracy": 0.85, "f1_score": 0.82}
    }


class SimpleNeuralNetwork:
    """
    A simple neural network implementation for educational purposes.
    
    This class demonstrates how to structure a neural network class
    with proper documentation. It implements a basic feedforward neural
    network with one hidden layer.
    
    Attributes:
        input_size (int): Number of input features
        hidden_size (int): Number of neurons in the hidden layer
        output_size (int): Number of output neurons
        learning_rate (float): Step size for gradient updates
        weights (dict): Dictionary containing the network weights
    """
    
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        """
        Initialize the neural network.
        
        Args:
            input_size (int): Number of input features
            hidden_size (int): Number of neurons in the hidden layer
            output_size (int): Number of output neurons
            learning_rate (float, optional): Learning rate for training. Default: 0.01
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Initialize weights (placeholder)
        self.weights = {
            "W1": "random_weights_1",
            "b1": "random_bias_1",
            "W2": "random_weights_2",
            "b2": "random_bias_2"
        }
    
    def forward(self, X):
        """
        Perform a forward pass through the network.
        
        Args:
            X (np.ndarray): Input data of shape (batch_size, input_size)
            
        Returns:
            np.ndarray: Model predictions of shape (batch_size, output_size)
        """
        # Placeholder for actual implementation
        return "output_predictions"
    
    def train(self, X, y, epochs=100, batch_size=32):
        """
        Train the neural network on the provided data.
        
        Args:
            X (np.ndarray): Training data of shape (n_samples, input_size)
            y (np.ndarray): Target values of shape (n_samples, output_size)
            epochs (int, optional): Number of training epochs. Default: 100
            batch_size (int, optional): Number of samples per batch. Default: 32
            
        Returns:
            dict: Training history containing loss values
        """
        # Call the standalone training function as an example
        return train_model(X, y, self.learning_rate, epochs, batch_size)


def preprocess_data(data, normalize=True, split_ratio=0.8, random_state=42):
    """
    Preprocess data for machine learning.
    
    This function demonstrates how to document a preprocessing function.
    It shows proper typing hints and comprehensive parameter documentation.
    
    Args:
        data (np.ndarray): Raw input data
        normalize (bool, optional): Whether to normalize the data. Default: True
        split_ratio (float, optional): Train/test split ratio. Default: 0.8
        random_state (int, optional): Random seed for reproducibility. Default: 42
        
    Returns:
        tuple: A tuple containing:
            - X_train (np.ndarray): Training features
            - X_test (np.ndarray): Testing features
            - y_train (np.ndarray): Training targets
            - y_test (np.ndarray): Testing targets
    """
    # Placeholder implementation
    print(f"Preprocessing data with normalize={normalize}, split_ratio={split_ratio}")
    return "X_train", "X_test", "y_train", "y_test"


# Example usage
if __name__ == "__main__":
    import numpy as np
    
    # Create dummy data
    X = np.random.randn(100, 10)
    y = np.random.randint(0, 2, size=100)
    
    # Preprocess
    X_train, X_test, y_train, y_test = preprocess_data(X)
    
    # Create and train model
    model = SimpleNeuralNetwork(input_size=10, hidden_size=5, output_size=1)
    results = model.train(X, y, epochs=50)
    
    print("\nTraining completed with results:")
    print(f"Final loss: {results['history']['loss'][-1]:.4f}")
    print(f"Metrics: {results['metrics']}")
