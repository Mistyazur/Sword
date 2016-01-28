import sqlite3
import requests
import json


class QuestionArchvie(object):

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabets = list(alphabet)

    def __init__(self):
        super(QuestionArchvie, self).__init__()
        self.conn = 0
        self.cur = 0

    def request(self, key):
        try:
            r = requests.get("http://huodong.duowan.com/wxdatiqi/backend/index.php", params={
                             "r": "index/GetQuestionByKeyword", "callback": "jsonpReturn", "keyword": key})
            if r.text != "jsonpReturn(null);":
                text = r.text[13:-3]
                text = text.replace("<font color=\\\"red\\\">", "")
                text = text.replace("<\\/font>", "")
                text = text.replace("},{", "},,,{")
                answer_list = text.split(",,,")
                if len(answer_list) < 50:
                    for answer in answer_list:
                        # print(answer)
                        j = json.loads(answer)
                        # try:
                        self.cur.execute("INSERT INTO Questions (question, answer) values (\"%s\", \"%s\")" % (
                            j["question"], j["answer"]))
                        # except Exception:
                        #     pass
                else:
                    for a in self.alphabets:
                        self.request(key + a)
        except Exception:
            pass

    def getArchiveFromDw(self):
        self.conn = sqlite3.connect("sword_dw.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question varchar(255) UNIQUE, answer varchar(255))")

        for a in self.alphabets:
            for b in self.alphabets:
                self.request(a + b)

        self.cur.close()
        self.conn.commit()
        self.conn.close()

    # def GetArchvieFromSina(self):
    #     # Open datebase
    #     self.conn = sqlite3.connect("sword.db")
    #     self.cur = self.conn.cursor()
    #     self.cur.execute(
    #         "CREATE TABLE IF NOT EXISTS Questions (id INTEGER PRIMARY KEY AUTOINCREMENT, question varchar(255) UNIQUE, answer varchar(255))")

    #     # Save archive to database
    #     res = requests.get("http://games.sina.com.cn/o/z/wuxia/date_td_qs.js")
    #     j = json.loads(res.text.encode("gbk", "ignore").decode("gbk")[16:])
    #     # json.loads(res.text.encode("gbk", "ignore").decode("gbk")[16:])
    #     for qid, qa in j["xlinfo"].items():
    #         question = qa["question"]
    #         answer = qa["opt1"]
    #         try:
    #             self.cur.execute(
    #                 "INSERT INTO Questions (question, answer) values (\"%s\", \"%s\")" % (question, answer))
    #         except sqlite3.IntegrityError:
    #             print(question)

    #     # Close datebase
    #     self.cur.close()
    #     self.conn.commit()
    #     self.conn.close()


if __name__ == "__main__":
    q = QuestionArchvie()
    q.getArchiveFromDw()
