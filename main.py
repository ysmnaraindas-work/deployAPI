# import libraby
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

# create object
app = FastAPI()

API_KEY = "cobaajaduluyak8"
# create endpoint home
@app.get("/")
def home():
    return {"message": "Selamat Datang di alam semesta"}

# create endpoint data
@app.get("/data")
def read_data():
    # baca data dari csv
    df = pd.read_csv("data.csv")
    # mengembalikan ke data dict with orient='records' for each row
    return df.to_dict(orient='records')


# create endpoin{t data with parameter number of parameter id
@app.get("/data/{number_id}")
def read_item(number_id: int):
    df = pd.read_csv("data.csv")
    # filter data by id
    filter_data = df[df["id"] == number_id]
    # cek fill data empty
    if len(filter_data) == 0:
        raise HTTPException(status_code=404, detail="sorry skip")

    # mengembalikan ke data dict with orient='records' for each row
    return filter_data.to_dict(orient='records')


@app.put("/items/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):
    df = pd.read_csv("data.csv")
    #create new_dataFrame with update values
    updated_data = pd.DataFrame([{
        "id": number_id,
        "nama_barang": nama_barang,
        "harga":harga
    }])
    # menggabungkan data lama dengan update an data baru
    df = pd.concat([df, updated_data], ignore_index=True)
    # Perform the update using the data from the request body
    df.to_csv("data.csv", index=False)

    return {"message": f"Item with ID {number_id} has been updated successfully."}


@app.get("/secret")
def read_secret(api_key: str = Header(None)):
    secret_df = pd.read_csv("secret_data.csv")
    # mengecek apakah api_key tidak sama dengan API_KEY
    if api_key != API_KEY:
        # maka akan muncul message ini
        raise HTTPException(status_code=401, detail="API Key tidak Valid jadi sorry skip")

    return secret_df.to_dict(orient='records')