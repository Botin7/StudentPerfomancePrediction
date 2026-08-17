@app.post("/upload")
def upload_file(file: UploadFile):

    file_path = "uploads/latest.csv"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"message": "uploaded successfully"}