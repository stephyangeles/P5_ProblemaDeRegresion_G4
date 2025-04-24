class Settings:
    def __init__(self):
        
        self.model = "catboost"  # Model name
        self.model_type = "regression"
        self.model_path = "regression/models/CatBoost.pkl"
        self.data_path = "regression/data/form_data.pkl"
        self.proyect_name = "Regression"
        self.version = "0.0.1"
        self.description = "Regression model for predicting car prices"

        self.api_prefix = "/api"
settings = Settings()
