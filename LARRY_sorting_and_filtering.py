import os, pickle, gzip

successes = []
no_fastq = []
no_abundant_bcs = []
if not os.path.exists('LARRY_tmp'):
	os.mkdir('LARRY_tmp')
	
for f in os.listdir('.'):
	if os.path.isdir(f):
	
		# check that there is at least 1 *.fastq.sorted.fastq.gz file
		sorted_fastqs = []
		if os.path.exists(f+'/filtered_parts'):
			sorted_fastqs = [ff for ff in os.listdir(f+'/filtered_parts') if ff.endswith('fastq')]
			sorted_fastqs = [f+'/filtered_parts/'+ff for ff in sorted_fastqs]
		
		# check that there is an abundant bcs file
		abundant_bcs = [ff for ff in os.listdir(f) if ff=='abundant_barcodes.pickle']
		
		# check that all the needed files are available...
		if len(abundant_bcs) == 0: no_abundant_bcs.append(f)
		if len(sorted_fastqs) == 0: no_fastq.append(f)
		
		# if we have all the necessary files, then let's go ahead and extract BC sequences	
		if len(abundant_bcs)>0 and len(sorted_fastqs)>0:
			
			# first, grep out lines with the barcode sequence...
			gfp_seq = 'taaccgttgctaggagagaccatatg'.upper()
			
			for i,ff in enumerate(sorted_fastqs):
				print('Retrieving barcode reads from '+ff.split('/')[-1])
				os.system('grep '+gfp_seq+' '+ff+' -B 1 >> LARRY_tmp/'+f+'_BC_'+repr(i)+'.txt')
		


if len(no_abundant_bcs) > 0:
	print('\nThe following libraries had no abundant_barcodes.pickle file')
	for f in no_abundant_bcs: print(f)

if len(no_fastq) > 0:
	print('\nThe following libraries had no fastq file')
	for f in no_fastq: print(f)
print('\n')

# Filtering and combining barcode reads

def is_valid(bc):
	return bc[4:6]=='TG' and bc[10:12]=='CA' and bc[16:18]=='AC' and bc[22:24]=='GA' and bc[-1]=='G'

out = gzip.open('LARRY_sorted_and_filtered_barcodes.fastq.gz','wb')
gfp_seq = 'taaccgttgctaggagagaccatatg'.upper()

for f in os.listdir('LARRY_tmp'):
	print('Filtering reads from ',f)
	lib = f[:-9]
	ab_bc = pickle.load(open(lib+'/abundant_barcodes.pickle','rb'))
	
	for xx in open('LARRY_tmp/'+f).read().strip('\n').split('--'):
		xx = xx.strip('\n').split('\n')
		gfp_bc = xx[1].split(gfp_seq)[1]
		umi = xx[0].split(':')[1]
		cell_bc = xx[0].split(':')[0][1:]
		if len(gfp_bc) >= 29:
			gfp_bc = gfp_bc[:29]
			if is_valid(gfp_bc):
				if cell_bc in ab_bc:
					tag = '>'+lib+','+ab_bc[cell_bc][0]+','+umi
					out.write((tag+'\n').encode('utf-8'))
					out.write((gfp_bc+'\n').encode('utf-8'))
					out.write('\n'.encode('utf-8'))
out.close()

			
