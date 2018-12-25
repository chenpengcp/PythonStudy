import urllib.request
import json
import pymysql


def insert_data(title, play, comment, favorites, video_review, team, party):
    db = pymysql.connect(host="*",
                         user="*",
                         passwd="*",
                         port=3306,
                         db="peo",
                         charset='utf8')
    cursor = db.cursor()
    start = "INSERT INTO bili1 (title,play,comment,favorites,video_review,team,party) VALUES ("
    mid = "','"
    end = ")"
    sql = start + "'" + title + mid + play + mid + comment + mid + favorites + mid + video_review + mid + team + mid + party + "'" + end
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("success")
    except:
        # 如果发生错误则回滚
        print("??")
        db.rollback()
    db.close()


def get_html(size, page):
    start = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=1315101&pagesize="
    end = "&keyword=&order=pubdate"
    response = urllib.request.urlopen(
        start + size + "&tid=0&page=" + page +
        end)
    html = response.read().decode("utf-8")
    json_data = json.loads(html)
    data = json_data["data"]
    v_list = data["vlist"]
    # print(v_list)
    return v_list


def get_data(size, page):
    v_list = get_html(size, page)
    for i in v_list:
        ss = i["title"]
        if "Mini Live" not in ss and "生日会" not in ss and "预备生" not in ss and "Team" in ss:
            if "《" in ss:
                team = ss[ss.index("T"):ss.index("《")]
            else:
                team = ss[ss.index("T"):ss.index("T") + 8]
            party = ss[ss.index("8") - 4:ss.index("8") + 1]
            # party.index()
            insert_data(ss, str(i["play"]), str(i["comment"]), str(i["favorites"]), str(i["video_review"]),
                        team,
                        party)


for i in range(23):
    get_data("30", str(i))
