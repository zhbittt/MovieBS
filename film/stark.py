from stark.service import v1
from film import models

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
#
#     return a
class UserInfoConfig(v1.StarkConfig):

    list_display = ["username","password","phone"]
    edit_link = ["username"]

v1.site.registry(models.UserInfo,UserInfoConfig)