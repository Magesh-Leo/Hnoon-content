from fastapi import Request, FastAPI
from app.scrapData import sentUrl

app=FastAPI()

@app.post("/")
async def get_body(request: Request):
    req_info = await request.json()
    uid = req_info["message"]["attributes"]["urlId"]
    url = req_info["message"]['attributes']['inputLink']
    resp_info = sentUrl(uid=uid,url=url)
    return {"Response":resp_info}
    
