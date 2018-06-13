# FileHandler specs

## Read chunks

The `read_chunk` method read a chunk of the selected file. The chunk size is set as a payload size in he top of the file.
The method returns the read chunks and if it's the last part of the file, it returns eof true.

## Write chunks

The `write_chunk` checks if the file exits and if it does, it append to the file, else the method creates the file and wirte the first chunk.
