class HarmonicSumScorer():

    def __init__(self, buffer = 100):
        """
        An HarmonicSumScorer will ingest any number of numeric score, keep in memory the top max number
        defined by the buffer and calculate an harmonic sum of those
        Args:
            buffer: number of element to keep in memory to compute the harmonic sum
        """
        self.buffer = buffer
        self.data = []
        self.refresh()

    def add(self, score):
        """
        add a score to the pool of values
        Args:
            score (float):  a number to add to the pool ov values. is converted to float

        """
        score = float(score)
        if len(self.data)>= self.buffer:
            if score >self.min:
                self.data[self.data.index(self.min)] = score
                self.refresh()
        else:
            self.data.append(score)
            self.refresh()


    def refresh(self):
        """
        Store the minimum value of the pool

        """
        if self.data:
            self.min = min(self.data)
        else:
            self.min = 0.

    def score(self, *args,**kwargs):
        """
        Returns an harmonic sum for the pool of values
        Args:
            *args: forwarded to HarmonicSumScorer.harmonic_sum
        Keyword Args
            **kwargs: forwarded to HarmonicSumScorer.harmonic_sum
        Returns:
            harmonic_sum (float): the harmonic sum of the pool of values
        """
        return self.harmonic_sum(self.data, *args, **kwargs)

    @staticmethod
    def harmonic_sum(data,
                     scale_factor = 1,
                     cap = None):
        """
        Returns an harmonic sum for the data passed
        Args:
            data (list): list of floats to compute the harmonic sum from
            scale_factor (float): a scaling factor to multiply to each datapoint. Defaults to 1
            cap (float): if not None, never return an harmonic sum higher than the cap value.

        Returns:
            harmonic_sum (float): the harmonic sum of the data passed
        """
        data.sort(reverse=True)
        harmonic_sum = sum(s / ((i+1) ** scale_factor) for i, s in enumerate(data))
        if cap is not None and \
                        harmonic_sum > cap:
            return cap
        return harmonic_sum