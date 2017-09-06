# this script removes all files from the CTU-13 dataset EXCEPT for the binetflow files.

DIR='./CTU-13-Dataset'

# iterate the subdirs and remove files that are not .binetflow files
find $DIR ! -name '*.binetflow' -type f -exec rm -f {} +

# move the binetflow files up a dir
mv $DIR/*/*.binetflow $DIR/ 
# clean up
rm -r $DIR/*/

