import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from EDA.ip import rf_model

# Загрузка данных для предсказания
data_to_predict = pd.read_csv('to_predict.csv')

# Предположим, что у вас уже есть обученная модель 'rf_model'
# Если нет, то вам нужно сначала её обучить, как показано в предыдущих примерах кода
# Например:
# rf_model = RandomForestClassifier()
# rf_model.fit(X_train, y_train)

# Получение предсказаний
predictions = rf_model.predict(data_to_predict)

# Вывод результатов предсказания
for i, prediction in enumerate(predictions, start=1):
    print(f"Sample {i}: {'Diabetes' if prediction == 1 else 'No Diabetes'}")
