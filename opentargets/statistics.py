class HarmonicSumScorer():

    def __init__(self, buffer = 100):
        '''
        will get every score,
        keep in memory the top max number
        calculate the score on those
        '''
        self.buffer = buffer
        self.data = []
        self.refresh()

    def add(self, score):
        if len(self.data)>= self.buffer:
            if score >self.min:
                self.data[self.data.index(self.min)] = float(score)
                self.refresh()
        else:
            self.data.append(float(score))
            self.refresh()


    def refresh(self):
        if self.data:
            self.min = min(self.data)
        else:
            self.min = 0.

    def score(self, *args,**kwargs):
        return self.harmonic_sum(self.data, *args, **kwargs)

    @staticmethod
    def harmonic_sum(data,
                     scale_factor = 1,
                     cap = None):
        data.sort(reverse=True)
        harmonic_sum = sum(s / ((i+1) ** scale_factor) for i, s in enumerate(data))
        if cap is not None and \
                        harmonic_sum > cap:
            return cap
        return harmonic_sum