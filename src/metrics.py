def true_positive(y_true, y_pred):
    sum = 0
    for yt, yp in zip(y_true, y_pred):
        if yt == 1 and yp == 1:
            sum += 1
    return sum

def true_negative(y_true, y_pred):
    sum = 0
    for yt, yp in zip(y_true, y_pred):
        if yt == 0 and yp == 0:
            sum += 1
    return sum

def false_positive(y_true, y_pred):
    sum = 0
    for yt, yp in zip(y_true, y_pred):
        if yt == 0 and yp == 1:
            sum += 1
    return sum

def false_negative(y_true, y_pred):
    sum = 0
    for yt, yp in zip(y_true, y_pred):
        if yt == 1 and yp == 0:
            sum += 1
    return sum

def compute_confusion_matrix(y_true, y_pred):
    tp = true_positive(y_true, y_pred)
    tn = true_negative(y_true, y_pred)
    fp = false_positive(y_true, y_pred)
    fn = false_negative(y_true, y_pred)
    return [[tp, fp], [fn, tn]]

def accuracy(y_true, y_pred):
    tp = true_positive(y_true, y_pred)
    tn = true_negative(y_true, y_pred)
    fp = false_positive(y_true, y_pred)
    fn = false_negative(y_true, y_pred)
    return (tp + tn) / (tp + tn + fp + fn)

def precision(y_true, y_pred):
    tp = true_positive(y_true, y_pred)
    fp = false_positive(y_true, y_pred)
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)

def recall(y_true, y_pred):
    tp = true_positive(y_true, y_pred)
    fn = false_negative(y_true, y_pred)
    if tp + fn == 0:
        return 0
    return tp / (tp + fn)

def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    if p + r == 0:
        return 0
    return 2 * (p * r) / (p + r)
