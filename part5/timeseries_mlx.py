#!/usr/bin/env python3

"""
Time series forecasting with MLX.
"""

import os
import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim

class SimpleRNN(nn.Module):
    """Simple recurrent neural network for time series forecasting."""
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.rnn_cell = nn.RNNCell(input_size, hidden_size)
        self.linear = nn.Linear(hidden_size, output_size)
    
    def __call__(self, x, hidden=None):
        """Forward pass through the network."""
        # x shape: (batch_size, sequence_length, input_size)
        batch_size, seq_len, _ = x.shape
        
        if hidden is None:
            hidden = mx.zeros((batch_size, self.hidden_size))
        
        outputs = []
        for t in range(seq_len):
            hidden = self.rnn_cell(x[:, t, :], hidden)
            outputs.append(hidden)
        
        # Use the last hidden state for prediction
        output = self.linear(outputs[-1])
        return output, hidden

def load_stock_data(csv_file, target_column="Close"):
    """Load stock price data from CSV."""
    dates = []
    prices = []
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.append(row["Date"])
            prices.append(float(row[target_column]))
    
    return dates, prices

def prepare_timeseries_data(data, sequence_length=10):
    """Prepare time series data for training."""
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    
    # Convert to MLX arrays
    X = mx.array(np.array(X, dtype=np.float32).reshape(-1, sequence_length, 1))
    y = mx.array(np.array(y, dtype=np.float32).reshape(-1, 1))
    
    # Normalize data
    X_mean = mx.mean(X)
    X_std = mx.std(X)
    X = (X - X_mean) / X_std
    
    y_mean = mx.mean(y)
    y_std = mx.std(y)
    y = (y - y_mean) / y_std
    
    return X, y, X_mean, X_std, y_mean, y_std

def train_model(model, X, y, epochs=100, batch_size=32, learning_rate=0.01):
    """Train the model."""
    optimizer = optim.Adam(learning_rate=learning_rate)
    num_samples = X.shape[0]
    num_batches = num_samples // batch_size
    
    # Define loss function
    def loss_fn(model, X_batch, y_batch):
        pred, _ = model(X_batch)
        return mx.mean(mx.square(pred - y_batch))
    
    # Define training step
    def train_step(model, X_batch, y_batch):
        loss, grads = mx.value_and_grad(model, loss_fn)(model, X_batch, y_batch)
        optimizer.update(model, grads)
        return loss
    
    # Training loop
    losses = []
    for epoch in range(epochs):
        # Shuffle data
        indices = np.random.permutation(num_samples)
        epoch_loss = 0
        
        for i in range(num_batches):
            batch_indices = indices[i * batch_size:(i + 1) * batch_size]
            X_batch = X[batch_indices]
            y_batch = y[batch_indices]
            
            loss = train_step(model, X_batch, y_batch)
            epoch_loss += loss.item()
        
        epoch_loss /= num_batches
        losses.append(epoch_loss)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss:.6f}")
    
    return losses

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Time series forecasting with MLX")
    parser.add_argument("--csv", type=str, required=True,
                        help="Path to CSV file with stock price data")
    parser.add_argument("--column", type=str, default="Close",
                        help="Column name for price data")
    parser.add_argument("--epochs", type=int, default=100,
                        help="Number of training epochs")
    parser.add_argument("--sequence", type=int, default=10,
                        help="Sequence length for time series")
    parser.add_argument("--predict", type=int, default=30,
                        help="Number of days to predict")
    args = parser.parse_args()
    
    # Load and prepare data
    dates, prices = load_stock_data(args.csv, args.column)
    X, y, X_mean, X_std, y_mean, y_std = prepare_timeseries_data(prices, args.sequence)
    
    # Create and train model
    model = SimpleRNN(input_size=1, hidden_size=32, output_size=1)
    losses = train_model(model, X, y, epochs=args.epochs)
    
    # Make predictions
    test_data = prices[-args.sequence:]
    predictions = []
    current_sequence = mx.array(np.array(test_data, dtype=np.float32).reshape(1, args.sequence, 1))
    current_sequence = (current_sequence - X_mean) / X_std
    
    # Generate future predictions
    hidden = None
    for _ in range(args.predict):
        # Make prediction
        pred, hidden = model(current_sequence, hidden)
        
        # Denormalize
        pred_value = pred.item() * y_std.item() + y_mean.item()
        predictions.append(pred_value)
        
        # Update sequence (remove first element, add prediction)
        new_seq = mx.concatenate([current_sequence[:, 1:, :], 
                                 mx.array([[[pred.item()]]]) * y_std / X_std + (y_mean - X_mean) / X_std], 
                                 axis=1)
        current_sequence = new_seq
    
    # Plot results
    plt.figure(figsize=(12, 6))
    
    # Plot historical data
    plt.plot(range(len(prices)), prices, label="Historical Data")
    
    # Plot predictions
    forecast_range = range(len(prices) - 1, len(prices) + args.predict - 1)
    plt.plot(forecast_range, predictions, label="Forecast", color="red")
    
    # Add vertical line at prediction start
    plt.axvline(x=len(prices) - 1, color="gray", linestyle="--")
    
    plt.title(f"Stock Price Forecast ({args.column})")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    
    # Save plot
    output_file = f"stock_forecast_{os.path.basename(args.csv).split('.')[0]}.png"
    plt.savefig(output_file)
    print(f"Forecast saved to {output_file}")
    
    # Print predictions
    print("\nPredictions for the next", args.predict, "days:")
    for i, pred in enumerate(predictions):
        print(f"Day {i+1}: {pred:.2f}")

if __name__ == "__main__":
    main()
