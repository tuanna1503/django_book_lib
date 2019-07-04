from django.contrib import admin
from .models import BookType, Book, UserProfileInfo, RentalBook
# Register your models here.

class BookTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['book_type']}),
    ]
    list_display = [('book_type')]

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['book_name', 'book_type', 'amount']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('book_name', 'pub_date', 'amount','was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['book_name']

admin.site.register(UserProfileInfo)
admin.site.register(Book, BookAdmin)
admin.site.register(BookType, BookTypeAdmin)