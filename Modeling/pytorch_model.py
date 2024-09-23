#%%
import torch
import torch.nn as nn
import torch.nn.functional as F
import pyarrow
from sklearn.model_selection import train_test_split

#%%
import pandas as pd

path = r'Modeling\model_ready.parquet'
df = pd.read_parquet(path)

# %%
class Model(nn.Module):

    def __init__(self):
        super().__init__()
        # Define the layers
        self.fc1 = nn.Linear(197, 64) 
        self.fc2 = nn.Linear(64, 32) 
        self.fc3 = nn.Linear(32, 3)

    def forward(self, x):
        x = F.relu(self.fc1(x)) 
        x = F.relu(self.fc2(x))
        x = self.fc3(x)      
        return x
 
# %%
torch.manual_seed(101)
model = Model()

# %%
X = df.drop(['item0', 'item1', 'item2'], axis=1)
y = df[['item0', 'item1', 'item2']]

X = X.values
y = y.values

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=101)

# %%
X_train = torch.Tensor(X_train)
X_test = torch.Tensor(X_test)

y_train = torch.Tensor(y_train)
y_test = torch.Tensor(y_test)

# %%
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

#%%
epochs = 1000
losses = []

for i in range(epochs):
    y_pred = model.forward(X_train)
    loss = criterion(y_pred, y_train)

    losses.append(loss.detach().numpy())

    if i % 10 == 0:
        print(f'Epoch: {i} and loss {loss}')

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# %%
with torch.no_grad():
    print(model(X_test))

# %%
path = r'Modeling\first_attempt_pytorch.pt'
torch.save(model.state_dict(), path)

