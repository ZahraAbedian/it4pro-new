from django.contrib import admin
from .models import Categories, Answers, Questions, Paragraphs, UserAnswers, UserCategories, UserResult, ResultPageParaghraphs

# Register your models here.


class QuestionsAdmin(admin.ModelAdmin):
    # Ordering questions by category and then by the question text
    ordering = ['question_fk__category', 'question']
    
    # Adding a filter option to filter questions by category
    list_filter = ['question_fk']

    # Optional: If you want to display additional fields in the admin list view
    list_display = ['question', 'question_fk', 'question_order', 'date']


class CategoriesAdmin(admin.ModelAdmin):
    ordering = ['category']
   # list_filter = ['category_order']
    list_display = ['category', 'category_order']

class ParagraphsAdmin(admin.ModelAdmin):
    ordering = ['paragraph_fk__category', 'paragraph']
    list_filter = ['paragraph_fk']
    list_display = ['paragraph', 'paragraph_fk', 'paragraph_order']

class UserAnswersAdmin(admin.ModelAdmin):
    ordering = ['user']
    list_display = ['user', 'question', 'answer', 'mdate']

class UserCategoriesAdmin(admin.ModelAdmin):
    ordering = ['user']
    list_display = ['user', 'category', 'score']

class UserResultAdmin(admin.ModelAdmin):
    ordering = ['user']
    list_display = ['user', 'radarChart', 'barChart', 'QuestionLock', 'Change']

class ResultPageParaghraphsAdmin(admin.ModelAdmin):
    ordering = ['category']
    list_display = ['category', 'score', 'paragraph']

admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Answers)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Paragraphs, ParagraphsAdmin)
admin.site.register(UserAnswers, UserAnswersAdmin)
admin.site.register(UserCategories, UserCategoriesAdmin)
admin.site.register(UserResult, UserResultAdmin)
admin.site.register(ResultPageParaghraphs, ResultPageParaghraphsAdmin)


