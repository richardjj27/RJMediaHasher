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
   return time.strftime("%Y-%m-%d %H:%M:%S", t_obj)

def gethashtimeattribute(fname):
   try:
      t_obj = xattr.getxattr(fname, "user.md5time")
   #m_ti = time.ctime(ti_m)
   #t_obj = time.strptime(m_ti)
   except Exception as e:
      t_obj = "null"
   return t_obj

def setextendedattribute(fname, attribute, value):
   try:
      xattr.setxattr(fname, attribute, value)
      print ("attribute set for " + fname + " (" + attribute + " / " + value + ")")
   except Exception as e:
      print ("attribute set for " + fname + " (" + attribute + " / " + value + ") : failed")

def process_attributes(filepath, filetype):
   #paths = []
   for root, dirs, files in os.walk(filepath):
      for file in files:
         if file.lower().endswith(tuple(filetype)):
            filename = os.path.join(root, file)
            
            modtime = getmodtime(filename)
            md5hashtimeattribute = gethashtimeattribute(filename)
            md5hash = getmd5hash(filename)
            
            print(filename)
            print(modtime)
            print(md5hashtimeattribute)
            print(md5hash)

            #xattr.setxattr(filename, "user.md5time", modtime)
            #xattr.setxattr(filename, "user.md5hash", md5hash)

            #print(getmodtime(filename))
            #print(getmd5hash(filename))


            try:
               xattr.removexattr(filename, "user.md5hash")
            except Exception as e:
               pass

            try:
               xattr.removexattr(filename, "user.md5time")
            except Exception as e:
               pass

            setextendedattribute(filename, "user.md5hash", getmd5hash(filename))
            setextendedattribute(filename, "user.md5time", getmodtime(filename))

            print("=======================")

            #xattr.setxattr(filename, "user.md5hash", getmd5hash(filename))
            #xattr.setxattr(filename, "user.md5time", getmodtime(filename))
            # the attributes
            #user.md5hash
            #user.md5time

   return

process_attributes('./test', [".avi", ".mp4"])
