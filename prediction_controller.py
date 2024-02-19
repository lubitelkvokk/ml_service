import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Загрузка модели
model = joblib.load('dummy_model.pkl')

# Подготовка данных
data = {
    'age_group': [1, 1, 1, 2],
    'RIDAGEYR': [61.0, 26.0, 16.0, 75.0],
    'RIAGENDR': [2.0, 2.0, 1.0, 1.0],
    'PAQ605': [2.0, 2.0, 2.0, 2.0],
    'BMXBMI': [35.7, 20.3, 23.2, 38.9],
    'LBXGLU': [110.0, 89.0, 89.0, 89.0],
    'LBXGLT': [150.0, 80.0, 68.0, 113.0],
    'LBXIN': [14.91, 3.85, 6.14, 17.47]
}
df = pd.DataFrame(data)

# Сделать предсказание
predictions = model.predict(df)

# Вывести результат
print(predictions)
