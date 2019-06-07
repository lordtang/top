一.实体：用户 user_tbl
    字段： id user_name  user_tel register_date birthday gender  account passwd last_time status ip port
    1.登录：查询用户名和密码是否匹配
    flag = 0
    sql =  "select * from %s where name = '%s' and passwd = '%s' "%(user_tbl,name,passwd)
    data = list
    2.注册:查询用户名不重复
    flag = 0
    sql =  "select * from %s where name = '%s'"%(table_user,user_name)
    data = list
    注册成功后 插入信息
    flag = 1
    sql_insert_info = "insert into table_user(user_name,passwd,gender,birth,user_tel,status,user_ip,\                               user_tcp_port,last_time)values('%s','%s','%s',date,'%s',1,'%s','%s',time.time())"\
                                %(user_name,passwd,gender,birth,user_tel,self.ip,self.port)
    data = True/False
    3.找回密码：
    flag = 0
    sql =  "select * from %s where name = '%s' and user_tel = '%s'"%(table_user,user_name,tel_no)
    找回密码成功后
    flag = 1
    sql = 'insert into %s() values()'
    data = True/False
插入测试数据：
insert into user_tbl(user_name,passwd,gender,brith,user_tel,user_stat,user_ip, user_tcp_port,user_udp_port,last_time)values('%s','%s','%s',date,'%s',1,'%s','%s',time.time)%(user_name,passwd,gender,birth,user_tel,self.ip,self.port)

insert into user_tbl(user_name,passwd,gender,brith,user_tel,user_stat,user_ip, user_tcp_port,user_udp_port,last_time)values("xiaohan",'123456','1','1992-07-14','18782211636','0','176.209.108.38',8080,8080,now());
#用户好友实体
create table user_friends(
    id int(10) primary key auto_increment,
    friend_id int(10) unsigned not null,
    owner_id int(10) unsigned not null,
    join_date datetime,
    constraint fk_friend_id foreign key(friend_id) references user_tbl(user_id),
    constraint fk_owner_id foreign key(owner_id) references user_tbl(user_id)
)ENGINE=InnoDB AUTO_INCREMENT=40000 DEFAULT CHARSET=utf8;
#消息记录实体
create table user_msg_content(
    id int(32) primary key auto_increment,
    send_user_id int(10) unsigned not null,
    recv_user_id int(10) unsigned not null,
    content text,
    content_type int,
    send_time datetime,
    constraint fk_send_user_id foreign key(send_user_id) references user_tbl(user_id),
    constraint fk_recv_user_id foreign key(recv_user_id) references user_tbl(user_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#用户群实体
create table user_groups(
    user_group_id int primary key  auto_increment,--群号
    user_group_name  varchar(128) not null,
    user_group_createtime datetime,
    user_admin_user_id  int(10) unsigned not null,
    user_group_notice varchar(200),
    user_intro    varchar(200),
    user_files   text,
    constraint fk_user_admin_user_id foreign key(user_admin_user_id) references user_tbl(user_id)
)ENGINE=InnoDB AUTO_INCREMENT=100000 DEFAULT CHARSET=utf8;


#群用户关联表
create table user_groups_to_user(
    id int primary key auto_increment,
    user_group_user_id int(10) unsigned not null,
    user_group_id int not null,
    join_date datetime,
    user_group_user_nick Varchar(15),
    constraint fk_user_group_user_id foreign key(user_group_user_id) references user_tbl(user_id),
    constraint fk_user_group_id foreign key(user_group_id) references user_group(user_group_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#群消息发送方内容关联
create table user_groups_msg_content(
    id int primary key auto_increment,
    msg_content text not null,
    send_user_id int(10) unsigned not null,
    send_user_group_id int not null,
    send_user_name varchar(30),
    send_time datetime,
    constraint refk_send_user_id foreign key(send_user_id) references user_tbl(user_id),
    constraint fk_send_user_group_id foreign key(send_user_group_id) references user_group(user_group_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#群消息接收方关联表(对方不在线时　在线时就不管接收到与否)
create table user_groups_msgtouer(
    id int primary key auto_increment,
    recv_group_user_id int(10) unsigned not null,
    msg_content_id int not null,
    send_group_msgtime datetime
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#群内私聊消息关联表(对方不在线时在线时就不管接收到与否　两个客户端之间的聊天)
create table user_groups_msgtoperson(
    id int primary key auto_increment,
    send_user_id int(10) unsigned not null,
    send_user_name vachar(30),
    recv_user_id int(10) unsigned not null,
    user_group_id int not null,
    msg_content varchar(300),
    send_time datetime,
    constraint reusefk_send_user_id foreign key(send_user_id) references user_tbl(user_id),
    constraint reusefk_recv_user_id foreign key(recv_user_id) references user_tbl(user_id),
    constraint refk_user_group_id foreign key(user_group_id) references user_group(user_group_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#用户头像
create table user_logo(
    id int primary key auto_increment,
    logo_pic mediumblob
)ENGINE=InnoDB DEFAULT CHARSET=utf8;