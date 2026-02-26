import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from .models import UserCategories, UserResult, ResultPageParaghraphs
from .models import Questions, UserAnswers

def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` Axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding Axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels, position):
            self.set_thetagrids(np.degrees(theta), labels, horizontalalignment=position, fontsize=10)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self, spine_type='circle', path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(0).translate(0, 0) + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

# draw radar chart
def drawRadarChart(data, categories, fileName):
    N = len(categories)
    theta = radar_factory(N, frame='polygon')

    # d = [0, 2, 3, 4, 5, 1, 2, 1, 3, 0]
    # spoke_labels = ['Availability Management', 'Capacity Management', 'Change Management', 'Configuration Managenment', 'Continuity Management', 'Financial Management', 'Incident Management', 'Problem Management', 'Release Management', 'Service Level Management']

    fig, axs = plt.subplots(figsize=(1, 1), nrows=1, ncols=1,
                            subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    axs.set_rgrids([1, 2, 3, 4, 5])
    axs.plot(theta, data, color='b', marker='o')
    axs.set_varlabels(categories, 'center')

    fig.text(0.5, 0.965, 'Process Maturity Level',
             horizontalalignment='center', color='black', weight='bold',
             fontsize=18)
    fig.set_size_inches(8, 6)
    plt.savefig('./assessment/static/assessment/radarChart/'+fileName, dpi=200)
    plt.savefig('./others/test.png', dpi=200)
    # plt.show()

def drawBarchart(scores, categories, fileName):
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.3)
    ax = fig.add_subplot(111)

    # categories = ['Availability Management', 'Capacity Management', 'Change Management', 'Configuration Managenment', 'Continuity Management', 'Financial Management', 'Incident Management', 'Problem Management', 'Release Management', 'Service Level Management']
    # scores = [4, 1, 3, 5, 1, 1, 2, 5, 1, 4]

    ax.bar(categories, scores, color="blue")

    ax.set_ylabel('Level', fontsize=8)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.savefig('./assessment/static/assessment/barChart/'+fileName, dpi=200)

def chechAndDrawResults(uid):
    ur = UserResult.objects.filter(user=uid).first()
    categoriesList = []
    statusImg = []
    data = []
    ResultPageDownContent = []
    for ucs in UserCategories.objects.filter(user=uid):
        mah = []
        categoriesList.append(ucs.category.category)
        data.append(ucs.score)
        mah.append('/'.join(ucs.category.photo.url.split('/')[3:]))
        mah.append(ucs.category.category)
        mah.append("assessment/result/management"+str(ucs.score)+".jpg")
        mah.append(ucs.score)
        mah.append(ResultPageParaghraphs.objects.filter(category=ucs.category, score=ucs.score))
        ResultPageDownContent.append(mah)
    if(ur.Change):
        drawRadarChart(data, categoriesList, ur.radarChart)
        drawBarchart(data, categoriesList, ur.barChart)
        ur.Change = False
        ur.save()
    for d in data:
        statusImg.append("assessment/result/management"+str(d)+".jpg")
    radarChartName = "assessment/radarChart/"+ur.radarChart
    barChartName = "assessment/barChart/"+ur.barChart
    return data, categoriesList, statusImg, radarChartName, barChartName, ResultPageDownContent


def getListOfTask(selectedCat, uid):
    tasksDic = {}
    for qt in Questions.objects.filter(question_fk = selectedCat):
        checkedState = False
        if(UserAnswers.objects.filter(user=uid, question=qt).first().answer.id==1):
            checkedState = True
        tasksDic[qt.id]=[checkedState,qt.task,UserAnswers.objects.filter(user=uid, question=qt).first().mdate]
    return tasksDic
        


