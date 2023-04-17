from django.contrib import admin

from . models import Faculty,Department,Courses, Mycourse, Wishlist, Message,Forum, Note, Picture
# Register your models here.

class PictureAdmin(admin.ModelAdmin):
    list_display = ('user','image')
    
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id','title','image','description')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','title','image','description','paid','available','facult')  

class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id','title','image','description','depart','fee','paid','available','end','start')  

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id','title','image','description','content','chapter','note')  

class MycourseAdmin(admin.ModelAdmin):
    list_display = ('id','user','title','image','description','paid')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id','user','thecontent','paid','image','amount')

class ForumAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','value','forum','sent','sender')


admin.site.register(Picture,PictureAdmin)
admin.site.register(Faculty,FacultyAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Mycourse,MycourseAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(Courses,CoursesAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Forum,ForumAdmin)
admin.site.register(Message,MessageAdmin)

