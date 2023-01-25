import os
from wand.image import Image
from pathlib import Path

# input parameters
directory_in_str = r"C:\Astrocache\20220119\tif"
out_str = r"out"
bnw_str = r"bnw"
colorized_str = r"colorized"
tint_str = r"gold"

# # Overrides. Uncomment and customize as needed.
# directory_in_str = r"C:\Astrocache\20220119\tif\d11g-2.5-5-10-15"
# # directory_in_str = r"C:\Astrocache\20220119\tif\l11g-10-5-2-2"
# # directory_in_str = r"C:\Astrocache\20220119\tif\l11g-10-10-10-10-10-10"
# out_str = r"gold"

directory_in = Path(directory_in_str)
print(f'directory_in: {directory_in}')

directory_in_path_name = directory_in.name
print(f'  directory: {directory_in_path_name}')
print()

pathlist = Path(directory_in).rglob('*.png')
for path in pathlist:
    image_filename = os.fsdecode(path)

    full_filename = Path(directory_in, path.name)
    print(f'Opening: {full_filename}')

    directory_out = Path((str(path.parent)).replace(
        directory_in_path_name, out_str))
    # print(f'  directory_out: {directory_out}')

    directory_out_bnw = Path(directory_out, bnw_str)
    if not os.path.exists(directory_out_bnw):
        os.makedirs(directory_out_bnw)
    # print(f'  directory_out_bnw: {directory_out_bnw}')

    directory_out_colorized = Path(directory_out, colorized_str)
    if not os.path.exists(directory_out_colorized):
        os.makedirs(directory_out_colorized)
    # print(f'  directory_out_colorized: {directory_out_colorized}')

    with Image(filename=path) as img:
        # format image type
        img.format = 'jpeg'

        # # equalize. method 1
        # img.auto_level()
        # img.auto_gamma()
        # img.clahe(img.width, img.height, 65536, 7)

        # # equalize. method 2
        # img.level(black=0.05, white=1.0)

        # save
        filename_out = path.name.replace(r".png", r".jpg")
        full_filename_out = Path(directory_out_bnw, filename_out)
        print(f'  Saving: {full_filename_out}')
        img.save(filename=full_filename_out)

        # colorize (duotone). method 1
        # r = 1.0
        # g = 0.75*0.95
        # b = 0.05
        # s = r+g+b
        # f = 3/s
        # img.gamma(f * r, 'red')
        # img.gamma(f * g, 'green')
        # img.gamma(f * b, 'blue')

        # colorize (duotone). method 2
        img.tint(tint_str, 'white')

        # sharpen
        img.unsharp_mask(0.0, 3.0, 1.0, 0.2)

        # save colorized
        filename_out_colorized = path.name.replace(r".png", r".colorized.jpg")
        full_filename_out_colorized = Path(
            directory_out_colorized, filename_out_colorized)
        print(f'  Saving: {full_filename_out_colorized}')
        img.save(filename=full_filename_out_colorized)

        # finish off file
        print()
