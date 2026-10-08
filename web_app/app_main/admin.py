from django.contrib import admin
from app_main.models import Profile, experience, Roadmap, Cinema, VideoGame, Music, Skill

class skillInline(admin.TabularInline):
    model = Skill 
class experienceInline(admin.TabularInline):
    model = experience
class roadmapInline(admin.TabularInline):
    model = Roadmap

class profileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'education', 'description')
    search_fields = ('id', 'user__first_name', 'user__last_name', 'education', 'description')
    list_filter = ('education',)
    inlines = (skillInline,experienceInline, roadmapInline)

    @admin.display(description='User')
    def get_full_name(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name if name else obj.user.username

admin.site.register(Profile, profileAdmin)
admin.site.register(experience)
admin.site.register(Roadmap)
admin.site.register(Cinema)
admin.site.register(VideoGame)
admin.site.register(Music)
admin.site.register(Skill)
