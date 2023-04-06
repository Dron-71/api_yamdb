# модули для панели администрирования
import csv

from django.contrib import admin
from django.contrib.auth import get_user_model
from reviews.models import Category, Genre, Title, Review, Comment, GenreTitle
from csvimport.models import CsvImport
from csvimport.form import CsvImportForm
from users.models import User
# обслуживание импорта
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages


@admin.register(CsvImport)
class CsvImportAdmin(admin.ModelAdmin):
    list_display = ('id', 'csv_file', 'date_added')


class GenreInline(admin.TabularInline):
    model = Title.genre.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'name', 'slug')

    # даем django(urlpatterns) знать
    # о существовании страницы с формой
    # иначе будет ошибка
    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

        # если пользователь открыл url 'csv-upload/',
        # то он выполнит этот метод,
        # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            # т.к. это метод POST проводим валидацию данных
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'name', 'slug']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        Category.objects.update_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )

                # возвращаем пользователя на главную с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        # если это не метод POST, то возвращается форма с шаблоном
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    model = Title
    inlines = (GenreInline,)
    list_display = ('id', 'name', 'year', 'category', 'description')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

        # если пользователь открыл url 'csv-upload/',
        # то он выполнит этот метод,
        # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            # т.к. это метод POST проводим валидацию данных
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'name', 'year',
                                      'category']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла}')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        Title.objects.update_or_create(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            category=Category.objects.get(id=row[3])

                        )
                # возвращаем пользователя на главную с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        # если это не метод POST, то возвращается форма с шаблоном
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = (GenreInline,)
    list_display = ('id', 'name', 'slug')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

        # если пользователь открыл url 'csv-upload/',
        # то он выполнит этот метод,
        # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            # т.к. это метод POST проводим валидацию данных
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'name', 'slug']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        Genre.objects.update_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )
                # возвращаем пользователя на главную с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        # если это не метод POST, то возвращается форма с шаблоном
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('id', 'title_id', 'text', 'author', 'score',  'pub_date')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

        # если пользователь открыл url 'csv-upload/',
        # то он выполнит этот метод,
        # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            # т.к. это метод POST проводим валидацию данных
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'title_id', 'text', 'author',
                                      'score', 'pub_date']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        Review.objects.update_or_create(
                            id=row[0],
                            title_id=Title.objects.get(id=row[1]).id,
                            text=row[2],
                            author=User.objects.get(id=row[3]),
                            score=row[4],
                            pub_date=row[5]
                        )
                # возвращаем пользователя на главную с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        # если это не метод POST, то возвращается форма с шаблоном
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('id', 'review_id', 'text', 'author', 'pub_date')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

        # если пользователь открыл url 'csv-upload/',
        # то он выполнит этот метод,
        # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            # т.к. это метод POST проводим валидацию данных
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'review_id', 'text', 'author',
                                      'pub_date']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        Comment.objects.update_or_create(
                            id=row[0],
                            review_id=Review.objects.get(pk=row[1]).id,
                            text=row[2],
                            author=User.objects.get(pk=row[3]),
                            pub_date=row[4]

                        )
                        # добавляем данные в базу
                # возвращаем пользователя на главную с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        # если это не метод POST, то возвращается форма с шаблоном
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(GenreTitle)
class GenreTileAdmin(admin.ModelAdmin):

    list_display = ('id', 'title_id', 'genre_id')

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

        # если пользователь открыл url 'csv-upload/',
        # то он выполнит этот метод,
        # который работает с формой
    def upload_csv(self, request):
        if request.method == 'POST':
            # т.к. это метод POST проводим валидацию данных
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                # сохраняем загруженный файл и делаем запись в базу
                form_object = form.save()
                # обработка csv файла
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'title_id', 'genre_id']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        GenreTitle.objects.update_or_create(
                            id=row[0],
                            title=Title.objects.get(pk=row[1]),
                            genre=Genre.objects.get(pk=row[2]),
                        )
                # возвращаем пользователя на главную с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        # если это не метод POST, то возвращается форма с шаблоном
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})
