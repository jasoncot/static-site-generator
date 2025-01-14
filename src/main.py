import functools
import os
import shutil
from textnode import TextNode, TextType

def files_and_dirs_accumulator(files_and_dirs, item):
	if os.path.is_file(item):
		return [files_and_dirs[0] + [item], files_and_dirs[1]]
	return [files_and_dirs[0], files_and_dirs[1] + [item]]

def copy_dir_files_to_dest(src_path, dest_path):
	# make sure we have files that we will be doing things
	if not os.path.exists(src_path):
		raise Exception("source path does not exist")
	
	if os.path.exists(dest_path):
		shutil.rmtree(dest_path)

	os.path.mkdir(dest_path)
	
	[files, dirs] = functools.reduce(
		files_and_dirs_accumulator,
		os.listdir(src_path)
	)

	print(f"Copying files from directory {src_path} -> {dest_path}")
	for file in files:
		print(f" * {file}")
		shutil.copy(os.path.join(src_path, file), os.path.join(dest_path, file))

	for dir in dirs:
		print(f"Moving into subdirectory {src_path} {dir}")
		copy_dir_files_to_dest(
			os.path.join(src_path, dir),
			os.path.join(dest_path, dir)
		)



def main():
	text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
	print(text_node)

main()
