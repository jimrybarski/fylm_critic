import sqlite3
from model.offset import RegistrationOffsets, RotationOffsets
from model.coordinates import Point


class Database(object):
    def __init__(self, database_path: str):
        self._database_path = database_path

    @property
    def conn(self):
        return sqlite3.connect(self._database_path)

    def save(self, obj):
        table_name = obj.__class__.__name__.lower()
        obj.df.to_sql(table_name, self.conn, flavor='sqlite', if_exists='replace')

    def load_registration_offsets(self) -> RegistrationOffsets:
        offsets = RegistrationOffsets()
        try:
            cursor = self.conn.execute("""SELECT field_of_view, frame_number, x, y FROM registrationoffsets""")
            for field_of_view, frame_number, x, y in cursor.fetchall():
                offsets.set(field_of_view, frame_number, Point(x=x, y=y))
        except:
            return None
        return offsets

    def load_rotation_offsets(self) -> RotationOffsets:
        offsets = RotationOffsets()
        try:
            cursor = self.conn.execute("""SELECT field_of_view, offset FROM rotationoffsets""")
            for field_of_view, offset in cursor.fetchall():
                offsets.set(field_of_view, offset)
        except:
            return None
        return offsets
