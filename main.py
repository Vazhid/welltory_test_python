import openai
import pandas as pd


API_KEY = ""
FILE_NAME = "query.txt"


def query_from_txt_run(filename: str) -> str:
    openai.api_key = API_KEY

    with open(filename) as f:
        query = f.read()

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query}
        ]
    )

    return completion.choices[0].message.content


def main():
    arr = query_from_txt_run(FILE_NAME).split("\n")

    data = pd.read_csv("data.csv")

    for elem in arr:
        tmp_arr = elem.split(" - ")
        if len(tmp_arr) == 2:
            data['rate'].where(~(data.email == tmp_arr[0]), other=int(tmp_arr[1]), inplace=True)

    print(data.head(10))
    data.to_csv("data_analyzed.csv")


if __name__ == '__main__':
    main()
