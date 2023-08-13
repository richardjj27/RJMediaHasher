#!/usr/bin/python
#sudo apt install attr
#pip install pyxattr

import os, xattr, subprocess, time

def getmd5hash(fname):
   cmd = "md5sum " + fname + " | cut -d ' ' -f 1"
   md5hash = subprocess.run(cmd, capture_output=True, shell=True, text=True)
   return md5hash.stdout.rstrip('\n')

def getmodtime(fname):
   ti_m = os.path.getmtime(fname)
   m_ti = time.ctime(ti_m)
   t_obj = time.strptime(m_ti)
   return time.strftime("%Y-%m-%d %H:%M:%S",  t_obj)

def process_attributes(filepath, filetype):
   #paths = []
   for root, dirs, files in os.walk(filepath):
      for file in files:
         if file.lower().endswith(filetype.lower()):
            filename = os.path.join(root, file)
            xattr.setxattr(filename, "user.comment", "Simple text file abc")

            print(filename)
            print(getmodtime(filename))
            print(getmd5hash(filename))

            # the attributes
            #user.md5hash
            #user.md5time

   return

process_attributes('./test', 'txt')
