import app
# app.main()


import config as c
import sim900 as s

def test1():
    data = {"hwid":"test","t":1,"p":999}
    rc = s.submit_data(c.SUBMIT_URL, (c.SUBMIT_USER, c.SUBMIT_PASS), data)
    return rc
