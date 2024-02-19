from datetime import time

from sqlalchemy.util import queue

from src.db.schemas.predictor import PredictionInfo
from src.db.schemas.users import UserCreate
from src.ml.MLModel import MLModel
from src.ml.preprocess import CSVDataProcessor
from src.services.user_service import user_service

# redis_conn = Redis()


async def handle_prediction(model_info, data_json, create_time, user_id, balance, model_cost):
    model = MLModel()
    data = pd.read_json(data_json)
    start_time = time.time()

    try:
        prediction = model.get_prediction(model_info['name'], model_info['path'], data)
        total_time = time.time() - start_time
        await prediction_repository.update(create_time, {"is_successful": True, "duration": total_time})
        await billig_service.update_balance(user_id, balance, model_cost)
        logging.info(f"Как тебе такое, Маск")
        return {"model_info": model_info, "results": prediction, "total_time": total_time, "status": 'success',
                'create_time': create_time}
    except Exception as e:
        await prediction_repository.update(create_time, {"is_successful": False})
        logging.error(f"Ошибка при выполнении предсказания: {e}")
        logging.error(f"надо было и дальше учиться на биоинженера")
        return {"model_info": model_info, "error": str(e), "status": 'error', 'create_time': create_time}


class PredictionService:
    def __init__(self):
        self.model = MLModel()
        self.data_preprocessor = CSVDataProcessor()
        self.mapper = {1: 'GBM', 0: 'LGG'}

    async def get_model_from_db(self, model):
        # model_info = await model_repository.get_by_modelname(modelname=model)
        # if model_info is None:
        #     raise ModelNotFoundError()
        return model_info

    async def predict(self, user: UserCreate, model: str, file):
        balance = await user_service.check_balance(user)
        model_info = await self.get_model_from_db(model)
        billig_service.is_enough_for_model(model_info.cost, balance)
        data = await self.data_preprocessor.process(file)
        data_json = data.to_json()
        model_dict = {'name': model_info.modelname, 'path': model_info.file_path, 'id': model_info.id}
        create_time = time.time()
        job = queue.enqueue(handle_prediction, model_dict, data_json, create_time, user.id, balance, model_info.cost)
        prediction = PredictionInfo(id=job.id,
                                    user_id=user.id,
                                    model_id=model_info.id,
                                    cost=model_info.cost,
                                    timestamp=create_time)
        await prediction_repository.add(prediction.dict())
        return job.id

    async def get_job_results(self, job_id):
        job = queue.fetch_job(job_id)
        if not job:
            raise JobNotFoundError()

        if job.is_finished:
            latest_result = job.latest_result()
            results = latest_result.return_value
        else:
            raise ModelStillProcessingError

        pred = [self.mapper[result] for result in results['results']]

        response = PredictionResponse(
            prediction_id=job.id,
            prediction_model_id=results['model_info']['id'],
            created_at=results['create_time'],
            prediction_results=pred
        )

        return response

    async def get_user_predictions(self, user):
        predictions = await prediction_repository.get_by_user_id(user.id)
        return predictions


prediction_service = PredictionService()


prediction_service.predict(User())