from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

labels = [
    True, True, True, True, True,
    False, True, False, True, False,
    True, True, True, False, False,
    False, False, True, True, False,
    False, False, False, True, False,
    False, True, True, True, False,
    True, True, False, True, False,
    False, True, False, True, False
]

features = [
    [539, 556, 553, 518, 509, 588, 581, 569, 574, 511, 548, 505, 574, 527, 587],
    [640, 613, 700, 669, 690, 648, 610, 614, 687, 690, 612, 678, 658, 637, 658],
    [660, 621, 668, 610, 633, 614, 696, 625, 658, 651, 683, 643, 662, 668, 648],
    [557, 556, 591, 595, 509, 550, 563, 556, 562, 577, 542, 572, 548, 579, 577],
    [665, 640, 637, 694, 662, 646, 637, 674, 686, 627, 697, 684, 630, 607, 601],
    [978, 853, 487, 350, 540, 284, 254, 662, 794, 868, 400, 388, 927, 986, 835],
    [544, 592, 518, 595, 570, 565, 552, 546, 548, 553, 536, 552, 531, 516, 572],
    [95, 479, 538, 679, 207, 452, 521, 6, 461, 341, 436, 356, 413, 508, 738],
    [662, 685, 674, 648, 616, 671, 624, 660, 670, 653, 644, 681, 640, 667, 661],
    [998, 79, 672, 695, 26, 771, 699, 347, 933, 935, 544, 381, 538, 652, 616],
    [513, 513, 519, 503, 510, 537, 531, 586, 503, 588, 535, 500, 523, 562, 505],
    [605, 676, 663, 665, 678, 637, 658, 605, 614, 653, 687, 650, 656, 602, 675],
    [645, 640, 639, 600, 634, 655, 612, 687, 675, 652, 610, 683, 645, 644, 659],
    [865, 42, 423, 43, 542, 782, 340, 678, 941, 643, 547, 81, 410, 935, 449],
    [862, 646, 520, 757, 461, 366, 19, 507, 153, 380, 976, 729, 10, 395, 21],
    [998, 227, 289, 189, 737, 193, 453, 442, 850, 186, 681, 848, 561, 865, 233],
    [630, 511, 919, 953, 765, 514, 220, 173, 704, 765, 69, 124, 855, 695, 384],
    [618, 699, 628, 612, 609, 671, 629, 662, 634, 695, 650, 687, 643, 688, 662],
    [661, 691, 677, 641, 617, 690, 609, 689, 659, 610, 627, 698, 667, 647, 606],
    [193, 292, 973, 992, 796, 359, 407, 309, 196, 411, 415, 853, 495, 83, 297],
    [388, 136, 6, 708, 687, 930, 880, 237, 171, 704, 917, 975, 143, 840, 815],
    [351, 542, 506, 465, 747, 945, 121, 294, 545, 306, 999, 777, 849, 599, 120],
    [528, 689, 610, 818, 425, 690, 266, 719, 18, 570, 628, 141, 535, 975, 559],
    [676, 625, 641, 687, 681, 690, 681, 633, 631, 644, 633, 621, 607, 679, 656],
    [930, 25, 948, 736, 606, 717, 193, 920, 194, 711, 228, 875, 427, 364, 685],
    [204, 949, 344, 314, 788, 818, 738, 51, 454, 741, 713, 709, 559, 1, 47],
    [630, 663, 697, 611, 644, 605, 661, 608, 662, 692, 676, 600, 610, 635, 658],
    [613, 634, 659, 672, 631, 665, 669, 655, 683, 685, 621, 673, 651, 620, 690],
    [638, 649, 691, 606, 672, 635, 608, 656, 621, 615, 671, 666, 687, 689, 642],
    [432, 340, 920, 467, 269, 876, 744, 384, 902, 684, 296, 704, 172, 394, 845],
    [606, 672, 675, 608, 674, 668, 687, 694, 680, 676, 602, 625, 625, 664, 670],
    [692, 662, 696, 672, 606, 685, 685, 698, 607, 643, 662, 650, 675, 685, 673],
    [228, 699, 108, 103, 619, 606, 777, 114, 165, 487, 945, 182, 10, 393, 869],
    [648, 628, 644, 693, 607, 645, 600, 662, 666, 665, 683, 647, 674, 674, 653],
    [298, 857, 658, 958, 845, 854, 536, 945, 500, 898, 417, 749, 825, 98, 861],
    [959, 330, 904, 624, 742, 275, 958, 927, 288, 467, 736, 865, 852, 411, 506],
    [609, 693, 700, 660, 650, 632, 692, 606, 605, 600, 638, 645, 651, 617, 697],
    [26, 250, 80, 620, 178, 67, 301, 415, 433, 366, 646, 731, 542, 620, 238],
    [684, 632, 677, 625, 660, 658, 616, 601, 626, 694, 611, 692, 662, 700, 648],
    [336, 836, 518, 832, 875, 554, 927, 288, 589, 940, 111, 741, 787, 485, 412]
]


test_features = [
    [514, 543, 594, 557, 527, 596, 581, 531, 597, 568, 542, 590, 546, 574, 501],
    [528, 562, 547, 527, 536, 534, 565, 599, 528, 526, 528, 527, 525, 531, 593],
    [122, 100, 917, 244, 327, 387, 398, 597, 121, 777, 183, 580, 808, 496, 483],
    [918, 716, 581, 450, 34, 497, 909, 530, 745, 392, 55, 28, 100, 222, 130],
    [901, 473, 701, 297, 814, 846, 271, 320, 95, 668, 307, 392, 260, 653, 218],
    [473, 411, 118, 906, 974, 472, 635, 88, 840, 353, 209, 8, 663, 360, 691],
    [339, 517, 430, 54, 67, 960, 874, 45, 505, 204, 202, 740, 734, 658, 38],
    [664, 642, 624, 645, 641, 654, 629, 661, 680, 645, 646, 669, 629, 614, 663],
    [648, 548, 201, 876, 711, 932, 958, 233, 130, 281, 287, 691, 472, 291, 834],
    [674, 700, 603, 628, 649, 690, 649, 682, 630, 676, 666, 670, 668, 676, 610],
    [616, 692, 611, 667, 686, 680, 698, 623, 623, 699, 681, 692, 624, 665, 648],
    [727, 120, 375, 569, 66, 998, 504, 571, 234, 25, 486, 690, 34, 712, 624],
    [670, 603, 659, 665, 645, 622, 649, 674, 624, 628, 636, 633, 641, 600, 698],
    [633, 636, 652, 644, 676, 644, 626, 696, 642, 600, 685, 627, 689, 626, 615],
    [615, 682, 612, 663, 612, 675, 620, 632, 615, 689, 697, 687, 699, 674, 655],
    [5, 458, 744, 466, 175, 205, 919, 630, 275, 629, 760, 719, 955, 988, 584],
    [692, 664, 639, 630, 658, 679, 620, 665, 659, 626, 622, 680, 671, 617, 693],
    [943, 461, 877, 125, 155, 887, 188, 60, 238, 257, 443, 71, 819, 701, 990],
    [57, 335, 255, 445, 218, 660, 782, 605, 496, 996, 985, 283, 56, 818, 70],
    [329, 940, 284, 437, 390, 713, 932, 4, 875, 524, 692, 154, 518, 808, 376],
    [668, 679, 677, 691, 666, 638, 631, 603, 687, 679, 602, 665, 696, 605, 700],
    [551, 687, 801, 959, 374, 429, 534, 568, 266, 44, 886, 664, 453, 286, 662],
    [625, 924, 615, 300, 847, 333, 233, 70, 133, 654, 77, 52, 107, 169, 968],
    [551, 575, 579, 549, 598, 521, 513, 522, 548, 549, 505, 566, 537, 519, 500],
    [568, 580, 574, 577, 576, 566, 524, 527, 548, 516, 561, 512, 558, 567, 568],
    [559, 571, 500, 523, 555, 533, 556, 547, 555, 558, 500, 578, 567, 583, 556]
]

test_labels = [
    True, True, False,
    False, False, False, False,
    True, False, True, True,
    False, True, True, True,
    False, True, False, False,
    False, True, False, False,
    True, True, True
]

# Логистическая регрессия
logreg_clf = LogisticRegression() # создаем обьект класса
logreg_clf.max_iter += 10000  # увеличиваем количество итераций
logreg_clf.fit(features, labels)
# обучаем на помеченных данных первый аргумент это массив массивов с данными
# второй массив массивов с метками которые соответсвуют данным
prediction = logreg_clf.predict(test_features)  # предсказание сделланое моделью, возвращает массив с метками

# Линейный дискриминантный анализ
linerd_clf = LinearDiscriminantAnalysis()
linerd_clf.fit(features, labels)
predictiond = linerd_clf.predict(test_features)

# K-Ближайшие Соседи
kn_clf = KNeighborsClassifier()
kn_clf.fit(features, labels)
predictionkn = kn_clf.predict(test_features)


# Наивный Байес
g_clf = GaussianNB()
g_clf.fit(features, labels)
predictiong = g_clf.predict(test_features)

# Деревья решений
DES_clf = DecisionTreeClassifier()
DES_clf.fit(features, labels)
predictionDES = DES_clf.predict(test_features)


# Машины опорных Векторов
svc_clf = SVC()
svc_clf.fit(features, labels)
prediction_svc = svc_clf.predict(test_features)


print("Логистическая регрессия")
print("------------------------------------------------------------------")
print(prediction)
print("------------------------------------------------------------------")
print(accuracy_score(prediction, test_labels))
print("------------------------------------------------------------------")
print(confusion_matrix(prediction, test_labels))
print("------------------------------------------------------------------")
print(classification_report(prediction, test_labels))
print("------------------------------------------------------------------")


print("Линейный дискриминантный анализ")
print("------------------------------------------------------------------")
print(predictiond)
print("------------------------------------------------------------------")
print(accuracy_score(predictiond, test_labels))
print("------------------------------------------------------------------")
print(confusion_matrix(predictiond, test_labels))
print("------------------------------------------------------------------")
print(classification_report(predictiond, test_labels))
print("------------------------------------------------------------------")

print("K-Ближайшие Соседи")
print(predictionkn)
print("------------------------------------------------------------------")
print(accuracy_score(predictionkn, test_labels))
print("------------------------------------------------------------------")
print(confusion_matrix(predictionkn, test_labels))
print("------------------------------------------------------------------")
print(classification_report(predictionkn, test_labels))
print("------------------------------------------------------------------")

print("Наивный Байес")
print(predictiong)
print("------------------------------------------------------------------")
print(accuracy_score(predictiong, test_labels))
print("------------------------------------------------------------------")
print(confusion_matrix(predictiong, test_labels))
print("------------------------------------------------------------------")
print(classification_report(predictiong, test_labels))
print("------------------------------------------------------------------")

print("Деревья решений")
print(predictionDES)
print("------------------------------------------------------------------")
print(accuracy_score(predictionDES, test_labels))
print("------------------------------------------------------------------")
print(confusion_matrix(predictionDES, test_labels))
print("------------------------------------------------------------------")
print(classification_report(predictionDES, test_labels))
print("------------------------------------------------------------------")

print("Машины опорных Векторов")
print(prediction_svc)
print("------------------------------------------------------------------")
print(accuracy_score(prediction_svc, test_labels))
print("------------------------------------------------------------------")
print(confusion_matrix(prediction_svc, test_labels))
print("------------------------------------------------------------------")
print(classification_report(prediction_svc, test_labels))
print("------------------------------------------------------------------")
