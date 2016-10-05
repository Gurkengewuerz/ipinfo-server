"""
    @AUTHOR: Gurkengewuerz
    @REVIEW: 05.10.2016
    @DESCRIPTION: An API for IPINFO with Cache Function
"""

from Config import DB, DATA_EXPIRE
import socket
import time
import requests


class IPValidator:
    @staticmethod
    def is_valid_ipv4_address(address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True

    @staticmethod
    def is_valid_ipv6_address(address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True


class Cache:
    @staticmethod
    def exists(ip):
        cur = DB.retrieve(
            "SELECT * FROM data_storage WHERE date > %s AND ip = '%s'" % (
                int(time.time()) - DATA_EXPIRE, ip)).fetchall()
        return len(cur) >= 1

    @staticmethod
    def getCache(ip):
        cur = DB.retrieve(
            "SELECT * FROM data_storage WHERE date > %s AND ip = '%s'" % (
                int(time.time()) - DATA_EXPIRE, ip)).fetchall()
        return cur

    @staticmethod
    def insert(ip, hostname, org, country, region, city, postal, loc):
        DB.sql_do(
            (
                "INSERT INTO data_storage (`date`,`ip`,`hostname`,`org`,`country`,`region`,`city`,`postal`,`loc`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %
                (int(time.time()), ip, hostname, org, country, region, city, postal, loc)))


class RequestManager:
    def __init__(self, ip):
        self.status = "OK"
        self.ip = ip
        self.where = "UNKNOWN"
        self.reponse = {"ip": "UNKNOWN", "hostname": "UNKNOWN", "org": "UNKNOWN",
                        "country": "UNKNOWN", "region": "UNKNOWN", "city": "UNKNOWN", "postal": "UNKNOWN",
                        "loc": "UNKNOWN"}

    def makeRequest(self, forceNoCache=False):
        if Cache().exists(self.ip) and not forceNoCache:
            cur = Cache().getCache(self.ip)
            for attribute in dict(cur[0]):
                self.reponse[attribute] = dict(cur[0])[attribute]
            self.status = "Answer from Cache"
        else:
            response_ipinfo = requests.get("https://ipinfo.io/" + self.ip)
            for attribute in response_ipinfo.json():
                self.reponse[attribute] = response_ipinfo.json()[attribute]
            Cache().insert(self.reponse["ip"], self.reponse["hostname"], self.reponse["org"], self.reponse["country"],
                           self.reponse["region"], self.reponse["city"], self.reponse["postal"], self.reponse["loc"])
            if forceNoCache:
                self.status = "Answer from IPINFO with force NO Cache"
            else:
                self.status = "Answer from IPINFO"
        return self.reponse

    def getStatus(self):
        return self.status

    def getResponse(self):
        return self.reponse
