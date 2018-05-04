from django.db import models

# Create your models here.
class UserInfo(models.Model):
    '''
    用户表
    '''
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    head_img = models.FileField(verbose_name='头像', upload_to='upload', default="default.jpg",null=True,blank=True)
    phone = models.CharField(verbose_name="电话",max_length=11,blank=True,null=True)

    def __str__(self):
        return self.username

class MovieType(models.Model):
    """电影类型"""
    name = models.CharField(verbose_name="电影类型",max_length=32)

    def __str__(self):
        return self.name

class MovieDetail(models.Model):
    """电影详情"""
    name = models.CharField(verbose_name="电影名",max_length=32)
    period = models.CharField(verbose_name="电影时长",max_length=32)
    # img = models.CharField(verbose_name="电影图片",max_length=32)
    img = models.FileField(verbose_name='电影图片', upload_to='upload', default="default_film.jpg",null=True,blank=True)

    info = models.TextField(verbose_name="电影简介",max_length=255,null=True,blank=True)
    plot = models.TextField(verbose_name="电影剧情",max_length=1024,null=True,blank=True)
    company = models.CharField(verbose_name="发行公司",max_length=32,null=True,blank=True)

    score = models.CharField(verbose_name="电影评分", max_length=32,null=True,blank=True)
    comment_num = models.IntegerField(verbose_name="评分人数",null=True,blank=True,default=0)
    like_num = models.IntegerField(verbose_name="想看人数",null=True,blank=True,default=0)
    share_num = models.IntegerField(verbose_name="转发人数",null=True,blank=True,default=0)
    other_name = models.CharField(verbose_name="更多片名",max_length=32,null=True,blank=True)
    release = models.DateField(verbose_name="上映时间",null=True,blank=True)

    mtype = models.ManyToManyField(verbose_name="电影类型",to='MovieType')

    def __str__(self):
        return self.name

class Worker(models.Model):
    """电影相关人员"""
    name = models.CharField(verbose_name="扮演者",max_length=32)

    act_chocies = ((1,"导演"),(2,"编剧"),(3,"演员"))
    Actor = models.IntegerField(verbose_name="职责",choices=act_chocies)
    role = models.CharField(verbose_name="扮演角色",max_length=32,blank=True,null=True)
    # act_img = models.CharField(verbose_name="演员图片",max_length=64,blank=True,null=True)
    act_img = models.FileField(verbose_name='演员图片', upload_to='upload', default="default.jpg",null=True,blank=True)

    # role_img = models.CharField(verbose_name="角色图片",max_length=64,blank=True,null=True)
    role_img = models.FileField(verbose_name='角色图片', upload_to='upload', default="default.jpg",null=True,blank=True)

    movie = models.ForeignKey(verbose_name="关联电影",to='MovieDetail',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comment(models.Model):
    """电影评论表"""

    content = models.TextField(verbose_name="评论内容",max_length=255,blank=True,null=True)
    up_count = models.IntegerField(default=0,verbose_name="赞")
    down_count = models.IntegerField(default=0,verbose_name="踩")
    create_data = models.DateTimeField(verbose_name="评论时间",auto_now_add=True)

    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="评论者",to="UserInfo",on_delete=models.CASCADE)
    movie = models.ForeignKey(verbose_name="评论电影",to="MovieDetail",on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%s"%(self.user.username,self.content)

class Cinema(models.Model):
    """电影院表"""

    title = models.CharField(verbose_name="电影院名",max_length=64)
    addr = models.CharField(verbose_name="地址",max_length=128)

    def __str__(self):
        return self.title
    # imax_choices = (
    #     (1,"有"),
    #     (2,"无")
    # )
    # M_IMAX = models.IntegerField(verbose_name="IMAX",choices=imax_choices)
    #
    #
    # m3d_choices = (
    #     (1,"有"),
    #     (2,"无")
    # )
    # M_3D =models.IntegerField(verbose_name="3D",choices=m3d_choices)
    #
    # glasses_choices = (
    #     (1, "有"),
    #     (2, "无")
    # )
    # M_FreeGlasses = models.IntegerField(verbose_name="3D", choices=glasses_choices)

class MovieField(models.Model):
    """电影场次表"""
    start_time = models.CharField(verbose_name="开始时间",max_length=32)
    price = models.IntegerField(verbose_name="票价",default=0)

    play_date = models.DateField(verbose_name="播放日期")
    ballot = models.IntegerField(verbose_name="票数")

    movie = models.ForeignKey(verbose_name="影片",to="MovieDetail",on_delete=models.CASCADE)
    cinema = models.ForeignKey(verbose_name="电影院",to="Cinema",on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%s"%(self.movie.name ,self.start_time)

class PlayRoom(models.Model):
    """播放大厅"""
    caption = models.CharField(verbose_name="播放厅名",max_length=32)
    cinema = models.ForeignKey(verbose_name="关联电影院",to="Cinema",on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

class Order(models.Model):
    """订单"""
    payment_type_choices = ((0,"微信"),(1, '支付宝'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices,verbose_name="支付方式")
    payment_number = models.CharField(max_length=128, verbose_name="支付第3方订单号", null=True, blank=True)
    order_number = models.CharField(max_length=128, verbose_name="订单号", unique=True)  # 考虑到订单合并支付的问题

    user = models.ForeignKey(to="UserInfo",on_delete=models.CASCADE,verbose_name="支付人")
    actual_amount = models.FloatField(verbose_name="实付金额")

    status_choices = ((0, '交易成功'), (1, '待支付'), (2, '退费申请中'), (3, '已退费'), (4, '主动取消'), (5, '超时取消'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="订单生成时间")
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name="付款时间")
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name="订单取消时间")

    def __str__(self):
        return "%s" % self.order_number

class OrderDetail(models.Model):
    """订单详情"""
    order = models.ForeignKey("Order",on_delete=models.CASCADE,verbose_name="关联订单")
    moviefield = models.ForeignKey(to="MovieField",on_delete=models.CASCADE,verbose_name="影片场次")
    original_price = models.FloatField("电影票原价")
    seat_row = models.IntegerField(verbose_name="行")
    seat_col = models.IntegerField(verbose_name="列")
    content = models.CharField(max_length=255, blank=True, null=True)  # ？
    valid_period_display = models.CharField("有效期显示", max_length=32,null=True,blank=True)  # 在订单页显示
    valid_period = models.PositiveIntegerField("有效期(days)",null=True,blank=True)  # 课程有效期

    def __str__(self):
        return self.moviefield.movie.name

