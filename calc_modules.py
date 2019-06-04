#-*- coding: utf-8 -*-


#複数点で囲まれた面積を計算して返す関数　引数はx,yで座標を持つ辞書の配列
def calc_area(points):
    area = 0
    for i in range(len(points)):
        if i == len(points)-1:
            area += points[i]['x']*points[0]['y'] - points[0]['x']*points[i]['y']
        else:
            area += points[i]['x']*points[i+1]['y'] - points[i+1]['x']*points[i]['y']
    return abs(area)*0.5

#二点間の距離を求める
def calc_distance(points):
    x_dis = points[0]['x'] - points[1]['x']
    y_dis = points[0]['y'] - points[1]['y']
    return (x_dis**2 + y_dis**2) ** 0.5


if __name__ == "__main__":
    o = {'x':0, 'y':0}
    a = {'x':2, 'y':2}
    b = {'x':4, 'y':1}
    c = {'x':6, 'y':0}

    point_4 = [o,a,b,c]
    point_4r = [c,b,a,o]

    print calc_area(point_4)
    print calc_area(point_4r)

    print ''

    print calc_distance([o,a])
    print calc_distance([o,c])