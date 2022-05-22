from django.shortcuts import render, redirect
import json
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.views import View


class MainPage(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class SomeNewPage(View):
    def get(self, request, link):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_list = json.load(json_file)
            for new in news_list:
                if new['link'] == int(link):
                    return render(request, 'new.html', context=new)


class NewsPage(View):
    def get(self, request):
        #date_dict = {}
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:

            news_list = json.load(json_file)
            news_list.sort(key=lambda new: new['created'], reverse=True)
            date_dict = {}

            for elem in news_list:
                created = datetime.strptime(elem['created'], "%Y-%m-%d %H:%M:%S")
                date = created.strftime("%Y-%m-%d")
                elem['created'] = date

                if date not in date_dict:
                    date_dict[date] = [elem]
                else:
                    date_dict[date].append(elem)
            # print(date_dict)

        query = request.GET.get('q')
        print(query)

        if query:
            result = {}
            for date in date_dict:
                for news in date_dict[date]:
                    if query in news['title'] and date not in result:
                        result[date] = [news]
                    elif query in news and date in result:
                        result[date].append(news)

            print(result)
            return render(request, 'news.html', {'date_dict': result})
        else:
            return render(request, 'news.html', {'date_dict': date_dict})


class CreatePage(View):
    def get(self, request):

        return render(request, 'create.html')

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            try:
                data_list = json.load(json_file)
            except json.decoder.JSONDecodeError:
                data_list = []

        with open(settings.NEWS_JSON_PATH, 'w+') as json_file:
            if data_list:
                link = max([elem['link'] for elem in data_list]) + 1

                data_list.append({'created': created,
                                  'text': text,
                                  'title': title,
                                  'link': link
                                  })

                json.dump(data_list, json_file)
            else:
                link = 1

                data_list.append({'created': created,
                                  'text': text,
                                  'title': title,
                                  'link': link
                                  })

                json.dump(data_list, json_file)

        return redirect('/news/')


