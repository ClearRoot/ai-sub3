from sqlalchemy import Column, Integer, String, DateTime 
from database import Base 

class TbTest(Base):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    __tablename__ = 'tbTable' 
    
    id = Column(Integer, primary_key=True) 
    datetime = Column(DateTime) 
    string = Column(String(250)) 
    
    def __init__(self, datetime=None, string=None): 
        self.datetime = datetime 
        self.string = string 
        
    def __repr__(self): 
        return "<TbTest('%d', '%s', '%s')>" %(self.id, str(self.datetime), self.string)