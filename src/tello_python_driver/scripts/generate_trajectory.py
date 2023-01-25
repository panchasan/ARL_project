import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import sys
import librosa
import random
import math

def figure8():
    angle = np.linspace(0, 2 * np.pi, 40)
    radius = 2
    x = radius * np.sin(angle)
    y = radius * np.sin(angle) * np.cos(angle)
    return x, y

def circle():
    angle = np.linspace(0, 2 * np.pi, 30)
    radius = 1
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    return x, y

def sin_draw():
    x = np.arange(0, 0.7 * np.pi, 0.3)
    y = np.sin(x)
    return x, y

def sin_draw2():
    x = np.arange(0, 0.7 * np.pi, 0.3)
    y = np.sin(-x)
    return x, y

def sin_draw3():
    x = np.arange(0, 0.7 * np.pi, 0.3)
    y = -(np.sin(x))
    return x, y

def rectangle():
    x = [0, 0, 0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0]
    y = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
    return x, y

def find_plp_value(time_p, zm, times):
    wi = 2.9
    tp = 0
    for i in time_p:
        if abs(i - zm) < wi:
            wi = abs(i - zm)
            tp = i
    n2 = 0
    for n, i in enumerate(times):
        if i == tp:
            n2 = n
            break
    return n2

def choose_traj():
    que = []
    fl = 300
    for i in range(800):
        a = random.randint(0, 5)
        if a == fl:
            while a == fl:
                a = random.randint(0, 5)
        que.append(a)
        fl = a
    return que


def save_traj(x, y, z, time):
    # print(len(x), len(y), len(z), len(time))
    a = []
    b = []
    c = []
    with open('traj.txt', 'w') as f:
        for num, line in enumerate(z):
            if z[num]<0.4:
                z[num]=0.4
            elif z[num]>1.7:
                z[num]=1.7
            text = str(round(time[num],4)) + ', ' +str(x[num]) + ', ' + str(y[num]) + ', ' + str(z[num]) + ', 0'
            a.append(x[num])
            b.append(y[num])
            c.append(z[num])
            f.write(text)
            f.write('\n')

    # ax = plt.figure().add_subplot(projection='3d')
    # ax.plot(a, b, c)
    # ax.scatter(a, b, c)
    # plt.show()

def gen_traj(dicx, dicy, list_of_traj, point_num):
    fl = False
    x = []
    y = []
    for i in list_of_traj:
        if fl:
            fl2 = True
            for n, j in enumerate(dicx[i]):
                if fl2:
                    if math.dist((j, dicy[i][n]), (x[-1], y[-1])) < 25 and math.dist((j, dicy[i][n]), (x[-1], y[-1])) > 2:
                        fl2 = False

                else:
                    x.append(round(j, 3))
                    y.append(round(dicy[i][n], 3))
        else:
            for n, j in enumerate(dicx[i]):
                x.append(round(j,3))
                y.append(round(dicy[i][n],3))

                fl=True

        if len(x)>point_num:
            break
    return x, y


def gen_x_y():
    dicx = []
    dicy = []
    x, y = figure8()
    dicx.append(x)
    dicy.append(y)

    x1, y1 = circle()
    dicx.append(x1)
    dicy.append(y1)

    x2, y2 = sin_draw()
    dicx.append(x2)
    dicy.append(y2)

    x3, y3 = rectangle()
    dicx.append(x3)
    dicy.append(y3)

    x4, y4 = sin_draw2()
    dicx.append(x4)
    dicy.append(y4)

    x5, y5 = sin_draw3()
    dicx.append(x5)
    dicy.append(y5)

    return dicx, dicy


def main(args):
    dicx, dicy = gen_x_y()
    list_of_traj = choose_traj()

    filename = str(args[1])
    hop_length = 512
    y, sr = librosa.load(filename, duration = 60)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    time_bet = librosa.frames_to_time(beats, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
    beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
    time_p = librosa.frames_to_time(beats_plp, sr=sr)
    times = librosa.times_like(onset_env, sr=sr, hop_length=hop_length)

    z = []

    for n, i in enumerate(time_bet):
        num = find_plp_value(time_p, i, times)
        z.append(round(librosa.util.normalize(pulse)[num]*2, 4))

    x, y = gen_traj(dicx, dicy, list_of_traj, len(z))
    save_traj(x, y, z, time_bet)


if __name__ == '__main__':
    main(sys.argv)


