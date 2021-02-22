# Data Edit

## Example use:
```py
import data_edit as de # as de to make our lives easier

# data_edit supports datatypes such as data_set:
data_set = [{'id': 1, 'name':'John', 'age': 20}, {'id': 2, 'name':'Sarah', 'age': 20}]

# Calling the function
reformatted_data = de.reformat_data(data_set, ['id', 'name'])

print('id and name only:\n', reformatted_data)
```

## Functions

`remove_duplicate(unfilteredlist:list):`

Returns the filtered list
<br>

`sort_data(_list:list, attribute:str):` 

Returns the sorted data according to the given attribute
<br>

`reformat_data(data:list, attributes:list):`

Returns the reformatted data
<br>

`reformat_file(sourcefilename:str, savefilename:str, attributes:list):` 

Reformat sourcefilename with reformat_data and saving the reformatted data to savefilename
Returns tuple (status code, process info)
<br>

`join_files(sourcedir:str, file:str, attrs=None, cout=False):`

cout signifies whether to output progress indicator or not

Joins your json files from the sourcedir and using reformat_data for each filedata if passed attrs. 
Saves the joined file
Returns tuple (status code, process info)
<br>

`main():`

A mini demo for reformat_file & join_files.
<br>

Thats all, hopefully this module helps you.
