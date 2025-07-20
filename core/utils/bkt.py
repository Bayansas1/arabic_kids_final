
class BKTModel:
    def __init__(self, p_know, p_t, p_g, p_s):
        self.p_know = p_know  #احتمال اتقان المهارة من البداية
        self.p_t = p_t  #احتمال التعلم بعد كل محاولة
        self.p_g = p_g   #احتمال التخمين (guess)
        self.p_s = p_s    #احتمال الخطأ رغم المعرفة

    def update(self, correct):
        if correct:  #اذا كانت الاجابة صحيحة
            p_correct = self.p_know * (1 - self.p_s) + (1 - self.p_know) * self.p_g
            p_know_given_obs = (self.p_know * (1 - self.p_s)) / p_correct
        else:
            p_correct = self.p_know * self.p_s + (1 - self.p_know) * (1 - self.p_g)
            p_know_given_obs = (self.p_know * self.p_s) / p_correct

        self.p_know = p_know_given_obs + (1 - p_know_given_obs) * self.p_t  #تحديث احتمال الاتقان بعد الملاحظة
        return self.p_know