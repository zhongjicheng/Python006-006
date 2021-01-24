from django.shortcuts import render

# Create your views here.
from .models import T1
from django.db.models import Avg


def books_short(requtest):
    # # 从 models 取数据传给 template
    # shorts = T1.objects.all()
    # # 评论数量
    # counter = T1.objects.all().count()
    #
    # # 平均星级，保留1位小数
    # # star_value = T1.objects.values('n_star')
    # star_avg = f"{T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f}"
    # # 情感倾向，保留2位小数
    # sent_avg = f"{T1.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f}"
    #
    # # 正向数量，取出 sentiment >= 0.5 的数据
    # queryset = T1.objects.values('sentiment')
    # # key sentiment__gte 由2部分组成，用 __ 隔开：1，sentiment 为字段名称；2， gte 为判断条件 大于等于；其他条件（gt、lt、gte、lte）
    # conditions = {'sentiment__gte': 0.5}
    # plus = queryset.filter(**conditions).count()
    #
    # # 负向数量，取出 sentiment < 0.5 的数据
    # queryset = T1.objects.values('sentiment')
    # conditions = {'sentiment__lt': 0.5}
    # minus = queryset.filter(**conditions).count()

    # 展示高于 3 星级（不包括 3 星级）的短评内容和它对应的星级；
    conditions = {'n_star__gt': 3}
    queryset = T1.objects.filter(**conditions)

    # return render(request, 'douban.html', locals())
    return render(requtest, 'result.html', locals())
