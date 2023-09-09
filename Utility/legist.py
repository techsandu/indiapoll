import pandas
import pandas as pd


def scrap_legist_data(data):
    print("entered to first line")

    df = pd.read_csv(data)
    print("success")
    # for i,j in df.iterrows():
    #     print(i)
    print("success")
if __name__ == "__main__":
    scrap_legist_data("Files/Kerala_2021.csv")