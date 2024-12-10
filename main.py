#import library 
from fastapi import FastAPI, HTTPException, Header
#import dataframe
import pandas as pd

#create object /intance
app = FastAPI()

#create API KEY
API_key = "QWERTY"
#variabel bebas > STRING

#create endpoint > pintu gerbang
#endpoind home
@app.get("/")
        #home localhost
def home(): 
    return {"message": "Selamat datang di Toko Doyok"}
#Json > dict base
#bikin function 

#create endpoint data 
@app.get("/data")
def read_data():
#read data di endpoint berbeda
        #read data from file csv
    df = pd.read_csv("data.csv")
    #mengembalikan data df 
    return df.to_dict(orient="records")
    #ini belum bersih > membersihkan pakai records
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html#pandas.DataFrame.to_dict

#create endpoint data with number of parameter id
@app.get("/data/{number_id}")
def read_item(number_id: int):
    #read data from file csv
    df = pd.read_csv("data.csv")

    #filter data by id
    filter_data = df[df["id"] == number_id]
 
    #check filter data kosong/emty
    if len(filter_data) == 0:
    #memanggil kosong pakai len
        raise HTTPException(status_code=404, detail="Not Found Find Data")

    #mengembalikan data df 
    return filter_data.to_dict(orient="records")


#PUT update endpoint file csv data 
#update > put
@app.put("/items/{number_id}")
#bikin fucntion update_item > yang di tambah item_id > int, bentuk dict
def update_item(number_id: int, nama_barang: str, harga: float):
    #harus read ulang file.csv
    df = pd.read_csv("data.csv")

    #create dataframe from update input
    #create new database
    updated_df = pd.DataFrame({
        "id":number_id,
        "nama_barang":nama_barang,
        "harga":harga
    }, index=[0])
    #, index=[0]

    #merge ipdated dataframe with original dataframe
    #metode concat bisa di dalam list
    df = pd.concat([df, updated_df], ignore_index=True)
    #save updated dataframe > csv
    df.to_csv("data.csv", index=False)

    return {"message": f"Item dengan nama {nama_barang} berhasil di tambahkan "}

##GET Secret
@app.get("/secret")
#function def 
def read_secret(api_key: str = Header(None)):
    #nama class dari fast api > header > api
    #return 
    secret_df = pd.read_csv("secret_data.csv")
    if api_key != API_key:
        raise HTTPException(status_code=401, detail="API KEY NOT VALID")
    #jika api_key tidak sama dengan maka akan raised HTTPExprection
    return secret_df.to_dict(orient="records")