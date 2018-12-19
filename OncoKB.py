#!/usr/bin/env python

import requests, os, datetime


class OncoKB_parsing():
	def __init__(self):
		print("START\n")
		temp_today = datetime.datetime.today()
		self.today = str(temp_today).split(" ")[0]
		print(temp_today)

	def OncoKB_download(self, url, input_path):
		data = requests.get(url)
		r_data = data.text
		self.r_list = r_data.splitlines()
		#OncoKB making
		if not os.path.exists(input_path): os.makedirs(input_path)
		OncoKB_down = '{0}/OncoKB_allActionableVariants_{1}'.format(input_path, self.today)
		with open(OncoKB_down, 'w') as w:
			w.write(r_data.encode('utf-8'))

	def OncoKB_processing(self, output_path):
		if not os.path.exists(output_path): os.makedirs(output_path)
		output_path_n = os.path.join(output_path, "Parsed_OncoKB_{0}".format(self.today))
		with open(output_path_n, "w") as w:
			header = '\t'.join(['P_change', 'Gene', 'Transcript', 'Disease', 'Drug', 'Level']) + '\n'
			w.write(header)
			for line in self.r_list[1:]:
				line = line.encode('utf-8')
				line_split = line.split('\t')
				P_change = line_split[5] ; Gene = line_split[3]
				Transcript = line_split[0]
				cancer = line_split[6] ; Level = line_split[7] ; Drug = line_split[8] ; Source =line_split[9]
				out_result = '\t'.join([P_change, Gene, Transcript, cancer, Drug, Level]) + '\n'
				w.write(out_result)

if __name__ == '__main__':

	url = "http://oncokb.org/api/v1/utils/allActionableVariants.txt"
	input_path = 'Input'
	output_path = 'Output'

	#OncoKB_Class
	go = OncoKB_parsing()
	#OncoKB_ActionableAlteration_Download_lastest
	go.OncoKB_download(url, input_path)
	# #OncoKB_Parsing
	go.OncoKB_processing(output_path)

	print("\nEND")