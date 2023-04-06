import csv

from django.contrib import admin

from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User
from csvimport.form import CsvImportForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name')
    search_fields = ('username',)
    list_filter = ('role',)

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
                    if next(rows) != ['id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name']:
                        # обновляем страницу пользователя
                        # с информацией о какой-то ошибке
                        messages.warning(request, 'Неверные заголовки у файла')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        # добавляем данные в базу
                        User.objects.update_or_create(
                            id=row[0],
                            username=row[1],
                            email=row[2],
                            role=row[3],
                            bio=row[4],
                            first_name=row[5],
                            last_name=row[6]
                        )
                # возвращаем пользователя на главную с сообщением об успехе
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        # если это не метод POST, то возвращается форма с шаблоном
        form = CsvImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})
