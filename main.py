import grade_1_2
import grade_3_4_5_6
import const

#得到一二年级书籍数据
grade_1_2.download_books(const.urls_low,const.headers)

#得到其他年级书籍数据
grade_3_4_5_6.download_books(const.urls_mid_and_high,const.headers)





