import controller as con
from sklearn.tree import DecisionTreeClassifier as dtc
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.metrics import accuracy_score as acs
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression as lr
from sklearn.ensemble import RandomForestRegressor as rfr
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import root_mean_squared_error as rmse


def _split_trainee_valid_(dataframe1, dataframe2=None, percent_test: float = 0.25, random_state=12345):
    try:
        if dataframe2 == None:
            con.log.INFO("Split started with 1 df")
            return tts(dataframe1, test_size=percent_test, random_state=random_state)
        else:
            con.log.INFO("Split started with 2 df")
            return tts(dataframe1, dataframe2, test_size=percent_test, random_state=random_state)
    except Exception as e:
        con.log.ERROR(con.__exception__(e, 'split_trainee'))
