import sqlite3, os

class Jango():
    
    cursor = None
    con = None
    
    def __init__(self):
        
        if os.path.exists("../jango.db") == False:
            self.con = sqlite3.connect("../jango.db")
            self.cursor = self.con.cursor()
            self.create_table()
        else:
            self.con = sqlite3.connect("../jango.db")
            self.cursor = self.con.cursor()
            
    def create_table(self):
        self.cursor.execute("CREATE TABLE jango(subject_code text, meme_price real, mesu_medo text, flow text, how_many int, sonjalga real, date text, removed text)")
        
    def add_db_contract(self, subject_code, meme_price, mesu_medo, flow, how_many, sonjalga, date):
        list = [subject_code, meme_price, mesu_medo, flow, how_many, sonjalga, date,'false']
        self.cursor.execute("insert into jango values(?,?,?,?,?,?,?,?)",list)
        self.con.commit()
        
    def delete_db_contract(self, subject_code):
        sql = "UPDATE jango SET removed='true' WHERE subject_code=?"
        self.cursor.execute(sql,(subject_code,))
        self.con.commit()
        
    def update_db_contract(self, subject_code, how_many):
        sql = "UPDATE jango SET how_many=? WHERE subject_code=? and removed='false'"
        self.cursor.execute(sql,(how_many, subject_code,))
        self.con.commit()
        
    def get_db_jango(self, subject_code):
        rtn = self.cursor.execute("select * from jango where subject_code=? and removed='false'",(subject_code,))
        for r in rtn:
            dic = {}
            dic['subject_code'] = r[0]
            dic['매매가'] = r[1]
            dic['플로우'] = r[3]
            dic['잔고수량'] = r[4]
            dic['손절가'] = r[5]
            dic['주문일자'] = r[6]
            if r[2] == 'mesu':
                dic['매도수구분'] = '매수'            
            elif r[2] == 'medo':
                dic['매도수구분'] = '매도'
                
            print(dic)
            return dic
        #cursor.execute('INSERT INTO images VALUES(?)', (img,))
if __name__ == "__main__":
    
    #jg = Jango()
    #jg.select_jango('GCJ17')
    #jg.add_db_contract('GCJ17', 1120.2, 'up', 2, 1020.2, "20170221")
    #jg.delete_db_contract('GCJ17')
    pass