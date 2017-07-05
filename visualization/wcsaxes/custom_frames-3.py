from astropy.visualization.wcsaxes.frame import BaseFrame

class HexagonalFrame(BaseFrame):

    spine_names = 'abcdef'

    def update_spines(self):

        xmin, xmax = self.parent_axes.get_xlim()
        ymin, ymax = self.parent_axes.get_ylim()

        ymid = 0.5 * (ymin + ymax)
        xmid1 = (xmin + xmax) / 4.
        xmid2 = (xmin + xmax) * 3. / 4.

        self['a'].data = np.array(([xmid1, ymin], [xmid2, ymin]))
        self['b'].data = np.array(([xmid2, ymin], [xmax, ymid]))
        self['c'].data = np.array(([xmax, ymid], [xmid2, ymax]))
        self['d'].data = np.array(([xmid2, ymax], [xmid1, ymax]))
        self['e'].data = np.array(([xmid1, ymax], [xmin, ymid]))
        self['f'].data = np.array(([xmin, ymid], [xmid1, ymin]))