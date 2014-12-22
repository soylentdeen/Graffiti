import scipy
import pyfits
import matplotlib.pyplot as pyplot

fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

d1 = pyfits.getdata("HOCtr.ACT_POS_REF_MAP.fits")
d2 = pyfits.getdata("original.fits")
d3 = pyfits.getdata("saved.fits")
d4 = pyfits.getdata("old.fits")

ax.plot(d1[0], color = 'r')
ax.plot(d2, color = 'b')
ax.plot(d3[0], color = 'k')
ax.plot(d4[0], color = 'g')

fig.canvas.draw()
fig.show()
