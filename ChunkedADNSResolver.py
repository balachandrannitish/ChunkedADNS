from async_dns import AsyncResolver
from time import time
import sys
import os

def Generate_Domains_List(filepath):
	'''
	Generates the full list of domains to be resolved from a file.
	Each line in the file must have one domain name per line. For instance,

		google.com
		oracle.com
		yahoo.com
	
	IMPORTANT: Duplicate domain names, if any, will be removed as they make the ADNS Resolver hang
	'''
	try:
		f = open(filepath,'r')
	except IOError:
		print "The file at " + filepath + " doesn't exist.\n"

	DomainList = []
	for line in f:
		text = line.replace('\r',"").replace('"',"").replace("\n","")
		Current = text
		DomainList.append(Current)
	#---Use the domain list below for testing---
	#DomainList = ["www.google.com", "www.reddit.com", "www.nonexistz.net"]
	#---------------------------------------------------------------------
	DomainList = list(set(DomainList))   # Remove duplicate domain names. E.g. - If duplicates exist in the list; they will only occur once after this line
	return DomainList



def doAsyncDNSResolution(DomainList):
	'''
	Resolves the domains in the DomainList argument very quickly, asynchronously. 
	Returns a dictionary of {'host': 'ip'}

	@DomainList = A list of domains to be resolved. 

	IMPORTANT: The DomainList cannot contain duplicate domain names 
	or else this function will NEVER return!
	'''
	ar = AsyncResolver(DomainList,intensity=100)
	resolved = ar.resolve()
	return resolved



def Resolve_Chunk(input_chunk_path,chunk_number):
	"""
	Takes the path to an individual chunk and its chunk_number as input and
	does two things:

	1. Resolves the domain names in the chunk using ADNS
	2. Writes the Domain and IP to a CSV output file specific to the chunk [filename = 'output_<ChunkNumber>']

	E.G - If chunk number given as input is '07', the output_file will be named "output_07"
	Basically, separate output files are generated for EACH chunk number. 
	These are later combined into a single output file by the main shell script, ChunkedADNSResolver.sh

	@param: input_chunk_path = The relative or absolute path to a single chunk
	@param: chunk_number = This number is used to identify which chunk this is. [E.g. - first, second, etc.]
	"""
	print "Chunk " + chunk_number + ": Generating Domain List"
	DomainList = Generate_Domains_List(input_chunk_path)
	
	print "Chunk " + chunk_number + ": Domain List Generation complete; Number of Domains = " + str(len(DomainList))
	print "Chunk " + chunk_number + ": Begin ADNS Resolution "
	Result = doAsyncDNSResolution(DomainList)
	
	print "Chunk " + chunk_number + ": DNS resolution complete"
	output_file_path = "temp/output/output_" + chunk_number
	
	print "Chunk " + chunk_number + ": Writing to output file: output_" + chunk_number
	with open(output_file_path,"w") as output_file:
		for host, ip in Result.items():
			if ip is None:
				output_file.write("%s,ERR_NOT_RESOLVED\n" % host)
			else:
				output_file.write("%s,%s\n" % (host, ip))


if __name__=='__main__':
	
	StartTime = time()
	
	input_chunk_path = sys.argv[1]      # EXAMPLE: input_chunk_path = "/home/nsadmin/ADNS/temp/input/input_03"
	input_file_name = input_chunk_path.split("/")[len(input_chunk_path.split("/")) - 1]   # input_file_name = "input_03"
	chunk_number = input_file_name.split("_")[len(input_file_name.split("_")) - 1]   # Chunk number = "03"
	
	output_chunk_path = r"temp/output/output_" + chunk_number 

	if os.path.exists(output_chunk_path):       # Check to ensure that if a particular input chunk had been previously processed and an output chunk had been generated, skip it this time
		EndTime = time()
		print "Chunk " + chunk_number + ": ALREADY PROCESSED. SKIPPING.\n" + "Chunk " + chunk_number + ": Total Time Taken (in seconds): %.2f" % (EndTime - StartTime)
	else:
		Resolve_Chunk(input_chunk_path,chunk_number)
		EndTime = time()
		print "Chunk " + chunk_number + ": ADNS RESOLUTION & OUTPUT FILE GENERATION COMPLETE!\n" + "Chunk " + chunk_number + ": Total Time Taken (in seconds): %.2f" % (EndTime - StartTime)

	




