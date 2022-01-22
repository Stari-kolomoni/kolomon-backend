from sqlalchemy.orm import Session


class UsersDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    #async def get_all_users(self, params) -> (List[schema.User]):
