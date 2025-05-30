import os


def file_name_converter(uc):
	'''
	This function converts all the spaces of a string into the following char: _
	It is used to name the csv files.
	'''
	if ' ' in str(uc):
		return (str(uc)).replace(' ', '_')
	return str(uc)


def fill_csv(uc, info):
	'''
	This function fills both csv files, one with the information of shifts and other with the information of students allocation
	'''

	buffer = ""
	for type_class in info[uc]:
		for shift in info[uc][type_class]:
				buffer += f"\"{uc}-{type_class}{shift}\",\"{uc}-{type_class}{shift}\",\"\",\"\",S,\"\",N,\"\",\"\",\"\",\"\",\"\"\n"

	path_compare = os.path.join("parser", "parser_csv_ucs.py")
	if(os.path.relpath(__file__) == path_compare):
		path_shifts = os.path.join("OutputCsvUcs", file_name_converter(uc))  + "_turnos.csv"

		if not os.path.exists("OutputCsvUcs"):
			os.makedirs("OutputCsvUcs")
			print("Directory ", "OutputCsvUcs", " Created ")

	else:
		path = os.path.join("..", "schedule", "schedule", "output", "OutputCsvUcs", file_name_converter(uc))
		path_shifts = path + "_turnos.csv"

		if not os.path.exists(path):
			os.makedirs(path)
			print("Directory ", path, " Created ")



	file_shifts = open(path_shifts, "a")
	file_shifts.write(buffer)
	file_shifts.close()

	buffer = ""
	for type_class in info[uc]:
		for shift in info[uc][type_class]:
			for student in info[uc][type_class][shift]:
				buffer += f"\"{uc}-{type_class}{shift}\",\"{student}\",\"{student}\",\"{student}\",\".\"\n"

	
	path_compare = os.path.join("parser", "parser_csv_ucs.py")
	if(os.path.relpath(__file__) == path_compare):
		path_students = os.path.join("OutputCsvUcs", file_name_converter(uc)) + "_alunos.csv"
	else:
		path_students = os.path.join("..", "schedule", "schedule", "output", "OutputCsvUcs", file_name_converter(uc)) + "_alunos.csv"
	
	file_students = open(path_students, "a")
	file_students.write(buffer)
	file_students.close()



def parser_csv_ucs(solver, P):
	'''
	This function returns a dictionary with all students allocated of each shift for all ucs
	It already creates all the csv files with the necessary information
	'''
	info = {}
	for student in P:
		for year in P[student]:
			for semester in P[student][year]:
				for uc in P[student][year][semester]:
					if uc not in info:
						info[uc] = {}
					for type_class in P[student][year][semester][uc]:
						if type_class != "T":
							if type_class not in info[uc]:
								info[uc][type_class] = {}
							for shift in P[student][year][semester][uc][type_class]:
								if shift not in info[uc][type_class]:
									info[uc][type_class][shift] = list()
								if (solver.Value(P[student][year][semester][uc][type_class][shift]) == 1):
									info[uc][type_class][shift].append("a" + str(student[1:]))


	for uc in info:
		fill_csv(uc, info)

  		


