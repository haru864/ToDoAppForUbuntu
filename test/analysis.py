import os
import pandas
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


current_file_path: str = os.path.abspath(__file__)
current_directory: str = os.path.dirname(current_file_path)
csv_file_path: str = current_directory + "/" + "test_data.csv"

df: pandas.DataFrame = pandas.read_csv(csv_file_path)
# print(df)
# print(df[["task_type", "difficulty_level", "estimated_time_seconds"]])
# print(df.head(10))
task_type_set: set[str] = set(df["task_type"].tolist())
task_type_mapping: dict[str, int] = {}
for num, task_type in enumerate(task_type_set):
    task_type_mapping[task_type] = num
# print(task_type_mapping)

df_preprocessed: pandas.DataFrame = df.copy(deep=True)
df_preprocessed["task_type"] = df_preprocessed["task_type"].map(task_type_mapping)
# print(df_preprocessed.head(10))

reg = linear_model.LinearRegression()
x = df_preprocessed[["task_type", "difficulty_level", "estimated_time_seconds"]]
y = df_preprocessed["total_elapsed_time_seconds"]
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=0)
reg.fit(x, y)
# print(reg.coef_)

y_pred = reg.predict(x)
# print(y_pred)

mse = mean_squared_error(y, y_pred)
print(f"Mean Squared Error: {mse}")
