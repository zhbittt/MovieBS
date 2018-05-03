from stark.service import v1
from film import models
import datetime
# show_edit_link = False
# edit_link = [点击修改字段]

# list_display = [列表展示字段]

# show_add_btn = True 添加按钮

# show_query_field = False  关键字搜索
# query_field = [字段]

# list_acions = [action操作]
# show_actions = False

# show_comb_filter = False 组合搜索
# comb_filter

# def course_semester(self,obj=None,is_header=None):
#     if is_header:
#         return "班级"
#     return "%s(%s期)"%(obj.course.name,obj.semester)
#
# def start_date(self,obj=None,is_header=None):
#     if is_header:
#         return "开班日期"
#     return obj.start_date.strftime("%Y-%m-%d")
#
# def cls_num(self,obj=None,is_header=None):
#     if is_header:
#         return "班级人数"
#     a = models.Student.objects.filter(class_list=obj.pk).count()
#     return a

class UserInfoConfig(v1.StarkConfig):
    list_display = ["username","password","phone"]
    edit_link = ["username"]

v1.site.registry(models.UserInfo,UserInfoConfig)

class MovieTypeConfig(v1.StarkConfig):
    list_display = ["name"]
    edit_link = ["name"]

v1.site.registry(models.MovieType,MovieTypeConfig)

class MovieDetailConfig(v1.StarkConfig):
    def mtype(self,obj=None,is_header=None):
        if is_header:
            return "电影类型"
        mtypes = []
        for item in obj.mtype.all().values_list("name"):
            mtypes.append(item[0])
        return ",".join(mtypes)

    def release(self, obj=None, is_header=None):
        if is_header:
            return "上映时间"
        return datetime.datetime.strftime(obj.release,"%Y-%m-%d")

    list_display = ["name","period","company","score","comment_num","like_num",release,mtype]
    edit_link = ["name"]

v1.site.registry(models.MovieDetail,MovieDetailConfig)


class WorkerConfig(v1.StarkConfig):

    def Actor(self, obj=None, is_header=None):
        if is_header:
            return "职责"
        return obj.get_Actor_display()

    def movie(self, obj=None, is_header=None):
        if is_header:
            return "关联电影"
        return obj.movie.name

    list_display = ["name",Actor,"role",movie]
    edit_link = ["name"]

v1.site.registry(models.Worker,WorkerConfig)

class CommentConfig(v1.StarkConfig):

    def parent_comment(self, obj=None, is_header=None):
        if is_header:
            return "父级评论"
        if obj.parent_comment:
            return obj.parent_comment.content
        return "无"

    def user(self, obj=None, is_header=None):
        if is_header:
            return "评论者"
        return obj.user.username

    def movie(self, obj=None, is_header=None):
        if is_header:
            return "评论电影"
        return obj.movie.name

    def create_data(self, obj=None, is_header=None):
        if is_header:
            return "评论时间"
        return datetime.datetime.strftime(obj.create_data,"%Y-%m-%d %H:%M")

    list_display = [user,movie,"content",parent_comment,"up_count","down_count",create_data]
    edit_link = [user]
    list_acions = [v1.StarkConfig.multi_del]
    show_actions = True
v1.site.registry(models.Comment,CommentConfig)

class CinemaConfig(v1.StarkConfig):

    list_display = ["title","addr"]
    edit_link = ["title"]

v1.site.registry(models.Cinema,CinemaConfig)


class MovieFieldConfig(v1.StarkConfig):

    def movie(self, obj=None, is_header=None):
        if is_header:
            return "影片"
        return obj.movie.name

    def cinema(self, obj=None, is_header=None):
        if is_header:
            return "影片"
        return obj.cinema.title

    def play_date(self, obj=None, is_header=None):
        if is_header:
            return "播放日期"
        return datetime.datetime.strftime(obj.play_date,"%Y-%m-%d")

    list_display = ["start_time", "price",play_date,"ballot",movie,cinema]
    edit_link = ["start_time"]


v1.site.registry(models.MovieField, MovieFieldConfig)

class PlayRoomConfig(v1.StarkConfig):

    def cinema(self, obj=None, is_header=None):
        if is_header:
            return "关联电影院"
        return obj.cinema.title

    list_display = ["caption",cinema]
    edit_link = ["caption"]
v1.site.registry(models.PlayRoom, PlayRoomConfig)

class OrderConfig(v1.StarkConfig):

    def payment_type(self, obj=None, is_header=None):
        if is_header:
            return "支付方式"
        return obj.get_payment_type_display()

    def user(self, obj=None, is_header=None):
        if is_header:
            return "支付人"
        return obj.user.username

    def status(self, obj=None, is_header=None):
        if is_header:
            return "状态"
        return obj.get_status_display()

    def date(self, obj=None, is_header=None):
        if is_header:
            return "订单生成时间"
        return datetime.datetime.strftime(obj.date,"%Y-%m-%d %H:%M")

    def pay_time(self, obj=None, is_header=None):
        if is_header:
            return "付款时间"
        if obj.pay_time:
            return datetime.datetime.strftime(obj.pay_time,"%Y-%m-%d %H:%M")
        return "无"

    def cancel_time(self, obj=None, is_header=None):
        if is_header:
            return "订单取消时间"
        if obj.pay_time:
            return datetime.datetime.strftime(obj.cancel_time,"%Y-%m-%d %H:%M")
        return "无"

    list_display = [user,payment_type,"actual_amount","status","payment_number","order_number",date,pay_time,cancel_time]
    edit_link = [user]
v1.site.registry(models.Order, OrderConfig)

class OrderDetailConfig(v1.StarkConfig):

    def order(self, obj=None, is_header=None):
        if is_header:
            return "关联订单"
        return obj.order.order_number

    def moviefield(self, obj=None, is_header=None):
        if is_header:
            return "影片场次"
        return "%s-%s"%(obj.moviefield.play_date,obj.moviefield.start_time)

    def seat(self, obj=None, is_header=None):
        if is_header:
            return "位置"
        return "%s 行 %s 列"%(obj.seat_row,obj.seat_col)


    list_display = [order,moviefield,"original_price",seat]
    edit_link = [order]


v1.site.registry(models.OrderDetail, OrderDetailConfig)

