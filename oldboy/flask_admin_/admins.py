import os
from .manage import admin, session

# 在将表注册之前应该对app进行配置
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1:3307/py9api?charset=utf8mb4"
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = -1

# 导入models文件的中的表模型
from flask_admin.contrib.sqla import ModelView
from models import UserInfo

admin.add_view(ModelView(UserInfo, session))

"""如果有个字段是图片字段"""
# 配置上传文件的路径
from flask_admin.contrib.fileadmin import FileAdmin, form

file_path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(FileAdmin(file_path, '/static/', name='上传文件'))


# 如果有个字段要是上传文件重写该方法的modleView类，假设imgae_url是文件图片的字段
class ImagesView(ModelView):
    form_extra_fields = {
        'image_url': form.ImageUploadField('Image',
                                           base_path=file_path,
                                           relative_path='uploadFile/'
                                           )
    }

# admin.add_view(ImagesView(Images, session))
