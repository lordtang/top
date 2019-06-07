import datetime


def get_sql(id_name,gender,age):
    str_id_name = str(id_name)
    if str_id_name.isdigit():
        if gender == '不限' and age == '不限':
            sql = "select user_id from user_tbl where user_id = %d or user_name like '%%%s%%'"%(id_name,str_id_name)
        elif gender == '不限' and age == '18岁以下':
            birth = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where user_id = %d or (user_name like '%%%s%%' and brith>'%s-00-00')"%(id_name,id_name,birth)
        elif gender == '不限' and age == '18-22岁':
            birth_start = datetime.date.today().year - 22
            birth_end = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where user_id = %d or (user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,id_name,birth_start,birth_end)
        elif gender == '不限' and age == '22-30岁':
            birth_start = datetime.date.today().year - 30
            birth_end = datetime.date.today().year - 22
            sql = "select user_id from user_tbl where user_id = %d or (user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,id_name,birth_start,birth_end)
        elif gender == '不限' and age == '30岁以上':
            sql = "select user_id from user_tbl where user_id = %d or (user_name like '%%%s%%' and brith<'%s-00-00')"%(id_name,id_name,birth)
        elif gender == '男' and age == '不限':
            sql = "select user_id from user_tbl where user_id = %d or (gender = 0 and user_name like '%%%s%%')"%(id_name,id_name)
        elif gender == '男' and age == '18岁以下':
            birth = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where user_id = %d or (gender = 0 and user_name like '%%%s%%' and brith>'%s-00-00')"%(id_name,id_name,birth)
        elif gender == '男' and age == '18-22岁':
            birth_start = datetime.date.today().year - 22
            birth_end = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where user_id = %d or (gender = 0 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,id_name,birth_start,birth_end)
        elif gender == '男' and age == '22-30岁':
            birth_start = datetime.date.today().year - 30
            birth_end = datetime.date.today().year - 22
            sql = "select user_id from user_tbl where user_id = %d or (gender = 0 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,id_name,birth_start,birth_end)
        elif gender == '男' and age == '30岁以上':
            birth = datetime.date.today().year - 30
            sql = "select user_id from user_tbl where user_id = %d or (gender = 0 and user_name like '%%%s%%' and brith<'%s-00-00')"%(id_name,id_name,birth)
        elif gender == '女' and age == '不限':
            sql = "select user_id from user_tbl where user_id = %d or (gender = 1 and user_name like '%%%s%%')"%(id_name,id_name)
        elif gender == '女' and age == '18岁以下':
            birth = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where user_id = %d or (gender = 1 and user_name like '%%%s%%' and brith>'%s-00-00')"%(id_name,id_name,birth)
        elif gender == '女' and age == '18-22岁':
            birth_start = datetime.date.today().year - 22
            birth_end = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where user_id = %d or (gender = 1 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,id_name,birth_start,birth_end)
        elif gender == '女' and age == '22-30岁':
            birth_start = datetime.date.today().year - 30
            birth_end = datetime.date.today().year - 22
            sql = "select user_id from user_tbl where user_id = %d or (gender = 1 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,id_name,birth_start,birth_end)
        elif gender == '女' and age == '30岁以上':
            birth = datetime.date.today().year - 30
            sql = "select user_id from user_tbl where user_id = %d or (gender = 1 and user_name like '%%%s%%' and brith<'%s-00-00')"%(id_name,id_name,birth)
    else:
        if gender == '不限' and age == '不限':
            sql = "select user_id from user_tbl where user_name like '%%%s%%'"%(id_name)
        elif gender == '不限' and age == '18岁以下':
            birth = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where (user_name like '%%%s%%' and brith>'%s-00-00')"%(id_name,birth)
        elif gender == '不限' and age == '18-22岁':
            birth_start = datetime.date.today().year - 22
            birth_end = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where (user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,birth_start,birth_end)
        elif gender == '不限' and age == '22-30岁':
            birth_start = datetime.date.today().year - 30
            birth_end = datetime.date.today().year - 22
            sql = "select user_id from user_tbl where (user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,birth_start,birth_end)
        elif gender == '不限' and age == '30岁以上':
            birth = datetime.date.today().year - 30
            sql = "select user_id from user_tbl where (user_name like '%%%s%%' and brith<'%s-00-00')"%(id_name,birth)
        elif gender == '男' and age == '不限':
            sql = "select user_id from user_tbl where (gender = 0 and user_name like '%%%s%%')"%(id_name)
        elif gender == '男' and age == '18岁以下':
            birth = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where (gender = 0 and user_name like '%%%s%%' and brith>'%s-00-00')"%(id_name,birth)
        elif gender == '男' and age == '18-22岁':
            birth_start = datetime.date.today().year - 22
            birth_end = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where (gender = 0 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,birth_start,birth_end)
        elif gender == '男' and age == '22-30岁':
            birth_start = datetime.date.today().year - 30
            birth_end = datetime.date.today().year - 22
            sql = "select user_id from user_tbl where (gender = 0 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,birth_start,birth_end)
        elif gender == '男' and age == '30岁以上':
            birth = datetime.date.today().year - 30
            sql = "select user_id from user_tbl where (gender = 0 and user_name like '%%%s%%' and brith<'%s-00-00')"%(id_name,birth)
        elif gender == '女' and age == '不限':
            sql = "select user_id from user_tbl where (gender = 1 and user_name like '%%%s%%')"%(id_name)
        elif gender == '女' and age == '18岁以下':
            birth = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where (gender = 1 and user_name like '%%%s%%' and brith>'%s-00-00')"%(id_name,birth)
        elif gender == '女' and age == '18-22岁':
            birth_start = datetime.date.today().year - 22
            birth_end = datetime.date.today().year - 18
            sql = "select user_id from user_tbl where (gender = 1 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,birth_start,birth_end)
        elif gender == '女' and age == '22-30岁':
            birth_start = datetime.date.today().year - 30
            birth_end = datetime.date.today().year - 22
            sql = "select user_id from user_tbl where (gender = 1 and user_name like '%%%s%%' and '%s-00-00'<=brith<='%s-00-00')"%(id_name,birth_start,birth_end)
        elif gender == '女' and age == '30岁以上':
            birth = datetime.date.today().year - 30
            sql = "select user_id from user_tbl where (gender = 1 and user_name like '%%%s%%' and brith<'%s-00-00')"%(id_name,birth)
    return sql