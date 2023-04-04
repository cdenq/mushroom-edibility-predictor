# ----------------------------
# Dependencies
# ----------------------------
# libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# global vars
filepath = 'Main/Resources/Raw/primary_data.csv'
filepath2 = 'Main/Resources/Raw/secondary_data.csv'
global_random_state = 42

# ----------------------------
# Preprocessing SECONDARY
# ----------------------------
def preprocessing():
    #import data
    df = pd.read_csv(filepath2, sep=';')

    # PREPROCESS FOR DROPPING NAS
    #dropping rows with nans + one-hot encoding
    df_smaller = df.drop(columns={'stem-root', 'stem-surface','veil-type', 'veil-color', 'spore-print-color', 'gill-spacing'})
    df_smaller.dropna(inplace=True)
    df_smaller_dummies = pd.get_dummies(df_smaller)

    #separate X and y data
    X = df_smaller_dummies.drop(columns = {'class_e','class_p'})
    y = df_smaller_dummies['class_e']
    first_row = X.head(1) #for front-end loading

    #scaling the data
    #using standard scaler because assuming the mushroom data is normal
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    #splitting dataset into train and test
    X_train_secondary_droppedna, X_test_secondary_droppedna, y_train_secondary_droppedna, y_test_secondary_droppedna = train_test_split(X_scaled, y, random_state=global_random_state)

    #scaling the data
    #using standard scaler because assuming the mushroom data is normal
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    #splitting dataset into train and test
    X_train_secondary, X_test_secondary, y_train_secondary, y_test_secondary = train_test_split(X_scaled, y, random_state=global_random_state)
    return first_row, X_train_secondary_droppedna, X_test_secondary_droppedna, y_train_secondary_droppedna, y_test_secondary_droppedna, global_random_state

# ----------------------------
# Preprocessing PRIMARY
# ----------------------------
# IF NEEDED