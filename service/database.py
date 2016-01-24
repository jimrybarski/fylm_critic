import sqlite3
from model.offset import RegistrationOffsets, RotationOffsets
from model.coordinates import Point


class Database(object):
    def __init__(self, database_path: str):
        self._conn = sqlite3.connect(database_path)

    def save(self, obj):
        table_name = obj.__class__.__name__.lower()
        obj.df.to_sql(table_name, self._conn, flavor='sqlite', if_exists='replace')

    @property
    def registration(self) -> RegistrationOffsets:
        offsets = RegistrationOffsets()
        cursor = self._conn.execute("""SELECT field_of_view, frame_number, x, y FROM registrationoffsets""")
        for field_of_view, frame_number, x, y in cursor.fetchall():
            offsets.set(field_of_view, frame_number, Point(x=x, y=y))
        return offsets

    @property
    def rotation(self) -> RotationOffsets:
        offsets = RotationOffsets()
        cursor = self._conn.execute("""SELECT field_of_view, offset FROM rotationoffsets""")
        for field_of_view, offset in cursor.fetchall():
            offsets.set(field_of_view, offset)
        return offsets
