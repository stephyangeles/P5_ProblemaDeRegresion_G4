class Settings:
    def __init__(self):
        
        self.model = "catboost"  # Model name
        self.model_type = "regression"
        self.model_path = "regression/models/catboost_best_model.pkl"
        self.proyect_name = "Regression"
        self.version = "0.0.1"
        self.description = "Regression model for predicting car prices"

        self.api_prefix = "/api/v1"
settings = Settings()
