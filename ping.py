# ping

import subprocess
import os
import datetime
import time

from my_db import MyDb

hosts = {
    "external": "www.ua",
    "router": "192.168.1.1",
    "old_hik": "192.168.1.64",
    "bullet": "192.168.1.70",
    "door_bell": "192.168.1.165"
}


def ping(host: str, n: int = 3):
    results = {"host": host, "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               "OK": False,
               "loss(%)": 100,
               "min": -1.0, "avg": -1.0, "max": -1.0, "mdev": -1.0,
               }
    try:
        ping_answer: str = subprocess.check_output(
            [f"ping {host} -c {n} -q"],
            universal_newlines=True,
            shell=True,
            stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        # results["OK"] = False
        # by default the results have already been set to connection broken
        pass
    else:
        results["OK"] = True
        answer_lines = ping_answer.splitlines(keepends=False)
        results["loss(%)"] = int(answer_lines[-2].split(sep=' ')[5][:-1])
        rtt_indicators = answer_lines[-1].split(sep=' ')[1].split(sep='/')
        rtt_values = answer_lines[-1].split(sep=' ')[3].split(sep='/')
        for indicator, value in zip(rtt_indicators, rtt_values):
            results[indicator] = float(value)
    return results

def create_table(db:MyDb):
    query = """
        create table if not exists ping (
          host varchar(20),
          time datetime,
          ok bool,
          loss float,
          min_rtt float,
          avg_rtt float,
          max_rtt float,
          mdev_rtt float
          )
          """
    db.exec(query)

def count_ping_items(db:MyDb):
    query = """
        select count(*)
        from ping
    """
    db.exec(query)

def insert_ping_item(db:MyDb,ping_res):
    query = f"""
        insert into ping values(
            "{ping_res['host']}", "{ping_res['time']}", {str(ping_res['OK']).upper()},
            "{ping_res['loss(%)']}", 
            "{ping_res['min']}","{ping_res['avg']}","{ping_res['max']}","{ping_res['mdev']}"
        )
    """
    # print(query)
    db.exec(query)

def main():
    db = MyDb()
    create_table(db)
    count_ping_items(db)
    while True:
        for host_name in hosts:
            res = ping(hosts[host_name])

            insert_ping_item(db,res)
            print(datetime.datetime.now(), res)
        time.sleep(10)


if __name__ == "__main__":
    main()
