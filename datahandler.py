import sqlite3

class Levelling():
    # Get a member's XP
    def getxp(self, memberid: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("SELECT xp FROM LEVELLING WHERE user_id = ?", (memberid,))
            return(cursor.fetchone()[0])
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Set a member's XP
    def setxp(self, memberid: int, amount: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("UPDATE LEVELLING SET xp = MAX(?, 0) WHERE user_id = ?", (amount, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Add to a member's XP
    def addxp(self, memberid: int, amount: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("UPDATE LEVELLING SET xp = xp + ? WHERE user_id = ?", (amount, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Take from a member's XP
    def takexp(self, memberid: int, amount: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("UPDATE LEVELLING SET xp = MAX(xp - ?, 0) WHERE user_id = ?", (amount, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Get a member's level
    def getlevel(self, memberid: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("SELECT level FROM LEVELLING WHERE user_id = ?", (memberid,))
            return(cursor.fetchone()[0])
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Set a member's level
    def setlevel(self, memberid: int, amount: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("UPDATE LEVELLING SET level = MAX(?, 0) WHERE user_id = ?", (amount, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Add to a member's level
    def addlevel(self, memberid: int, amount: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            
            cursor.execute("UPDATE LEVELLING SET level = level + ? WHERE user_id = ?", (amount, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Take from a member's level
    def takelevel(self, memberid: int, amount: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            
            cursor.execute("UPDATE LEVELLING SET level = MAX(level - ?, 0) WHERE user_id = ?", (amount, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Get a member's last message timestamp
    def getlastmessage(self, memberid: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("SELECT lastmessage FROM LEVELLING WHERE user_id = ?", (memberid,))
            return(cursor.fetchone()[0])
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Set a member's last message timestamp
    def setlastmessage(self, memberid: int, timestamp: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("UPDATE LEVELLING SET lastmessage = MAX(?, 0) WHERE user_id = ?", (timestamp, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Get a member's last reaction timestamp
    def getlastreaction(self, memberid: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("SELECT lastreact FROM LEVELLING WHERE user_id = ?", (memberid,))
            return(cursor.fetchone()[0])
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Set a member's last reaction timestamp
    def setlastreaction(self, memberid: int, timestamp: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("UPDATE LEVELLING SET lastreact = MAX(?, 0) WHERE user_id = ?", (timestamp, memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")
    
    # Get if a member was AFK in the last VC cycle
    def getlastvcafk(self, memberid: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("SELECT afklastvc FROM LEVELLING WHERE user_id = ?", (memberid,))
            return(bool(cursor.fetchone()[0]))
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Set if a member was AFK in the last VC cycle
    def setlastvcafk(self, memberid: int, state: bool):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("SELECT 1 FROM LEVELLING WHERE user_id = ?", (memberid,))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute("INSERT INTO LEVELLING (user_id) VALUES (?)", (memberid,))
                db.commit()
            cursor.execute("UPDATE LEVELLING SET afklastvc = MAX(?, 0) WHERE user_id = ?", (int(state), memberid))
            db.commit()
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")

    # Get the x top members levels/xp
    def xptop(self, amount: int):
        try:
            db = sqlite3.connect('userdata.db')
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS LEVELLING (
                user_id INTEGER PRIMARY KEY,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                lastmessage INTEGER DEFAULT 0,
                lastreact INTEGER DEFAULT 0,
                afklastvc INTEGER DEFAULT 0
            )
            """)
            cursor.execute("""
                SELECT user_id FROM LEVELLING
                ORDER BY level DESC, xp DESC
                LIMIT ?
            """, (amount,))
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as error:
            print(f"SQL ERROR: {error}")