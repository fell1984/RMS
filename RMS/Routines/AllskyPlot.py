""" Plots points on an all-sky sinusoidal projection plot. """


import numpy as np
import matplotlib.pyplot as plt



class AllSkyPlot(object):
	def __init__(self):

		self.ra0 = 180.0

		self.fig = plt.figure()

		# Set background color
		self.fig.patch.set_facecolor('black')
		self.ax = self.fig.add_subplot(1, 1, 1, facecolor='black')

		# Set equal aspect ratio
		self.ax.set_aspect('equal')

		# # Set tick color
		# self.ax.tick_params(axis='x', colors='0.5')
		# self.ax.tick_params(axis='y', colors='0.5')

		# Turn off ticks
		self.ax.tick_params(labeltop=False, labelright=False, labelbottom=False, labelleft=False)

		self.plotGrid()


	def raDec2XY(self, ra, dec):

		# Compute projected coordinates
		x = (ra - self.ra0)*np.cos(np.radians(dec))
		y = dec

		return x, y


	def plot(self, ra_array, dec_array, max_break_deg=30, **kwargs):

		# If there are more than one point, check for 0/360 wraparounds in RA
		if isinstance(ra_array, list) or isinstance(ra_array, np.ndarray):

			ra_array = np.array(ra_array)%360
			dec_array = np.array(dec_array)

			coord_list = []

			# Find large breaks in RA and plot them separately
			ra_diff = np.abs(ra_array[:-1] - ra_array[1:])
			break_indices = np.where(ra_diff > max_break_deg)[0]

			if not len(break_indices):
				coord_list = [[ra_array, dec_array]]

			else:
				prev_break_idx = 0
				for break_idx in break_indices:
					ra_temp = ra_array[prev_break_idx:break_idx + 1]
					dec_temp = dec_array[prev_break_idx:break_idx + 1]

					prev_break_idx = break_idx + 1

					coord_list.append([ra_temp, dec_temp])

				coord_list.append([ra_array[break_idx + 1:], dec_array[break_idx + 1:]])

		else:
			coord_list = [[ra_array, dec_array]]


		# Plot all segments
		for ra_temp, dec_temp in coord_list:
			x, y = self.raDec2XY(ra_temp, dec_temp)
			plt.plot(x, y, **kwargs)



	def scatter(self, ra_array, dec_array, **kwargs):

		x, y = self.raDec2XY(ra_array, dec_array)
		plt.scatter(x, y, **kwargs)




	def plotGrid(self, step=15):


		# Plot a meridian and parallel grid
		ra_grid = np.arange(0, 360 + step, step)
		dec_grid = np.arange(-90, 90 + step, step)


		# Plot meridians
		for ra in ra_grid:

			# Increase number of points for meridian plot so they are smoother
			step_finer = step/5
			dec_arr = np.arange(-90, 90 + step_finer, step_finer)

			ra_temp = np.zeros_like(dec_arr) + ra

			x_grid, y_grid = self.raDec2XY(ra_temp, dec_arr)

			self.ax.plot(x_grid, y_grid, linestyle='dotted', alpha=0.5, color='gray')


		# Plot parallels
		for dec in dec_grid:

			dec_temp = np.zeros_like(ra_grid) + dec

			x_grid, y_grid = self.raDec2XY(ra_grid, dec_temp)

			self.ax.plot(x_grid, y_grid, linestyle='dotted', alpha=0.5, color='gray')


		# Plot ticks
		for dec in dec_grid:

			x, y = self.raDec2XY(self.ra0 + 180, dec)

			if dec > 0:
				va = 'bottom'

			else:
				va = 'top'

			self.ax.text(x, y, "{:+d}$^\circ$".format(dec), color='0.5', ha='left', va=va, size=7)

		# Plot every other RA tick and skip 0 and 360
		for ra in ra_grid[0:-1:2]:

			x, y = self.raDec2XY(ra, 0)
			self.ax.text(x, y, "{:+d}$^\circ$".format(ra), color='0.5', ha='center', va='top', size=7)




	
	def beautify(self):

		self.ax.set_xlim([-180, 180])
		self.ax.set_ylim([-90, 90])

		self.fig.tight_layout()


	def show(self):

		self.beautify()
		plt.show()






if __name__ == "__main__":

	allsky_plot = AllSkyPlot()


	ra_array = [357, 358, 359, 0, 1, 2, 3, 2, 1, 0, 359, 358, 357]
	#ra_array = [1, 2, 3, 4, 5, 6, 7]
	dec_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

	allsky_plot.plot(ra_array, dec_arr, color='green', linestyle='dashed')

	allsky_plot.show()