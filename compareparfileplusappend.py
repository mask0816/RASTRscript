#! /usr/bin/env python
import sys
import time
import numpy as np
import argparse

### get parse to figure out what parameters to be compared
def parserInput(args):
        parser=argparse.ArgumentParser(description='what column to change')
        parser.add_argument('-phi','--anglephi',action='store_true',default=False,dest='phi')
        parser.add_argument('-theta','--angletheta',action='store_true',default=False,dest='theta')
        parser.add_argument('-psi','--anglepsi',action='store_true',default=False,dest='psi')
	parser.add_argument('-x','--shx',action='store_true',default=False,dest='x')
	parser.add_argument('-y','--shy',action='store_true',default=False,dest='y')
        return parser.parse_args(args)
### rmsd measurement method1, stupiest method
def rmsd_slow(list1,list2):
	n=0
	tempsum=0
	rmsdvalue='none'
	if len(list1)==len(list2):
		for i in range(len(list1)):
			dif=min(pow((list1[i]-list2[i]),2),pow((list1[i]-list2[i]+180),2),pow((list1[i]-list2[i]-180),2))
			tempsum+=dif
			n+=1
		rmsdvalue=pow(tempsum/n,0.5)
	return rmsdvalue

### rmsd measurement method2 using np array method, much quicker
def rmsd(list1,list2):
	l1=np.array(list1)
	l2=np.array(list2)
	difnce=l1-l2
	difnce=abs(difnce)
	## np.minimum only take two array
	minimum=np.minimum(difnce,abs(difnce-180))
	difnce=np.minimum(minimum,abs(difnce-360))

	rmsd=pow((difnce*difnce).mean(),0.5)
	## below lines are added specially for extract particles with psi not well aligned
	noaligns=[]
	count=0
	for i in range(len(difnce)):
		if difnce[i]>10:
			count+=1
			noaligns.append(i+1)
	print noaligns
	print count
		
	return rmsd

### extract parameters from .par file	
def extractpar(filename):
	f=open(filename,'r')
	lines=f.readlines()
	f.close()
	value={}
	psilist=[]
	philist=[]
	thetalist=[]
	shxlist=[]
	shylist=[]
	for line in lines:
		words=line.split()
		if words[0]=='C':
			continue
                psi=words[1]
                phi=words[3]
		theta=words[2]
                shx=words[4]
                shy=words[5]
		try:
		### change below line, do not change above
		    psilist.append(float(psi))
		    philist.append(float(phi))
		    thetalist.append(float(theta))
		    shxlist.append(float(shx))
		    shylist.append(float(shy))
		except:
		    continue
	value['phi']=philist
	value['psi']=psilist
	value['theta']=thetalist
	value['shx']=shxlist
	value['shy']=shylist
	return value
### extract parameters from .star file
def extractstar(filename):
	##to be finished
	f=open(filename,'r')


### main function
def main():
	argv=sys.argv
	file1=argv[1]
	file2=argv[2]
	parse=parserInput(argv[3:])
	# parameters from file 1
	values_1=extractpar(file1)
	# parameters from file 2
	values_2=extractpar(file2)
	if parse.phi:
		phirmsd=rmsd(values_1['phi'],values_2['phi'])
		print "phi rmsd: ", phirmsd
	if parse.psi:
                psirmsd=rmsd(values_1['psi'],values_2['psi'])
                print "psi rmsd: ", psirmsd	
	if parse.theta:
                thetarmsd=rmsd(values_1['theta'],values_2['theta'])
                print "theta rmsd: ", thetarmsd
	if parse.x:
                shxrmsd=rmsd(values_1['shx'],values_2['shx'])
                print "shx rmsd: ", shxrmsd
	if parse.y:
                shyrmsd=rmsd(values_1['shy'],values_2['shy'])
		print "shy rmsd: ", shyrmsd 
	
if __name__=="__main__":
	main()	
