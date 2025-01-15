import functools
import os
import shutil
from textnode import TextNode, TextType
from utils import generate_page
import re

def set_source_dir_for_accumulator(dir):
	def files_and_dirs_accumulator(files_and_dirs, item):
		if os.path.isfile(os.path.join(dir, item)) == True:
			return [files_and_dirs[0] + [item], files_and_dirs[1]]
		return [files_and_dirs[0], files_and_dirs[1] + [item]]
	
	return files_and_dirs_accumulator

def copy_dir_files_to_dest(src_path, dest_path):
	# make sure we have files that we will be doing things
	if not os.path.exists(src_path):
		raise Exception("source path does not exist")
	
	if os.path.exists(dest_path):
		print(f"Cleaning up new destination path ({dest_path})")
		shutil.rmtree(dest_path)

	print(f"Creating destination directory ({dest_path})")
	os.mkdir(dest_path)

	[files, dirs] = functools.reduce(
		set_source_dir_for_accumulator(src_path),
		os.listdir(src_path),
		[[], []]
	)

	print(f"Copying files from directory {src_path} -> {dest_path}")
	for file in files:
		print(f" * {file}")
		shutil.copy(os.path.join(src_path, file), os.path.join(dest_path, file))

	for dir in dirs:
		print(f"Moving into subdirectory {os.path.join(src_path, dir)}")
		copy_dir_files_to_dest(
			os.path.join(src_path, dir),
			os.path.join(dest_path, dir)
		)

def crawl_dir_for_files(src_path):
	if not os.path.exists(src_path):
		raise Exception("source path does not exist")

	[files, dirs] = functools.reduce(
		set_source_dir_for_accumulator(src_path),
		os.listdir(src_path),
		[[], []]
	)

	if len(files) == 0 and len(dirs) == 0:
		return []
	
	collected_files = []
	collected_files += list(map(lambda file: os.path.join(src_path, file), files))
	collected_files += functools.reduce(
		lambda acc, dir: acc + crawl_dir_for_files(os.path.join(src_path, dir)),
		dirs,
		[]
	)
	return collected_files

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	files_to_convert = crawl_dir_for_files(dir_path_content)
	print("files to convert: ", files_to_convert)
	pairs = list(map(
		lambda file_name: [file_name, re.sub(r"\.md$", ".html", file_name).replace(dir_path_content, dest_dir_path)],
		files_to_convert
	))
	for pair in pairs:
		generate_page(pair[0], template_path, pair[1])


def main():
	copy_dir_files_to_dest('./static', './public')
	generate_pages_recursive("./content", "./src/template.html", "./public")


main()
