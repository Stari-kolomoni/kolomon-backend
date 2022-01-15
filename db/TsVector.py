from sqlalchemy.sql.type_api import UserDefinedType


class TsVector(UserDefinedType):
    name = "TSVECTOR"

    def get_col_spec(self):
        return self.name
