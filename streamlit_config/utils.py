import pandas as pd
from pickleshare import PickleShareDB
import os

selec_dataset = {
    "données physiques": "PHY",
    "données réseaux": "NETW",
}

model_names_phy = {
    "CNN 1D": "cnn1d",
    "KNN" : "knn",
    "KNN PCA" : "knn_pca",
    "CART" : "cart",
    "Random Forest" : "rf",
    "XGBoost" : "xgb",
    "MLP" : "mlp",
}

colors_model_names = {
    "CNN 1D": "purple",
    "KNN": "blue_green",
    "KNN PCA": "blue_green",
    "CART": "green",
    "Random Forest": "yellow",
    "XGBoost": "orange",
    "MLP": "pink",
    "KNN article": "Bleu clair",
    "RF article": "Bleu moyen",
    "SVM Forest article": "Bleu vif",
    "NB article": "Bleu foncé",
}

model_names_netw = {
    "KNN": "KNN",
    "CART": "CART",
    "Random Forest": "RF",
    "XGBoost": "XGBoost",
    "MLP": "MLP",
}

attack_types_phy = {
    "détection d'attaque": "labeln",
    "DoS": "DoS",
    "MITM": "MITM",
    "physical fault": "physical fault",
    "scan": "scan",
}

attack_types_net = { 
    "détection d'attaque": "labeln",
    "DoS": "DoS",
    "MITM": "MITM",
    "physical fault": "physical fault",
    "anomaly": "anomaly",
}


data_dir = "prep_data"
db = PickleShareDB(os.path.join(data_dir, "kity"))

files_phy = []
files_netw = []

for _, v1 in attack_types_phy.items():
    for _, v2 in model_names_phy.items():
        files_phy.append(f"PHY_results_{v2}_{v1}")
    
for _, v1 in attack_types_net.items():
    for _, v2 in model_names_netw.items():
        files_netw.append(f"NETW_results_{v2}_{v1}")

keys_to_keep = [
    "data",
    "model_type",
    "attack_type",
    "confusion_matrix",
    "precision",
    "recall",
    "tnr",
    "fpr",
    "accuracy",
    "f1",
    "balanced_accuracy",
    "mcc",
    "fit_time",
    "predict_time",
    "fit_memory_usage",
    "predict_memory_usage",
    "TP",
    "FP",
    "TN",
    "FN",
]

data_list = []

for file in files_phy:
    data = db[file]
    filtered_data = {
        key: (str(data[key]) if key == "confusion_matrix" else data[key])
        for key in keys_to_keep
        if key in data
    }
    filtered_data["filename"] = file
    data_list.append(filtered_data)

for file in files_netw:
    data = db[file]
    filtered_data = {
        key: (str(data[key]) if key == "confusion_matrix" else data[key])
        for key in keys_to_keep
        if key in data
    }
    filtered_data["filename"] = file
    data_list.append(filtered_data)


df_results = pd.DataFrame(data_list)
