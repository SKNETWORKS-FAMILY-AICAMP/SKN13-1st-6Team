import pymysql
from Car import Car

class DbConnection:
    def __init__(self, host="192.168.0.15", uid="user4", pw="9999", db_name="test_db"):
        self.host = host
        self.uid = uid
        self.pw = pw
        self.db_name = db_name

    def select_all_data(self,mode:str = "") -> list | None:
        result = ""
        if mode == "500만원~2000만원":
            result = "WHERE price BETWEEN 1 AND 2000"
        elif mode == "2000만원~3000만원":
            result = "WHERE price BETWEEN  1 AND 3000"
        elif mode == "3000만원~5000만원":
            result = "WHERE price BETWEEN 3000 AND 5000"
        elif mode == "5000만원~8000만원":
            result = "WHERE price BETWEEN 5000 AND 8000"
        elif mode == "8000만원 이상":
            result = "WHERE price >= 8000;"
        
        #["500만원~2000만원", "2000만원~3000만원", "3000만원~5000만원", "5000만원~8000만원", "8000만원 이상"]
        
        sql = "SELECT * FROM car_info " + result

        cars = []

        try:
            # 커넥션 열기
            conn = pymysql.connect(
                host=self.host,
                port=3306,
                user=self.uid,
                password=self.pw,
                db=self.db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.Cursor  # 또는 DictCursor 원할 시 변경
            )

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    print("조회행수:", cursor.rowcount)
                    for row in cursor.fetchall():
                        if len(row) < 11:
                            row = row + ("",) * (11 - len(row))  # 부족한 필드를 빈 문자열로 채움
                        #car = Car(*row)
                        car = Car(*row)
                        cars.append(car)

        except pymysql.MySQLError as e:
            print("DB 오류:", e)
            return None

        return cars