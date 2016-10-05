"""
    @AUTHOR: Gurkengewuerz
    @REVIEW: 05.10.2016
    @DESCRIPTION: An API for IPINFO with Cache Function
"""

from DB import Database

PORT = 8082
DATA_EXPIRE = 14 * 24 * 60 * 60  # seconds
DB = Database(filename='data.db')
