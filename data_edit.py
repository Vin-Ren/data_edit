"""
data_edit is a module to assist data editing such as reformatting, sorting, duplicate removal, etc.


Function Lists:
remove_duplicate(unfilteredlist:list): 
Returns the filtered list

sort_data(_list:list, attribute:str): 
Returns the sorted data according to the given attribute

reformat_data(data:list, attributes:list): 
Reformat your data according to the given attribute
Returns the reformatted data

reformat_file(sourcefilename:str, savefilename:str, attributes:list): 
Reformat a file(sourcefilename) with reformat_data(attributes=attributes)
and saving the reformatted data to the new file(savefilename)
Returns tuple (status code, process info)
process info = {"data_lengths":list, "time_elapsed":float} if status code is 0

join_files(sourcedir:str, file:str, attrs=None, cout=False):
if cout is True: prints progress indicator. Ex: Processing 1 of 10

Joins your files from the directory(sourcedir) and 
using reformat_data(attributes=attrs) for each filedata if attrs is not None. 
Saves the joined file(file)
Returns tuple (status code, process info)
process info is a dictionary consist of {data_lenghts:list, time_elapsed:float, filtered_by_attrs:bool, source_files:list} 

main(): 
A mini demo for reformat_file & join_files.
"""

import json
import os
import time


def remove_duplicate(unfilteredlist:list):
	filteredlist = []
	for i in unfilteredlist:
		if i not in filteredlist:
			filteredlist.append(i)
	return filteredlist


def sort_data(_list:list, attribute:str):
	sorted(_list, key=lambda k: k[attribute])
	return _list


def reformat_data(data:list, attributes:list):
	newdata = [] # Making the return data
	for item in data:
		try:
			newdata.append({attr: item[attr] for attr in attributes})
			# Appends only if the item has all the attributes listed, else continue
		except KeyError:continue
	return newdata


def reformat_file(sourcefilename:str, savefilename:str, attributes:list):
	try:
		start_time = time.time() # Takes the current time

		with open(sourcefilename, "r") as file:
			data = json.load(file) # Load sourcefile's data
		start_length = len(data) # Check data lenght(start lenght)

		data = reformat_data(data, attributes=attributes) # Pass loaded data to reformat and attributes as it is.

		end_length = len(data) # Check data length(end length)
		with open(savefilename, "w") as file:
			json.dump(data, file, indent=4) # Dump reformated_data

		total_time = time.time()-start_time # Counting total time elapsed since start of process(is not rounded)

		return 0, {"data_lengths": [start_length, end_length], "time_elapsed": total_time}
		# 0 as all went well, {dict} with information of process

	except Exception as e:
		return 1, e
		# 1 as there is something wrong, Exception


def join_files(sourcedir:str, file:str, attrs=None, cout=False):
	try:
		# Statistics Collection
		start = time.time()
		start_length = 0


		joined_data = []

		file_list = os.listdir(sourcedir)
		for i, fl in enumerate(file_list):
			if cout:
				print(f"{f'Processing {i+1} of {len(file_list)}':<50}", end="\r") # Debugging

			with open(f"{sourcedir}/{fl}", "r") as fl:
				data = json.load(fl)
				start_length += len(data)

			if attrs: # If attributes were passed, reformat data first, then continue.
				data = reformat_data(data, attrs)

			joined_data.extend(data)

		end_length = len(joined_data) # By logic, joined_data is all the data combined.

		if cout:
			print(f"{f'Saving Data to {file}':<50}", end="\r")
		with open(file, "w") as file:
			json.dump(joined_data, file, indent=4)

		total_time = time.time() - start

		process_info = {"data_lengths": [start_length, end_length], "time_elapsed": total_time, "filtered_by_attrs": False if attrs is None else True, "source_files": file_list}
		return 0, process_info
	except Exception as e:return 1, e


def main():
	# Constants
	attribute_presets = [
		['id', 'score', 'rating', 'file_url'],
		['id', 'score', 'rating', 'file_url', 'tag_string']]

	def get_attribute():
		#print("\n--Attributes--\n[1][id, score, rating, file_url]\n[2][id, score, rating, file_url, tag_string]")
		print("\n--Attributes--")
		for i, preset in enumerate(attribute_presets):
			preset = str(preset).replace('\'', '')
			print(f"[{i+1}]{preset}")
		print("Type Yourself For Other Attribute Set. Ex: id,score,rating,file_url")
		print("Please Be Consistent With Your Use Of Attribute Seperator [,]\nIf only 1 attribute, enter the attribute without seperators.")
		attribute_input = input("Attributes:") # Asking for attributes to use
		try:
			attribute_set = attribute_presets[int(attribute_input)-1]
		except ValueError:
			try:
				attribute_set = attribute_input.split(", ")
			except:
				attribute_set = attribute_input.split(",")
		except IndexError:
			print("There Is No Preset On That Index. Using The Second Preset.")
			attribute_set = attribute_presets[1]
		return attribute_set

	while True:
		os.system("clear")
		os.system("cls")
		try:
			# Main Menu
			print("--Data Edit Demo--")
			print("[1]Reformat A File\n[2]Reformat All Files Of A Directory\n[3]Join Files\n[X]Exit")
			choice = int(input("Choice:"))

			if choice == 1:
				# Reformat A File
				print("\n--Reformat A File--")
				sourcefile=input("Source File     :")
				savefile = input("Reformatted File:")

				# Attribute Setting
				attribute_set = get_attribute()

				# Processing The Action
				if input("All Requirements Satisfied.\nWould You Like To Proceed(y/n)?").lower() in ['yes', 'ye', 'y']:
					print("Processing...")
					reformat_info = reformat_file(sourcefile, savefile, attribute_set)


					if reformat_info[0] == 0:
						# Printing Process Informations
						info = reformat_info[1]
						print(f"Data Length: {info['data_lengths'][0]}\nReformatted Data Length: {info['data_lengths'][1]}")
						print(f"Time Elapsed: {round(info['time_elapsed'], ndigits=2)} Seconds")
					else:
						print("Error: ",reformat_info[1])
					input("Press Any Key To Return.")
				else:continue

			if choice == 2:
				# Reformat All Files In A Directory
				print("\n--Reformat Files In Directory--")
				print("Only Reformatting If File Extension is json")
				print("Make sure you enter a valid directory be it source or reformatted.")
				sourcedir=input("Source Directory     :")
				savedir = input("Reformatted Directory:")

				# Attribute Setting
				attribute_set = get_attribute()

				print("All Requirements Satisfied.")

				# Printing Eligble Files
				try:
					file_list = [flname for flname in os.listdir(sourcedir) if flname.endswith(".json")]
					for i, flname in enumerate(file_list):
						print(f"{i+1}. {flname[:-5]}")
				except Exception as e:
					input(f"Error:{e}\nPress Enter To Exit.")
					exit()

				# Processing The Action
				if input("Above are the files.\nWould You Like To Proceed(y/n)?").lower() in ['yes', 'ye', 'y']:
					print("Processing...")
					total_time = 0
					total_data_len = 0
					total_reformatted_len = 0
					errors = []
					for index, file in enumerate(file_list):
						print(f"{f'[{index+1}/{len(file_list)}] Processing {file[:-5]}':<100}", end="\r")
						sourcefile = f"{sourcedir}/{file}"
						savefile = f"{savedir}/{file}"
						reformat_info = reformat_file(sourcefile, savefile, attribute_set)

						# Appending Process Informations
						if reformat_info[0] == 0:
							info = reformat_info[1]
							total_data_len += info['data_lengths'][0]
							total_reformatted_len += info['data_lengths'][1]
							total_time += info['time_elapsed']
						else:
							errors.append((file,f"Error: {reformat_info[1]}"))
					print("\n\nDone Processing.")

					# Printing Processess Informations
					print(f"Total Data Length: {total_data_len}\nTotal Reformatted Data Length: {total_reformatted_len}")
					print(f"Total Processing Time: {round(total_time, ndigits=2)} Seconds")
					if errors != []:
						print(f"--Errors--")
						for file, error in errors:
							print(f"{file}: {error}")
					input("Press Any Key To Return.")
				else:continue

			if choice == 3:
				# Joins A Directory Files To A File
				print("\n--Join Files--")
				print("Make sure you enter a valid source directory.")
				sourcedir=input("Source Directory:")
				savefile =input("Joined File     :")

				# Set Attribute
				print("\n--Reformat Data--")
				print("Do you want to reformat the data?")
				if input("Choice(y/n)?").lower() == "y":
					attrs = get_attribute()
					print(f"Attributes: {attrs}")
				else:
					attrs = None

				# Set cout Boolean
				print("\n--Progress Indicator--")
				print("Do you want to see the progress indicator?")
				if input("Choice(y/n)?").lower() == "y":
					cout = True
				else: cout = False

				# Processing Request
				print("\nAll Requirements Satisfied. Do You With To Proceed?")
				if input("Choice(y/n)?").lower() == "y":
					
					print("Processing...")
					process_info = join_files(sourcedir, savefile, attrs, cout)
					print(f"{'Done Processing.':<50}")

					if process_info[0] == 0:
						# Prints result info
						info = process_info[1]
						print(f"Total Data Length: {info['data_lengths'][0]}\nTotal Joined Length: {info['data_lengths'][1]}")
						print(f"Total Time Elapsed: {round(info['time_elapsed'], ndigits=2)} Seconds")
						print(f"Filtered: {info['filtered_by_attrs']}")
						
						print("Source Files:")
						for i, file in enumerate(info['source_files']):
							print(f"{i+1}. {file}")
					else:
						print("Error Catched.")
						print(process_info[1])
					input("Press Any Key To Return.")
				else:continue

		except KeyboardInterrupt:
			input("\nPress Enter To Exit.")
			exit()
		except ValueError: exit()
		except Exception as e:
			input(f"Error:{e}\nPress Enter To Exit.")
			exit()


if __name__ == "__main__":
	main()
