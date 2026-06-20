#paste this in bash
# python -c "
# import zipfile, os
# animals = ['lion', 'tiger', 'elephant', 'giraffe', 'penguin', 'dolphin', 'cheetah', 'gorilla', 'zebra', 'kangaroo']
# for animal in animals:
#     with zipfile.ZipFile(f'{animal}.zip', 'w') as z:
#         z.writestr(f'{animal}.txt', '')
# print('Done!')
# "