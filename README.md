###ChunkedADNS
ChunkedADNS is a tool to help you resolve an extremely large number of domains (2+ million) asynchronously (read:extremely quickly) while also giving you fine-grained control of the entire process. It does this by taking a mammoth single input file consisting of a lot of domain names, splitting it into "chunks" and resolving each chunk in parallel. Based on the async_dns python library by prkumins. Be sure to read his excellent [blog post](http://www.catonmat.net/blog/asynchronous-dns-resolution/) on ADNS resoltuion!<br/>

I was able to resolve over 2 million domain names in under two hours using a single chunk (i.e. in the worst case)

####Features:
#####1. Session Resumption
In case something goes wrong and you have to abort ADNS resolution for whatever reason, you can carry on from where you left off the next time you run it
#####2. Chunked / Distributed Processing
Each ADNS input file is split into a number of chunks and each chunk is resolved in parallel using Python Multiprocessing
#####3. Fine-grained Control [*partially implemented]
You can control the number of chunks you want to use, the size of each and also the intensity of DNS requests (i.e. how many DNS requests are made per second)


####Important Notes:
1. You need to install both the ADNS C library and it's Python wrapper for the ChunkedADNS program to work. See the last section for details on how to install both
2. Make sure the input file contains only one domain per line and nothing else
3. All output files will be in the results/ directory
4. If you're using your corporate DNS server for name resolution, you may get yelled at by your sysadmin for bombarding the server with too many queries. I did.

####Usage: 
./ChunkedADNS.sh<br/>
Just run the script without any arguments since it operates in interactive mode. You will be prompted for every input. 
The output file ["ADNS_OUTPUT_<date>".csv] will be in the results/ directory. If a domain name could not be resolved, you'll get 'ERR_NOT_RESOLVED' instead of the IP Address

####Installing the ADNS C library and its Python Wrapper:
Read the README_ADNSInstallInstructions.md in the help/ directory
