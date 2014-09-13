'''
Example usage (in terminal):
	import laparoscopy_performance as lp
	keyhole = lp.KeyholeSimPerformance(lp.KeyholeSimData())
	keyhole.performancesForThreadingTask()
	keyhole.correlateWithVisionSystem()
	keyhole.classifiers()
'''


import pandas as pd
import csv
import datetime
import orient.orientation as oo
import numpy as np
import json
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import resample
from scipy.stats import spearmanr, mannwhitneyu
from scipy.stats.mstats import kruskalwallis
from sklearn import svm, cross_validation
from sklearn.linear_model import LinearRegression, Ridge
from random import shuffle

# nodeID 2 == Left, nodeID 3 == right.

font = {'family' : 'normal',
		'weight' : 'bold',
		'size'   : 16}

matplotlib.rc('font', **font)

class KeyholeSimPerformance:
	def __init__(self, KeyholeSimDataInstance):
			self.db = KeyholeSimDataInstance
			self.vision_correspondence = [self.db.intermediate[9],self.db.intermediate[5],self.db.intermediate[7],self.db.novice[6],self.db.novice[5],self.db.expert[5],self.db.expert[4],self.db.expert[7],self.db.expert[8],self.db.expert[2],self.db.expert[1],self.db.novice[0],self.db.intermediate[2],self.db.intermediate[4],self.db.novice[1],self.db.intermediate[8],self.db.novice[3],self.db.intermediate[3],self.db.expert[6],self.db.intermediate[0],self.db.intermediate[1],self.db.intermediate[6],self.db.expert[3],self.db.novice[4],self.db.expert[0],self.db.novice[2]]
			self.perfsCalculated = False

	def calculatePerformances(self):
		self.novicePerfs = []
		self.intermediatePerfs = []
		self.expertPerfs = []

		for n in self.db.novice:
			self.novicePerfs.append( self.performance( n ) )
		for i in self.db.intermediate:
			self.intermediatePerfs.append( self.performance( i ) )
		for e in self.db.expert:
			self.expertPerfs.append( self.performance( e ) )
			
		self.perfsCalculated = True

	def performance(self, LR_data):
		L_duration = (LR_data[0]['currentTime'][LR_data[0].index[-1]] - LR_data[0]['currentTime'][LR_data[0].index[0]]).total_seconds()
		R_duration = (LR_data[1]['currentTime'][LR_data[1].index[-1]] - LR_data[1]['currentTime'][LR_data[1].index[0]]).total_seconds()
		duration = max(L_duration, R_duration)

		L_diff = self.db.angleDifferences( self.db.getQuaternionSequence(LR_data[0]) )
		R_diff = self.db.angleDifferences( self.db.getQuaternionSequence(LR_data[1]) )

		speedVariance = np.mean( [np.var(L_diff*100), np.var(R_diff*100)] )

		handedness = self.handedness(L_diff, R_diff)
		ambidextricity = self.ambidextricity(L_diff, R_diff)

		L_distance = sum( L_diff )
		R_distance = sum( R_diff )
		distance = L_distance + R_distance

		averageSpeed = distance / duration
		averageAccel = averageSpeed / duration

		L_motionSmoothness = np.sqrt( (L_duration**5/(2*L_distance**2)) * sum( np.diff(L_diff,2)**2 , 2) )
		R_motionSmoothness = np.sqrt( (R_duration**5/(2*R_distance**2)) * sum( np.diff(R_diff,2)**2 , 2) )
		motionSmoothness = (L_motionSmoothness + R_motionSmoothness) / 2

		return {'duration':duration, 'angularDist':distance, 'ambidextricity':ambidextricity, 'speedVariance':speedVariance, 'averageSpeed':averageSpeed, 'averageAccel':averageAccel, 'motionSmoothness':motionSmoothness, 'handedness':handedness, 'perf':((1/duration) * (1/distance))};

	def ambidextricity(self, L_angleDistances, R_angleDistances):
		if len(L_angleDistances) > len(R_angleDistances):
			L_angleDistances = resample(L_angleDistances,len(R_angleDistances))
		if len(R_angleDistances) > len(L_angleDistances):
			R_angleDistances = resample(R_angleDistances,len(L_angleDistances))
		return spearmanr(L_angleDistances, R_angleDistances)

	def handedness(self, L_angleDistances, R_angleDistances):
		if len(L_angleDistances) > len(R_angleDistances):
			L_angleDistances = resample(L_angleDistances,len(R_angleDistances))
		if len(R_angleDistances) > len(L_angleDistances):
			R_angleDistances = resample(R_angleDistances,len(L_angleDistances))
		return np.mean( np.array(R_angleDistances) - np.array(L_angleDistances) ) * 100

	def outputPerformances(self):
		print "Name\tExperience\tTask Duration\tAngular Distance\tAverage Speed\tAverage Acceleration\tMotion Smoothness\tHandedness\tSpeed Variance\tAmbidexterity"
		for s,n in zip(self.db.novice, self.db.key_novice):
			p = self.performance(s)
			print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}".format(n,'novice',p['duration'],p['angularDist'],p['averageSpeed'],p['averageAccel'],p['motionSmoothness'],p['handedness'],p['speedVariance'],p['ambidextricity'][0])

		for s,n in zip(self.db.intermediate, self.db.key_intermediate):
			p = self.performance(s)
			print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}".format(n,'intermediate',p['duration'],p['angularDist'],p['averageSpeed'],p['averageAccel'],p['motionSmoothness'],p['handedness'],p['speedVariance'],p['ambidextricity'][0])

		for s,n in zip(self.db.expert, self.db.key_expert):
			p = self.performance(s)
			print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}".format(n,'expert',p['duration'],p['angularDist'],p['averageSpeed'],p['averageAccel'],p['motionSmoothness'],p['handedness'],p['speedVariance'],p['ambidextricity'][0])

	def performancesForThreadingTask(self):
		if not self.perfsCalculated:
			self.calculatePerformances()

		durations = []
		angularDists = []
		speeds = []
		averageAccels = []
		smoothnesses = []
		handednesses = []
		speedVariances = []
		ambidexterities = []
		significances = []
		perfs = []
		for perf in self.novicePerfs+self.intermediatePerfs+self.expertPerfs:
			durations.append(perf['duration'])
			angularDists.append(perf['angularDist'])
			speeds.append(perf['averageSpeed'])
			averageAccels.append(perf['averageAccel'])
			smoothnesses.append(perf['motionSmoothness'])
			handednesses.append(perf['handedness'])
			speedVariances.append(perf['speedVariance'])
			ambidexterities.append(perf['ambidextricity'][0])
			significances.append(perf['ambidextricity'][1])
			perfs.append(perf['perf'])

		ticks = ['N'+str(i) for i in range(1,11)]+['I'+str(i) for i in range(1,11)]+['E'+str(i) for i in range(1,11)]
		colours = ['r']*10 + ['g']*10 + ['b']*10

		# Kruskal-Wallis tests (Non-parametric ANOVAS)

		# Between novices, intermediates and experts
		anova_durations = kruskalwallis(durations[0:10],durations[10:20],durations[20:30])
		anova_distances = kruskalwallis(angularDists[0:10],angularDists[10:20],angularDists[20:30])
		anova_speeds = kruskalwallis(speeds[0:10],speeds[10:20],speeds[20:30])
		anova_accels = kruskalwallis(averageAccels[0:10],averageAccels[10:20],averageAccels[20:30])
		anova_smoothness = kruskalwallis(smoothnesses[0:10],smoothnesses[10:20],smoothnesses[20:30])
		anova_handedness = kruskalwallis(handednesses[0:10],handednesses[10:20],handednesses[20:30])
		anova_variances = kruskalwallis(speedVariances[0:10],speedVariances[10:20],speedVariances[20:30])
		anova_ambidexterities = kruskalwallis(ambidexterities[0:10],ambidexterities[10:20],ambidexterities[20:30])
		anova_perfs = kruskalwallis(perfs[0:10],perfs[10:20],perfs[20:30])

		# Between experts and non-experts
		anova_two_durations = mannwhitneyu(durations[0:20],durations[20:30])
		anova_two_distances = mannwhitneyu(angularDists[0:20],angularDists[20:30])
		anova_two_speeds = mannwhitneyu(speeds[0:20],speeds[20:30])
		anova_two_accels = mannwhitneyu(averageAccels[0:20],averageAccels[20:30])
		#anova_two_smoothness = mannwhitneyu(smoothnesses[0:10]+smoothnesses[10:20],smoothnesses[20:30])
		anova_two_smoothness = mannwhitneyu(smoothnesses[0:20],smoothnesses[20:30])
		anova_two_handedness = mannwhitneyu(handednesses[0:20],handednesses[20:30])
		anova_two_variances = mannwhitneyu(speedVariances[0:20],speedVariances[20:30])
		anova_two_ambidexterities = mannwhitneyu(ambidexterities[0:20],ambidexterities[20:30])
		anova_two_perfs = mannwhitneyu(perfs[0:20],perfs[20:30])

		# SCATTER PLOTS
		def save_scatter(data,colours,title,ylabel,savePath,yLimTuple=None):
			fig = plt.figure()
			ax = fig.add_subplot(111)
			plt.title(title)
			plt.xlabel("Trials")
			plt.ylabel(ylabel)

			# Sort by value
			data, colours = zip(*sorted(zip(data, colours)))

			nov_data = [(i,d) for (i,d,c) in zip(range(len(data)), data, colours) if c=='r']
			inter_data = [(i,d) for (i,d,c) in zip(range(len(data)), data, colours) if c=='g']
			exp_data = [(i,d) for (i,d,c) in zip(range(len(data)), data, colours) if c=='b']

			nov = ax.scatter(zip(*nov_data)[0], zip(*nov_data)[1], color='r', marker='o', s=60)
			inter = ax.scatter(zip(*inter_data)[0], zip(*inter_data)[1], color='g', marker='^', s=60)
			exp = ax.scatter(zip(*exp_data)[0], zip(*exp_data)[1], color='b', marker='*', s=60)

			plt.legend((nov,inter,exp),['Novice','Intermediate','Expert'], loc=2)
			plt.xticks( [] )
			plt.gca().set_xlim(-1,len(data))
			if yLimTuple:
				plt.gca().set_xlim(yLimTuple)
			plt.tight_layout()
			with open(savePath, 'w') as figOut:
				plt.savefig(figOut)

		save_scatter(durations,colours,"Task Duration","Time (seconds)","/Users/robertevans/repos/minf/keyhole_graphs/durations.png")
		save_scatter(angularDists,colours,"Total Angular Distance","Rotation (radians)","/Users/robertevans/repos/minf/keyhole_graphs/distances.png")
		save_scatter(speeds,colours,"Average Speed","Speed (radians/second)","/Users/robertevans/repos/minf/keyhole_graphs/speeds.png")
		save_scatter(averageAccels,colours,"Average Acceleration","Acceleration (radians/second$^2$)","/Users/robertevans/repos/minf/keyhole_graphs/accels.png")
		save_scatter(smoothnesses,colours,"Motion Smoothness","Smoothness (radians/second$^3$)","/Users/robertevans/repos/minf/keyhole_graphs/smoothnesses.png")
		save_scatter(handednesses,colours,"Handedness","Right distance minus left distance per frame (radians)","/Users/robertevans/repos/minf/keyhole_graphs/handednesses.png")
		save_scatter(speedVariances,colours,"Variance of Angular Speed","Variance (radians/second)","/Users/robertevans/repos/minf/keyhole_graphs/variances.png")
		save_scatter(ambidexterities,colours,"Ambidexterity","Spearman correlation for left/right speeds (per frame)","/Users/robertevans/repos/minf/keyhole_graphs/ambidexterities.png")
		save_scatter(perfs,colours,"Total Task Performance","Score (radians$^{-1}$seconds$^{-1}$)","/Users/robertevans/repos/minf/keyhole_graphs/scores.png")

		# BOX PLOTS
		def save_box_plot(data,key,p_value,savePath,title,ylabel):
			plt.figure()
			plt.title("{0} - p-value: {1:.3g}".format(title, p_value))
			plt.ylabel(ylabel)
			plt.boxplot( data )
			plt.xticks( range(1,len(data)+1), key )
			plt.tight_layout()
			with open(savePath, 'w') as figOut:
				plt.savefig(figOut)

		save_box_plot([durations[:10], durations[10:20], durations[20:]],('Novices','Intermediates','Experts'),anova_durations[1],"/Users/robertevans/repos/minf/keyhole_graphs/durations_box_three.png","Duration","Time (seconds)")
		save_box_plot([angularDists[:10], angularDists[10:20], angularDists[20:]],('Novices','Intermediates','Experts'),anova_distances[1],"/Users/robertevans/repos/minf/keyhole_graphs/distances_box_three.png","Distance","Rotation (radians)")
		save_box_plot([speeds[:10], speeds[10:20], speeds[20:]],('Novices','Intermediates','Experts'),anova_speeds[1],"/Users/robertevans/repos/minf/keyhole_graphs/speeds_box_three.png","Speed","Speed (radians/second)")
		save_box_plot([averageAccels[:10], averageAccels[10:20], averageAccels[20:]],('Novices','Intermediates','Experts'),anova_accels[1],"/Users/robertevans/repos/minf/keyhole_graphs/accels_box_three.png","Acceleration","Acceleration (radians/second$^2$)")
		save_box_plot([smoothnesses[0:10], smoothnesses[10:20], smoothnesses[20:]],('Novices','Intermediates','Experts'),anova_smoothness[1],"/Users/robertevans/repos/minf/keyhole_graphs/smoothnesses_box_three.png","Smoothness","Smoothness (radians/second$^3$)")
		save_box_plot([handednesses[:10], handednesses[10:20], handednesses[20:]],('Novices','Intermediates','Experts'),anova_handedness[1],"/Users/robertevans/repos/minf/keyhole_graphs/handednesses_box_three.png","Handedness","Right distance minus left distance per frame (radians)")
		save_box_plot([speedVariances[:10], speedVariances[10:20], speedVariances[20:]],('Novices','Intermediates','Experts'),anova_variances[1],"/Users/robertevans/repos/minf/keyhole_graphs/variances_box_three.png","Speed Variance","Variance (radians/second)")
		save_box_plot([ambidexterities[:10], ambidexterities[10:20], ambidexterities[20:]],('Novices','Intermediates','Experts'),anova_ambidexterities[1],"/Users/robertevans/repos/minf/keyhole_graphs/ambidexterities_box_three.png","Ambidexterity","Spearman correlation for left/right speeds (per frame)")
		save_box_plot([perfs[:10], perfs[10:20], perfs[20:]],('Novices','Intermediates','Experts'),anova_perfs[1],"/Users/robertevans/repos/minf/keyhole_graphs/scores_box_three.png","Performance","Score (radians$^{-1}$seconds$^{-1}$)")

		save_box_plot([durations[:20], durations[20:]],('Non-Experts','Experts'),anova_two_durations[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/durations_box_two.png","Duration","Time (seconds)")
		save_box_plot([angularDists[:20], angularDists[20:]],('Non-Experts','Experts'),anova_two_distances[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/distances_box_two.png","Distance","Rotation (radians)")
		save_box_plot([speeds[:20], speeds[20:]],('Non-Experts','Experts'),anova_two_speeds[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/speeds_box_two.png","Speed","Speed (radians/second)")
		save_box_plot([averageAccels[:20], averageAccels[20:]],('Non-Experts','Experts'),anova_two_accels[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/accels_box_two.png","Acceleration","Acceleration (radians/second$^2$)")
		save_box_plot([smoothnesses[0:10]+smoothnesses[10:20], smoothnesses[20:]],('Non-Experts','Experts'),anova_two_smoothness[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/smoothnesses_box_two.png","Smoothness","Smoothness (radians/second$^3$)")
		save_box_plot([handednesses[:20], handednesses[20:]],('Non-Experts','Experts'),anova_two_handedness[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/handednesses_box_two.png","Handedness","Right distance minus left distance per frame (radians)")
		save_box_plot([speedVariances[:20], speedVariances[20:]],('Non-Experts','Experts'),anova_two_variances[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/variances_box_two.png","Speed Variance","Variance (radians/second)")
		save_box_plot([ambidexterities[:20], ambidexterities[20:]],('Non-Experts','Experts'),anova_two_ambidexterities[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/ambidexterities_box_two.png","Ambidexterity","Spearman correlation for left/right speeds (per frame)")
		save_box_plot([perfs[:20], perfs[20:]],('Non-Experts','Experts'),anova_two_perfs[1]*2,"/Users/robertevans/repos/minf/keyhole_graphs/scores_box_two.png","Performance","Score (radians$^{-1}$seconds$^{-1}$)")

		plt.show()

	def correlateWithVisionSystem(self):
		orient_vision_alignment = [self.db.intermediate[9],self.db.intermediate[5],self.db.intermediate[7],self.db.novice[6],self.db.novice[5],self.db.expert[5],self.db.expert[4],self.db.expert[7],self.db.expert[8],self.db.expert[2],self.db.expert[1],self.db.novice[0],self.db.intermediate[2],self.db.intermediate[4],self.db.novice[1],self.db.intermediate[8],self.db.novice[3],self.db.intermediate[3],self.db.expert[6],self.db.intermediate[0],self.db.intermediate[1],self.db.intermediate[6],self.db.expert[3],self.db.novice[4],self.db.expert[0],self.db.novice[2]]
		orient_performances = map(self.performance, orient_vision_alignment)

		colour_code = ['g','g','g','r','r','b','b','b','b','b','b','r','g','g','r','g','r','g','b','g','g','g','b','r','b','r']

		orient_durations = map(lambda d: d['duration'], orient_performances)
		orient_distances = map(lambda d: d['angularDist'], orient_performances)
		orient_speeds = map(lambda d: d['averageSpeed'], orient_performances)
		orient_accels = map(lambda d: d['averageAccel'], orient_performances)
		orient_smoothness = map(lambda d: d['motionSmoothness'], orient_performances)
		orient_handedness = map(lambda d: d['handedness'], orient_performances)

		vision_durations = [84,109,78,132,107,44,68,62,60,48,56,309,171,130,202,101,195,112,69,290,100,112,123,167,45,196]
		vision_distances = [1.52,2.36,1.86,2.91,1.47,1.28,1.33,1.35,1.74,1.19,0.98,4.23,2.9,2.69,4.68,1.55,2.97,2.3,2.21,3.45,2.63,1.73,2.05,1.96,0.77,2.4]
		vision_speeds = [3.07,3.84,4.22,4.38,2.35,5.01,3.37,4.06,5.4,4.33,2.98,2.36,3.05,3.8,4.3,2.65,2.8,3.8,6.18,2.13,4.63,3.18,2.96,2.15,2.96,2.07]
		vision_accels = [1.5,1.87,2.04,1.99,1.11,2.31,1.73,1.74,2.33,2.5,1.39,1.31,1.45,1.97,2.09,1.2,1.47,1.86,2.48,1.07,2.24,1.32,1.44,1.03,1.37,1]
		vision_smoothness = [0.09,0.09,0.14,0.08,0.05,0.29,0.14,0.15,0.21,0.28,0.13,0.02,0.04,0.08,0.05,0.06,0.04,0.1,0.19,0.02,0.12,0.06,0.06,0.03,0.16,0.02]
		vision_handedness = [1.52,0.7,0.74,1.32,1.56,1.19,1.32,1.08,1.14,0.77,1.08,1.9,1.3,1.55,0.44,1.92,0.95,1.05,1.14,1.01,0.57,1.16,0.86,1.5,1.24,1.09]

		# Remove wild outliers
		#orient_smoothness = orient_smoothness[:11]+orient_smoothness[12:]
		#vision_smoothness = vision_smoothness[:11]+vision_smoothness[12:]

		corr_durations = spearmanr(orient_durations, vision_durations)
		corr_distances = spearmanr(orient_distances, vision_distances)
		corr_speeds = spearmanr(orient_speeds, vision_speeds)
		corr_accels = spearmanr(orient_accels, vision_accels)
		corr_smoothness = spearmanr(orient_smoothness, vision_smoothness)
		corr_handedness = spearmanr(orient_handedness, vision_handedness)

		def plot_to_axis_helper(ax, orient_data, vision_data, colour_code, legend_loc):
			nov_data = [(o,v) for (o,v,c) in zip(orient_data, vision_data, colour_code) if c=='r']
			inter_data = [(o,v) for (o,v,c) in zip(orient_data, vision_data, colour_code) if c=='g']
			exp_data = [(o,v) for (o,v,c) in zip(orient_data, vision_data, colour_code) if c=='b']
			nov = ax.scatter(zip(*nov_data)[0], zip(*nov_data)[1], color='r', marker='o', s=60)
			inter = ax.scatter(zip(*inter_data)[0], zip(*inter_data)[1], color='g', marker='^', s=60)
			exp = ax.scatter(zip(*exp_data)[0], zip(*exp_data)[1], color='b', marker='*', s=60)
			plt.legend((nov,inter,exp),['Novice','Intermediate','Expert'], loc=legend_loc)

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.xlabel('Orient Duration (seconds)')
		plt.ylabel('Vision Duration (seconds)')
		plt.title("Task Duration\nSpearman Correlation: {0:.3g} p-value: {1:.3g}".format(corr_durations[0], corr_durations[1]))
		plot_to_axis_helper(ax, orient_durations, vision_durations, colour_code, 2)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/durations_corr.png", 'w') as figOut:
			plt.savefig(figOut)

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.xlabel('Angular Distance (radians)')
		plt.ylabel('Visual Distance (metres)')
		plt.title("Total Distance\nSpearman Correlation: {0:.3g} p-value: {1:.3g}".format(corr_distances[0], corr_distances[1]))
		plot_to_axis_helper(ax, orient_distances, vision_distances, colour_code, 2)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/distances_corr.png", 'w') as figOut:
			plt.savefig(figOut)

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.xlabel('Angular Speed (radians per second)')
		plt.ylabel('Visual Speed (metres per second)')
		plt.title("Average Speed\nSpearman Correlation: {0:.3g} p-value: {1:.3g}".format(corr_speeds[0], corr_speeds[1]))
		plot_to_axis_helper(ax, orient_speeds, vision_speeds, colour_code, 2)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/speeds_corr.png", 'w') as figOut:
			plt.savefig(figOut)

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.xlabel('Angular Acceleration (radians per second$^2$)')
		plt.ylabel('Visual Acceleration (metres per second$^2$)')
		plt.title("Average Acceleration\nSpearman Correlation: {0:.3g} p-value: {1:.3g}".format(corr_accels[0], corr_accels[1]))
		plot_to_axis_helper(ax, orient_accels, vision_accels, colour_code, 4)
		plt.gca().set_xlim(0,0.002)
		plt.gca().set_ylim(0.8,2.6)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/accels_corr.png", 'w') as figOut:
			plt.savefig(figOut)

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.xlabel('Angular Smoothness (radians per second$^3$)')
		plt.ylabel('Visual Smoothness (metres per second$^3$)')
		plt.title("Motion Smoothness\nSpearman Correlation: {0:.3g} p-value: {1:.3g}".format(corr_smoothness[0], corr_smoothness[1]))
		plot_to_axis_helper(ax, orient_smoothness, vision_smoothness, colour_code, 1)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/smoothnesses_corr.png", 'w') as figOut:
			plt.savefig(figOut)

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.xlabel('Orient Handedness bias (radians)')
		plt.ylabel('Visual Handedness bias (metres)')
		plt.title("Handedness\nSpearman Correlation: {0:.3g} p-value: {1:.3g}".format(corr_handedness[0], corr_handedness[1]))
		plot_to_axis_helper(ax, orient_handedness, vision_handedness, colour_code, 2)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/handednesses_corr.png", 'w') as figOut:
			plt.savefig(figOut)

		plt.show()

	def angularVelocityHistsForThreadingTask(self):
		# Not working (code was written for old data format and hasn't been updated)
		plt.figure()
		plt.title("Expert: Angular Velocity Distribution")
		plt.hist(self.diffs[0]+self.diffs[1], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.figure()
		plt.title("Novice 1: Angular Velocity Distribution")
		plt.hist(self.diffs[2]+self.diffs[3], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.figure()
		plt.title("Novice 2: Angular Velocity Distribution")
		plt.hist(self.diffs[4]+self.diffs[5], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.figure()
		plt.title("Novice 3: Angular Velocity Distribution")
		plt.hist(self.diffs[6]+self.diffs[7], normed=True, stacked=True, range=(0,3.15))
		plt.ylim([0,1.2])

		plt.show()

	def plotLR(self, LRdata, columns=['gyroX','gyroY','gyroZ','accelX','accelY','accelZ','magX','magY','magZ']):
		plt.figure()
		plt.suptitle("Both hands data")
		h1 = plt.subplot(2,1,1)
		plt.title("Left hand")
		plt.plot(LRdata[0][columns])
		#LRdata[0].plot(x=['currentTime'])
		h2 = plt.subplot(2,1,2, sharex=h1, sharey=h1)
		plt.title("Right hand")
		#LRdata[1].plot(x=['currentTime'])
		plt.plot(LRdata[1][columns])
		plt.show()

	def classifiers(self):
		# Get performance data.  A less busy person would put this in its own function.
		if not self.perfsCalculated:
			self.calculatePerformances()	

		accels = map(lambda x: x['averageAccel'], self.novicePerfs+self.intermediatePerfs+self.expertPerfs)
		durations = map(lambda x: x['duration'], self.novicePerfs+self.intermediatePerfs+self.expertPerfs)
		smooths = map(lambda x: x['motionSmoothness'], self.novicePerfs+self.intermediatePerfs+self.expertPerfs)
		distances = map(lambda x: x['angularDist'], self.novicePerfs+self.intermediatePerfs+self.expertPerfs)
		ambidexterities = map(lambda x: x['ambidextricity'][0], self.novicePerfs+self.intermediatePerfs+self.expertPerfs)

		# Make feature and target vectors
		X = np.array(zip(accels,durations,smooths,distances,ambidexterities))
		y = np.array([0]*10 + [0.25, 1.0/3, 1.0/3, 0.5, 0.5, 0.5, 2, 2, 2, 2] + [6, 6, 6, 8, 8, 8, 10, 10, 10, 6]) # Experience levels in years
		#y = np.array([0]*10 + [1]*10 + [2]*10)

		'''
		paired = zip(X,y)
		shuffle(paired)
		X,y = map(np.array, zip(*paired))
		'''

		def resolveClass(y):
			if y <= 0.1:
				return 'r'
			if y <= 2:
				return 'g'
			else:
				return 'b'

		# Cross validation
		all_colours = []
		all_regressions = []
		indexes = []
		skf = cross_validation.StratifiedKFold(map(resolveClass,y), n_folds=10)
		for train_index, test_index in skf:
			indexes.extend(test_index)

			X_train, X_test = X[train_index], X[test_index]
			y_train, y_test = y[train_index], y[test_index]
			linearRegressor = LinearRegression(normalize=True).fit(X_train,y_train)
			regressions = map( linearRegressor.decision_function, X_test)
			class_colours = map( resolveClass, y_test )

			all_regressions.extend(regressions)	
			all_colours.extend(class_colours)
			
			print linearRegressor.intercept_, linearRegressor.coef_
			"""
			# Plot
			classes = zip(regressions, class_colours)
			plt.figure()
			plt.title("Least Squares Fitted Performace")
			plt.xlabel("Trials")
			plt.ylabel("Score")
			zippedAndSorted = sorted(zip(regressions,class_colours))
			unzipped = zip(*zippedAndSorted)
			plt.scatter(range(len(unzipped[0])), unzipped[0], c=unzipped[1], s=60)
			nov = plt.scatter([], [], color='r')
			inter = plt.scatter([], [], color='g')
			exp = plt.scatter([], [], color='b')
			plt.legend((nov,inter,exp),['Novice','Intermediate','Expert'], loc=2)
			plt.xticks( [] )
			#plt.gca().set_xlim(-1,15)
			#plt.gca().set_ylim(-4,6)
			plt.tight_layout()
			plt.show()
			"""


		# Make test and training set 
		#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.5)
		# Fit linear regressor to weights
		#linearFit = LinearRegression().fit(X_train,y_train)
		#regressions = map( lambda x: linearFit.intercept_ + sum(np.array(x) * linearFit.coef_), X_test)

		#colours = map( resolveClass, y_test )

		classes = zip(all_regressions, all_colours)

		anova_perfs = kruskalwallis([t[0] for t in classes if t[1] == 'r'],[t[0] for t in classes if t[1] == 'g'],[t[0] for t in classes if t[1] == 'b'])

		fig = plt.figure()
		ax = fig.add_subplot(111)
		plt.title("Linear Performance Score")
		plt.xlabel("Trials")
		plt.ylabel("Score")

		# Sort by value
		all_regressions, all_colours = zip(*sorted(zip(all_regressions, all_colours)))

		# Plot each experience level with different markers and colours
		nov_data = [(i,d) for (i,d,c) in zip(range(len(all_regressions)), all_regressions, all_colours) if c=='r']
		inter_data = [(i,d) for (i,d,c) in zip(range(len(all_regressions)), all_regressions, all_colours) if c=='g']
		exp_data = [(i,d) for (i,d,c) in zip(range(len(all_regressions)), all_regressions, all_colours) if c=='b']
		nov = ax.scatter(zip(*nov_data)[0], zip(*nov_data)[1], color='r', marker='o', s=60)
		inter = ax.scatter(zip(*inter_data)[0], zip(*inter_data)[1], color='g', marker='^', s=60)
		exp = ax.scatter(zip(*exp_data)[0], zip(*exp_data)[1], color='b', marker='*', s=60)

		plt.legend((nov,inter,exp),['Novice','Intermediate','Expert'], loc=2)
		plt.xticks( [] )
		#plt.gca().set_xlim(-1,15)
		#plt.gca().set_ylim(-4,6)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/linFit.png", 'w') as figOut:
			plt.savefig(figOut)

		plt.figure()
		plt.title("Kruskal-Wallis p-value: {0:.3g}".format(anova_perfs[1]))
		plt.ylabel("Score")
		plt.boxplot( [[t[0] for t in classes if t[1] == 'r'],[t[0] for t in classes if t[1] == 'g'],[t[0] for t in classes if t[1] == 'b']] )
		plt.xticks( range(1,4), ('Novices', 'Intermediates', 'Experts') )
		#plt.gca().set_ylim(0,9)
		plt.tight_layout()
		with open("/Users/robertevans/repos/minf/keyhole_graphs/linFit_box.png", 'w') as figOut:
			plt.savefig(figOut)

		plt.show()

class KeyholeSimData:
	def __init__(self):
		with open('/Users/robertevans/repos/minf/captures/keyhole/session1/expertTouchingBases.csv','r') as csvfile:
			self.__csv_dialect = csv.Sniffer().sniff(csvfile.read())
			self.__date_parser = lambda x: datetime.datetime.fromtimestamp(x) if not np.isnan(x) else x
		self.loadAll()

	def loadAll(self):
		session1 = '/Users/robertevans/repos/minf/captures/keyhole/session1/'
		session2 = '/Users/robertevans/repos/minf/captures/keyhole/session2/'
		novices = [session2+'abhishek', session2+'adeline', session2+'gabby', session2+'john', session2+'robert1', session2+'robert2', session2+'rui', session1+'noviceRoland1', session1+'noviceRobert2', session1+'noviceCristie3']
		intermediates = [session2+'gregory', session2+'arthur', session2+'kevinC', session2+'kevin', session2+'kirsty1', session2+'kirsty2', session2+'michael1', session2+'michael2', session2+'namal1', session2+'namal2']
		experts = [session2+'roland1', session2+'roland2', session2+'roland3', session2+'ross1', session2+'ross2', session2+'ross3', session2+'iain1', session2+'iain2', session2+'iain3', session1+'expertRoland1']
		self.key_novice = ['abhishek', 'adeline', 'gabby', 'john', 'robert1', 'robert2', 'rui', 'noviceRoland1', 'noviceRobert2', 'noviceCristie3']
		self.key_intermediate = ['gregory', 'arthur', 'kevinC', 'kevin', 'kirsty1', 'kirsty2', 'michael1', 'michael2', 'namal1', 'namal2']
		self.key_expert = ['roland1', 'roland2', 'roland3', 'ross1', 'ross2', 'ross3', 'iain1', 'iain2', 'iain3', 'expertRoland1']

		self.novice =[]
		self.intermediate = []
		self.expert = []
		self.quats_novice = []
		self.quats_intermediate = []
		self.quats_expert = []
		self.diffs_novice = []
		self.diffs_intermediate = []
		self.diffs_expert = []

		# Trim data to just the task timestamps from the videos
		trimTimes = {'abhishek':(1395489767,1395490086),'adeline':(1395488797,1395489009),'arthur':(1395487005,1395487115),'gabby':(1395485614,1395485820),'gregory':(1395487242,1395487542),'iain3':(1395490447,1395490517),'iain2':(1395490596,1395490668),'iain1':(1395487590,1395487669),'john':(1395488047,1395488252),'kevin':(1395487809,1395487931),'kevinC':(1395489495,1395489676),'kirsty2':(1395492040,1395492159),'kirsty1':(1395489142,1395489282),'michael2':(1395491862,1395491950),'michael1':(1395486774,1395486896),'namal2':(1395492317,1395492411),'namal1':(1395488490,1395488601),'robert1':(1395486049,1395486226),'robert2':(1395491472,1395491589),'roland2':(1395490168,1395490234),'roland3':(1395490273,1395490331),'ross2':(1395490761,1395490839),'ross3':(1395490884,1395490938),'ross1':(1395486524,1395486657),'roland1':(1395485924,1395485979),'rui':(1395491668,1395491810),'noviceRoland1':(130000000,1395500000),'noviceRobert2':(130000000,1395500000),'noviceCristie3':(130000000,1395500000),'expertRoland1':(130000000,1395500000)}
		def trim(TwoNodesData, Ltrim, Rtrim):
			TwoNodesData[0] = TwoNodesData[0][TwoNodesData[0]['currentTime']>Ltrim][TwoNodesData[0]['currentTime']<Rtrim]
			TwoNodesData[1] = TwoNodesData[1][TwoNodesData[1]['currentTime']>Ltrim][TwoNodesData[1]['currentTime']<Rtrim]
			return TwoNodesData

		print "Loading data..."
		for n in novices:
			self.novice.append( self.parse_csv(n+'.csv') )
			name = n.split('/')[-1]
			Ltrim = datetime.datetime.fromtimestamp( trimTimes[name][0] )
			Rtrim = datetime.datetime.fromtimestamp( trimTimes[name][1] )
			self.novice[-1] = trim(self.novice[-1], Ltrim, Rtrim )
		for i in intermediates:
			self.intermediate.append( self.parse_csv(i+'.csv') )
			name = i.split('/')[-1]
			Ltrim = datetime.datetime.fromtimestamp( trimTimes[name][0] )
			Rtrim = datetime.datetime.fromtimestamp( trimTimes[name][1] )
			self.intermediate[-1] = trim(self.intermediate[-1], Ltrim, Rtrim )
		for e in experts:
			self.expert.append( self.parse_csv(e+'.csv') )
			name = e.split('/')[-1]
			Ltrim = datetime.datetime.fromtimestamp( trimTimes[name][0] )
			Rtrim = datetime.datetime.fromtimestamp( trimTimes[name][1] )
			self.expert[-1] = trim(self.expert[-1], Ltrim, Rtrim )

		print "Calculating quaternions..."
		for i,d in enumerate(self.novice):
			print "%i / %i..."%(i+1,len(self.novice)+len(self.intermediate)+len(self.expert))
			L_quats = self.getQuaternionSequence(d[0])
			R_quats = self.getQuaternionSequence(d[1])
			self.quats_novice.append( (L_quats, R_quats) )
		for i,d in enumerate(self.intermediate):
			print "%i / %i..."%(len(self.novice)+i+1,len(self.novice)+len(self.intermediate)+len(self.expert))
			L_quats = self.getQuaternionSequence(d[0])
			R_quats = self.getQuaternionSequence(d[1])
			self.quats_intermediate.append( (L_quats, R_quats) )
		for i,d in enumerate(self.expert):
			print "%i / %i..."%(len(self.novice)+len(self.intermediate)+i+1,len(self.novice)+len(self.intermediate)+len(self.expert))
			L_quats = self.getQuaternionSequence(d[0])
			R_quats = self.getQuaternionSequence(d[1])
			self.quats_expert.append( (L_quats, R_quats) )

		print "Computing quaternion differences..."
		for qs in self.quats_novice:
			L_diffs = self.angleDifferences(qs[0])
			R_diffs = self.angleDifferences(qs[1])
			self.diffs_novice.append( (L_diffs, R_diffs) )
		for qs in self.quats_intermediate:
			L_diffs = self.angleDifferences(qs[0])
			R_diffs = self.angleDifferences(qs[1])
			self.diffs_intermediate.append( (L_diffs, R_diffs) )
		for qs in self.quats_expert:
			L_diffs = self.angleDifferences(qs[0])
			R_diffs = self.angleDifferences(qs[1])
			self.diffs_expert.append( (L_diffs, R_diffs) )

	def parse_csv(self, filepath):
		table = pd.read_table(filepath, dialect=self.__csv_dialect, usecols=[0,4,5,6,8,9,10,12,13,14,15], parse_dates=[10], date_parser=self.__date_parser)
		sensors = table.groupby('nodeID')
		return [sensors.get_group(i).drop('nodeID',1) for i in sensors.indices if len(sensors.get_group(i))>10]

	def getQuaternionSequence(self, DataFrame):
		orientationEstimator = oo.OrientCF(oo.Quaternion(0,0,0,1),k=0.5,aT=0.1)
		quaternionSequence = [oo.Quaternion(0,0,0,1)]

		dt = 1e-04
		prev = DataFrame.index[0]
		for i in DataFrame.index[1:]:
			accel = np.float64( np.array( [[DataFrame.accelX[i]],[DataFrame.accelY[i]],[DataFrame.accelZ[i]]] ) )
			mag = np.float64( np.array( [[DataFrame.magX[i]],[DataFrame.magY[i]],[DataFrame.magZ[i]]] ) )
			gyro = np.float64( np.array( [[DataFrame.gyroX[i]],[DataFrame.gyroY[i]],[DataFrame.gyroZ[i]]] ) )
			if not any(map(np.isnan,[item for sublist in accel.tolist()+mag.tolist()+gyro.tolist() for item in sublist])):
				quat = orientationEstimator.update(accel, mag, gyro, dt)
				quaternionSequence.append( quat.copy() )
			prev = i

		return quaternionSequence

	def angleDifferences(self, quaternionSequence):
		angle_differences = []
		for i in range(len(quaternionSequence)-1):
			q1 = quaternionSequence[i]
			q2 = quaternionSequence[i+1]
			quaternion_difference = (q1**-1)*q2
			angle_differences.append( quaternion_difference.toAxisAngle()[1] )
		return np.radians(angle_differences)

	def dumpJSONrotationMatricies(self, quatsIndex, filepath):
		rotation_matricies = []
		for q in self.quats[quatsIndex]:
			rotation_matricies.append(q.toMatrix().tolist())
		with open(filepath, 'w') as jsonfile:
			jsonfile.write(json.JSONEncoder().encode(rotation_matricies))

	def dumpJSONeuler(self, quatsIndex, filepath):
		rotation_matricies = []
		for q in self.quats[quatsIndex]:
			rotation_matricies.append(q.toEuler().tolist())
		with open(filepath, 'w') as jsonfile:
			jsonfile.write(json.JSONEncoder().encode(rotation_matricies))



