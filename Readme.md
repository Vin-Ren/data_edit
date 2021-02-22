#Data Edit

##Example use:
```py
import data_edit as de # as de to make our lives easier

# data_edit supports datatypes such as data_set:
data_set = [{'id': 1, 'name':'John', 'age': 20}, {'id': 2, 'name':'Sarah', 'age': 20}]

# Calling the function
reformatted_data = de.reformat_data(data_set, ['id', 'name'])

print('id and name only:\n', reformat_data)
```

##Functions
Function Lists:

`remove_duplicate(unfilteredlist:list):`
Returns the filtered list


`sort_data(_list:list, attribute:str):` 
Returns the sorted data according to the given attribute


`reformat_data(data:list, attributes:list):`
Returns the reformatted data


`reformat_file(sourcefilename:str, savefilename:str, attributes:list):` 
Reformat sourcefilename with reformat_data and saving the reformatted data to savefilename
Returns tuple (status code, process info)


`join_files(sourcedir:str, file:str, attrs=None, cout=False):`
cout signifies whether to output progress indicator or not

Joins your json files from the sourcedir and using reformat_data for each filedata if passed attrs. 
Saves the joined file
Returns tuple (status code, process info)


`main():`
A mini demo for reformat_file & join_files.