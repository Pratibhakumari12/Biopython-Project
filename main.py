import sys
from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML

print("--- STARTING BIOINFORMATICS PIPELINE ---")

try:
    print("Step 1: Loading sequence from file...")
    record = SeqIO.read("unknown.fasta", "fasta")
    print(f"   Success! Sequence Length: {len(record.seq)} amino acids")
except FileNotFoundError:
    print("   ERROR: 'unknown.fasta' not found!")
    sys.exit()

print("\nStep 2: Connecting to NCBI Server (Running BLAST)...")
print("   (Please wait... Do not close this window...)")

result_handle = NCBIWWW.qblast("blastp", "nr", record.seq)

print("   BLAST finished! Saving output to 'my_blast.xml'...")
with open("my_blast.xml", "w") as out_handle:
    out_handle.write(result_handle.read())
result_handle.close()

print("\nStep 3: Analyzing Results...")
result_handle = open("my_blast.xml")
blast_record = NCBIXML.read(result_handle)

top_hit = blast_record.alignments[0]

print(f"\n--- FINAL REPORT ---")
print(f"Identified Gene: {top_hit.title}")
print(f"Significance (E-Value): {top_hit.hsps[0].expect}")
print(f"Conclusion: The sequence is confirmed to be {top_hit.title.split('|')[2]}")
print("--------------------")