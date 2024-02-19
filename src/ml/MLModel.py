import catboost
import joblib


class MLModel:
    def load_model(self, model_name, model_path):
        if model_name == 'catboost':
            model = catboost.CatBoostClassifier()
            model.load_model(model_path)
        else:
            model = joblib.load(model_path)

        return model

    def get_prediction(self, model_name, model_path, preprocessed_data):
        model = self.load_model(model_name, model_path)
        try:
            prediction = model.predict(preprocessed_data)
            return prediction
        except Exception as e:
            return None