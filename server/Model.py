import sqlite3, os, re
from datetime import datetime, timezone

class Model:
    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path, check_same_thread=False)
    
    def insert_comic(self, params):
        drive = params['drive']
        updateDate = params['timestamp']
        size = params['size']
        isFolder = params['isFolder']
        name = re.sub("'", "''", params['name'])


        info = 'NULL' if params['info'] is None else "'%s'" % params['info']
        picCount = 'NULL' if params['picCount'] is None else str(params['picCount'])

        updateDate = datetime.fromtimestamp(updateDate)
        updateDate = updateDate.astimezone(timezone.utc)
        updateDate = updateDate.strftime('%Y-%m-%d %H:%M:%S')

        cmd = '''
            INSERT INTO 
            Record 
            ( Drive, UpdateDate, Size, IsFolder, ComicName, PicCount, Info )
            VALUES
            ( '%s', '%s', %d, %d, '%s', %s, %s )
        ''' % (drive, updateDate, size, isFolder, name, picCount, info)
        
        cursor = self.con.cursor()
        cursor.execute(cmd)
        self.con.commit()
        cursor.close()

    def update_info(self, params):
        target_id = params['id']
        info = params['info']

        cmd = '''
            UPDATE 
            Record
            SET Info = '%s'
            WHERE ID = %d
        ''' % (info, target_id)

        cursor = self.con.cursor()
        cursor.execute(cmd)
        self.con.commit()
        cursor.close()

    def search_target_commics(self, keyword):
        cmd = '''
            SELECT
            ID, Drive, UpdateDate, Size, IsFolder, ComicName, PicCount, Info
            FROM
            Record
            WHERE
            LOWER(ComicName) LIKE '%%%s%%'
        ''' % keyword.lower()
        cursor = self.con.cursor()
        cursor.execute(cmd)
        rst = cursor.fetchall()
        cursor.close()
        return rst

    def get_single_commic(self, comic_name):
        cmd = '''
            SELECT
            ID, Drive, UpdateDate, Size, IsFolder, ComicName, PicCount, Info
            FROM
            Record
            WHERE
            ComicName = '%s'
        ''' % re.sub("'", "''", comic_name)

        cursor = self.con.cursor()
        cursor.execute(cmd)
        rst = cursor.fetchall()
        cursor.close()
        return rst