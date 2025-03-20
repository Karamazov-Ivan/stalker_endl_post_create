class SqlTextureDB:

    def create_tab(self, con):
        with con:
            try:
                con.execute('DROP TABLE TEXTURE_TABLE')
            except:
                print('Таблица TEXTURE_TABLE не существует')
            con.execute("""
                CREATE TABLE TEXTURE_TABLE (
                    name TEXT
                    ,TIMESTAMP_2 DEFAULT (datetime('now','localtime'))
                    ,path TEXT
                    --,magazine TEXT
                    --,rare TEXT
                    --,numb TEXT
                    --,TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        print('Таблица TEXTURE_TABLE создана')

    def insert_data(self, con, data):
        sql = 'INSERT INTO TEXTURE_TABLE (name, path) values(?, ?)'
        with con:
            con.executemany(sql, data)
        print('Данные текстур внесены в БД')

    def select_from(self, con, direct_quer=0, query_num=0):

        cursor = con.cursor()

        if query_num == 1:
            res = cursor.execute('''
                SELECT *
                FROM (
                    SELECT
                        name
                        ,SUBSTRING(name, 7, 2) AS mag
                        ,SUBSTRING(name, 10, 1) AS rare
                        ,SUBSTRING(name, 12, 4) AS numb
                        ,path
                        ,RANK() OVER (PARTITION BY SUBSTRING(name, 7, 2) ORDER BY SUBSTRING(name, 10, 1) DESC, SUBSTRING(name, 12, 4))
                    FROM TEXTURE_TABLE
                ) AS result_t
                --WHERE rare = '3'
            ''')
            return res.fetchall()
        
        elif query_num == 2:
            res = cursor.execute('''
                SELECT name
                FROM TEXTURE_TABLE
            ''')
            return res.fetchall()
        
        elif direct_quer:
            res = cursor.execute(direct_quer)
            return res.fetchall()
        
        else:
            res = cursor.execute('SELECT * FROM TEXTURE_TABLE')
            return res.fetchall()

        # if fetch:
        #     for row in res:
        #         print(row)

    def delete_from(self, con):
        with con:
            delete_table = 'TEXTURE_TABLE'
            con.execute(f'DELETE FROM {delete_table}')
            # con.close()
        print(f'Таблица {delete_table} очищена')