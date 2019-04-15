# -*- coding: utf-8 -*-
#!/usr/bin/env python
# File : test_different_metrics.py
# Date : 2019/4/11
# Author: leichao
# Email : leichaocn@163.com

"""简述功能.

详细描述.
"""

__filename__ = "test_different_metrics.py"
__date__ = 2019 / 4 / 11
__author__ = "leichao"
__email__ = "leichaocn@163.com"

import os
import sys

import pandas as pd
import numpy as np

from sklearn.metrics import r2_score
from matplotlib import pyplot as plt

def mean_absolute_percentage_error(y_true, y_pred):
    # y_true, y_pred = check_array(y_true, y_pred)
    ## Note: does not handle mix 1d representation
    # if _is_1d(y_true):
    #    y_true, y_pred = _check_1d_array(y_true, y_pred)
    abs_delta_price_list = np.abs((y_true - y_pred) / y_true) * 100
    # print('abs_delta_price_list=',abs_delta_price_list)
    return np.mean(abs_delta_price_list), np.std(abs_delta_price_list) * 1.96

def get_ape_reliability(y_true, y_pred, threshold):
    abs_delta_price_list = np.abs((y_true - y_pred) / y_true) * 100
    # print('abs_delta_price_list=',abs_delta_price_list)
    count = 0
    for i in abs_delta_price_list:
        if i <= threshold:
            count = count + 1
    ape_reliability = count / len(abs_delta_price_list)
    return ape_reliability

def get_aper_auc(y_true, y_pred):
    absolute_percentage_error_list = np.abs((y_true - y_pred) / y_true) * 100
    # print('abs_delta_price_list=',absolute_percentage_error_list)
    revised_sorted_ape_list=[ i if i <=100 else 100
                              for i in absolute_percentage_error_list]
    sorted_ape_list=sorted(revised_sorted_ape_list)
    # print('sorted_ape_list=',sorted_ape_list)
    size_of_sorted_ape_list=len(sorted_ape_list)
    sorted_ape_reliability_list=[]
    aper_curve_area = 0
    delta_aper_curve_area = 0
    delta_list = []
    aper_list = []
    last_ape = 100
    last_aper = 0
    break_flag = False
    for i,ape in enumerate(sorted_ape_list):
        # 本轮ape，可理解为auc曲线图上的每个小方块的横坐标
        this_ape = ape
        # 本轮aper，可理解为auc曲线图上的每个小方块的纵坐标
        this_aper = (i + 1) / size_of_sorted_ape_list
        
        ape_reliability_tuple = (this_ape,this_aper)
        sorted_ape_reliability_list.append(ape_reliability_tuple)

        if i != 0 :
            if this_ape >= 100:
                this_ape = 100
                break_flag = True

            # 用本轮与上一轮，构成梯形来计算
            # delta_aper_curve_area = 0.5 * (last_aper + this_aper) * (ape - last_ape)
            # 用上一轮的aper作为小方块的高，用上一轮到本轮的ape差值来作为宽。
            delta_aper_curve_area = last_aper * (this_ape - last_ape)
            aper_curve_area = aper_curve_area + delta_aper_curve_area

            delta_list.append(this_ape)
            aper_list.append(this_aper)
        
            if i == size_of_sorted_ape_list - 1 and this_ape < 100:
                delta_aper_curve_area = this_aper * (100 - this_ape)
                aper_curve_area = aper_curve_area + delta_aper_curve_area
                delta_list.append(100)
                aper_list.append(this_aper)
                break_flag = True
        else:
            delta_list.append(this_ape)
            aper_list.append(this_aper)
            
        last_ape = this_ape
        last_aper = this_aper
        
        if break_flag:
            break

        
        
    # print('sorted_ape_reliability_list = ',sorted_ape_reliability_list)
    plt.plot(delta_list, aper_list,'bo-')
    # plt.xticks(")
    plt.xlabel('reliability_threshold')
    plt.ylabel('APE_reliability')
    plt.title(" APER Curve (like ROC)")
    plt.show()
    return aper_curve_area/100

def get_auc(y_true, y_pred):
    delta_list=np.arange(5,105,5)
    # print("delta_list = ",delta_list)
    total_area=0
    last_aper=0
    aper_list=[]
    for i in delta_list:
        aper=get_ape_reliability(y_true, y_pred, i)
        if i == 5:
            delta_area=0.5*5*aper
        else:
            delta_area = 0.5 * 5 * (last_aper + aper)
        aper_list.append(aper)
        total_area=total_area+delta_area
        last_aper=aper
    delta_list=list(delta_list)
    aper_list=list(aper_list)
    delta_list.insert(0,0)
    aper_list.insert(0,0)
    plt.plot(delta_list, aper_list,'bo-')
    # plt.xticks(")
    plt.xlabel('reliability threshold')
    plt.ylabel('APE_reliability')
    plt.title(" APER Curve (like ROC)")
    plt.show()
    return total_area/100



def my_r2(y_true, y_pred):
    # return (y_true - y_pred)
    tmp=y_true - y_pred
    tmp1=[i**2 for i in tmp]
    this_mean=y_true.mean()
    tmp2=[(i-this_mean)**2 for i in y_true]
    # print("tmp1 = ",tmp1)
    # print("tmp2 = ",tmp2)

    res=sum(tmp1)
    tot=sum(tmp2)
    # print("res = ",res)
    # print("tot = ",tot)
    return (1-res/tot)
    # return sum(tmp2)


def get_performance(y_true, y_pred):
    print("-"*100)
    r2 = r2_score(y_true, y_pred)
    mape, ape_half_interval = mean_absolute_percentage_error(y_true,y_pred)

    ape_reliability_20 = get_ape_reliability(y_true, y_pred, 20)
    ape_reliability_10 = get_ape_reliability(y_true, y_pred, 10)
    aper_auc = get_auc(y_true, y_pred)
    aper_auc_2 = get_aper_auc(y_true, y_pred)
    print('mape is ', mape, '+/-', ape_half_interval)
    print('r2 is ', r2)
    print('ape_reliability_20 is ', ape_reliability_20)
    print('ape_reliability_10 is ', ape_reliability_10)
    print("aper_auc is ", aper_auc)
    print("aper_auc_2 is ", aper_auc_2)


# y_true=np.array([95,100,100,100,100,100,100,100,100,100,100])
# y_pred_0=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,90])
# y_pred_1=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,100])
# y_pred_2=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,110])
# y_pred_3=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,120])
# y_pred_4=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,130])
# y_pred_5=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,140])
# y_pred_6=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,150])
# aper_auc_2 = get_aper_auc(y_true, y_pred_0)
# print("aper_auc_1 is ", aper_auc_2)
# aper_auc_2 = get_aper_auc(y_true, y_pred_1)
# print("aper_auc_1 is ", aper_auc_2)
# aper_auc_2 = get_aper_auc(y_true, y_pred_2)
# print("aper_auc_2 is ", aper_auc_2)
# aper_auc_2 = get_aper_auc(y_true, y_pred_3)
# print("aper_auc_3 is ", aper_auc_2)
# aper_auc_2 = get_aper_auc(y_true, y_pred_4)
# print("aper_auc_4 is ", aper_auc_2)
# aper_auc_2 = get_aper_auc(y_true, y_pred_5)
# print("aper_auc_5 is ", aper_auc_2)
# aper_auc_2 = get_aper_auc(y_true, y_pred_6)
# print("aper_auc_6 is ", aper_auc_2)
# exit()

y_true=np.array([95,100,100,100,100,100,100,100,100,100,100])
y_pred_1=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,180])
y_pred_2=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,140])
y_pred_3=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,240])
get_performance(y_true, y_pred_1)
get_performance(y_true, y_pred_2)
get_performance(y_true, y_pred_3)


# y_true=np.array([95,100,100,100,100,100,100,100,100,100,10])
# y_pred_1=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,8.5])
# y_pred_2=np.array([90, 110, 90, 85,110,100,105,93, 120, 85,9])
# y_pred_3=np.array([90, 110, 90, 85,110,100,105,93, 120, 90,8.5])
# aper_auc = get_aper_auc(y_true, y_pred_1)
# print("aper_auc_1 is ", aper_auc)
# aper_auc = get_aper_auc(y_true, y_pred_2)
# print("aper_auc_2 is ", aper_auc)
# aper_auc = get_aper_auc(y_true, y_pred_3)
# print("aper_auc_3 is ", aper_auc)


# # r2 = r2_score(y_true, y_pred)
# mape_mean, mape_half_interval = mean_absolute_percentage_error(y_true, y_pred)
#
# mape_reliability_20 = get_mape_reliability(y_true, y_pred, 20)
# mape_reliability_10 = get_mape_reliability(y_true, y_pred, 10)
# maper_auc = get_auc(y_true, y_pred)
# print('mape_mean is ', mape_mean, '+/-', mape_half_interval)
# print('r2 is ', r2)
# print('mape_reliability_20 is ', mape_reliability_20)
# print('mape_reliability_10 is ', mape_reliability_10)
# print("maper_auc is ",maper_auc)
