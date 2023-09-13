CREATE TABLE Record (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Drive NVARCHAR(20) NOT NULL,
    UpdateDate DATETIME NOT NULL,
    Size INTEGER NOT NULL,
    IsFolder BIT NOT NULL,
    ComicName TEXT NOT NULL,

    -- if the target comic is folder, get the picture count
    PicCount INTEGER,

    --record the update infomation, store json
    Info TEXT
)