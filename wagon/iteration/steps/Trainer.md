class Trainer(object):

    def __init__(self, X, y, **kwargs):
        self.pipeline = None
        self.kwargs = kwargs
        self.dist = self.kwargs.get("distance_type", "euclidian")
        self.X_train, self.X_val, self.y_train, self.y_val = \
            train_test_split(X, y, test_size=0.15)
        self.nrows = self.X_train.shape[0]

    def get_estimator(self):
        estimator = self.kwargs.get("estimator", "RandomForest")
        if estimator == "RandomForest":
            model = RandomForestRegressor()
        return model

    def set_pipeline(self):
        # Define feature engineering pipeline blocks here
        pipe_tf = make_pipeline(TimeEncoder(),
                                OneHotEncoder())
        pipe_dist = make_pipeline(DistTransformer(distance_type=self.dist),
                                      StandardScaler())
        pipe_d2center = make_pipeline(DistToCenter(),
                                      StandardScaler())

        # Define default feature engineering blocs
        distance_columns = list(DIST_ARGS.values())
        feateng_blocks = [
            ('distance', pipe_dist, distance_columns),
            ('time_features', pipe_tf, ['pickup_datetime']),
            ('distance_to_center', pipe_d2center, distance_columns)]

        features_encoder = ColumnTransformer(feateng_blocks,
                                             n_jobs=None,
                                             remainder="drop")

        regressor = self.get_estimator()

        self.pipeline = Pipeline(steps=[
                    ('features', features_encoder),
                    ('rgs', regressor)])

    def train(self):
        self.set_pipeline()
        self.pipeline.fit(self.X_train, self.y_train)

    def evaluate(self):
        rmse_train = self.compute_rmse(self.X_train, self.y_train)
        rmse_val = self.compute_rmse(self.X_val, self.y_val, show=True)
        output_print = f"rmse train: {rmse_train} || rmse val: {rmse_val}"
        print(colored(output_print, "blue"))

    def compute_rmse(self, X_test, y_test, show=False):
        y_pred = self.pipeline.predict(X_test)
        rmse = compute_rmse(y_pred, y_test)
        return round(rmse, 3)

    def save_model(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, 'model.joblib')
        print(colored("model.joblib saved locally", "green"))

    ## Params
    params = dict(
        estimator='RandomForest',
        distance_type='haversine',
    )

    trainer = Trainer(X, y, **params)
    trainer.train()
    trainer.evaluate()
    trainer.save_model()

